from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import Optional
from models.schemas import (
    CampaignCreate, CampaignResponse, 
    SimulationResultResponse, CampaignStatsResponse, PaginatedResponse
)
from config.database import get_db
from services.simulation_engine import run_simulation, load_agents_from_db

router = APIRouter()

async def run_simulation_background(campaign_id: str, campaign_data: dict, use_llm: bool):
    import json
    try:
        agents = await load_agents_from_db()
        results = await run_simulation(campaign_data, agents, use_llm)
        
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE campaigns SET status = %s, completed_at = CURRENT_TIMESTAMP WHERE id = %s",
                ("completed", campaign_id)
            )
            
            cursor.execute("""
                INSERT INTO simulation_results (campaign_id, variant_results, metrics, summary)
                VALUES (%s, %s, %s, %s)
                RETURNING *
            """, (
                campaign_id,
                json.dumps(results["variant_results"]),
                json.dumps(results["metrics"]),
                results["summary"]
            ))
    except Exception as e:
        print(f"Background simulation error: {str(e)}")
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE campaigns SET status = %s WHERE id = %s",
                ("failed", campaign_id)
            )

@router.get("/", response_model=PaginatedResponse)
async def get_campaigns(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None
):
    offset = (page - 1) * page_size
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        count_query = "SELECT COUNT(*) FROM campaigns"
        params = []
        if status:
            count_query += " WHERE status = %s"
            params.append(status)
        
        cursor.execute(count_query, params)
        total_row = cursor.fetchone()
        total = total_row[0] if isinstance(total_row, (list, tuple)) else total_row.get('count', 0)
        
        query = "SELECT * FROM campaigns"
        if status:
            query += " WHERE status = %s"
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            cursor.execute(query, [status, page_size, offset])
        else:
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            cursor.execute(query, [page_size, offset])
        
        rows = cursor.fetchall()
        
        campaigns = []
        for row in rows:
            campaigns.append({
                "id": str(row['id']),
                "name": row['name'],
                "type": row['type'],
                "variants": row['variants'],
                "target_audience": row['target_audience'],
                "agent_count": row['agent_count'],
                "status": row['status'],
                "created_at": row['created_at'].isoformat() if row['created_at'] else None,
                "started_at": row['started_at'].isoformat() if row['started_at'] else None,
                "completed_at": row['completed_at'].isoformat() if row['completed_at'] else None
            })
        
        return {"data": campaigns, "total": total, "page": page, "page_size": page_size}

@router.get("/stats", response_model=CampaignStatsResponse)
async def get_campaign_stats():
    with get_db() as conn:
        cursor = conn.cursor()
        
        def get_count(query, params=None):
            cursor.execute(query, params or [])
            row = cursor.fetchone()
            return row[0] if isinstance(row, (list, tuple)) else row.get('count', 0)
        
        total = get_count("SELECT COUNT(*) FROM campaigns")
        running = get_count("SELECT COUNT(*) FROM campaigns WHERE status = %s", ['running'])
        completed = get_count("SELECT COUNT(*) FROM campaigns WHERE status = %s", ['completed'])
        draft = get_count("SELECT COUNT(*) FROM campaigns WHERE status = %s", ['draft'])
        
        return {"total": total, "running": running, "completed": completed, "draft": draft}

@router.get("/{campaign_id}")
async def get_campaign(campaign_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM campaigns WHERE id = %s", (campaign_id,))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Campaign not found")

        # 查询最新的模拟结果
        cursor.execute("""
            SELECT variant_results, metrics, summary, timestamp
            FROM simulation_results
            WHERE campaign_id = %s
            ORDER BY timestamp DESC LIMIT 1
        """, (campaign_id,))
        result_row = cursor.fetchone()

        variant_results = []
        metrics = {}
        summary = None
        if result_row:
            import json
            variant_results = result_row['variant_results'] if isinstance(result_row['variant_results'], list) else json.loads(result_row['variant_results'] or '[]')
            metrics = result_row['metrics'] if isinstance(result_row['metrics'], dict) else json.loads(result_row['metrics'] or '{}')
            summary = result_row['summary']

        return {
            "id": str(row['id']),
            "name": row['name'],
            "type": row['type'],
            "variants": row['variants'],
            "target_audience": row['target_audience'],
            "agent_count": row['agent_count'],
            "status": row['status'],
            "created_at": row['created_at'],
            "started_at": row['started_at'],
            "completed_at": row['completed_at'],
            "variant_results": variant_results,
            "metrics": metrics,
            "summary": summary
        }

@router.post("/", response_model=CampaignResponse, status_code=201)
async def create_campaign(campaign: CampaignCreate):
    import json
    variants = [
        {
            "id": v.id if v.id else chr(65 + i),
            "title": v.title,
            "description": v.description,
            "price": v.price
        }
        for i, v in enumerate(campaign.variants)
    ]
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO campaigns (name, type, variants, target_audience, agent_count, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            campaign.name,
            campaign.type,
            json.dumps(variants),
            json.dumps(campaign.target_audience.model_dump()),
            campaign.agent_count,
            "draft"
        ))
        
        row = cursor.fetchone()
        
        return {
            "id": str(row['id']),
            "name": row['name'],
            "type": row['type'],
            "variants": row['variants'],
            "target_audience": row['target_audience'],
            "agent_count": row['agent_count'],
            "status": row['status'],
            "created_at": row['created_at']
        }

@router.post("/{campaign_id}/start")
async def start_simulation(campaign_id: str, use_llm: bool = False, background_tasks: BackgroundTasks = None):
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM campaigns WHERE id = %s", (campaign_id,))
        campaign_row = cursor.fetchone()
        
        if not campaign_row:
            raise HTTPException(status_code=404, detail="Campaign not found")
        
        if campaign_row['status'] == "running":
            raise HTTPException(status_code=400, detail="Campaign is already running")
        
        cursor.execute(
            "UPDATE campaigns SET status = %s, started_at = CURRENT_TIMESTAMP WHERE id = %s",
            ("running", campaign_id)
        )
        
        campaign_data = {
            "id": str(campaign_row['id']),
            "name": campaign_row['name'],
            "type": campaign_row['type'],
            "variants": campaign_row['variants'],
            "target_audience": campaign_row['target_audience'],
            "agent_count": campaign_row['agent_count']
        }
        
        if background_tasks:
            background_tasks.add_task(run_simulation_background, campaign_id, campaign_data, use_llm)
        
        return {
            "message": "Simulation started",
            "campaign_id": campaign_id,
            "status": "running",
            "use_llm": use_llm
        }

@router.get("/{campaign_id}/results", response_model=list[SimulationResultResponse])
async def get_simulation_results(campaign_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM simulation_results 
            WHERE campaign_id = %s 
            ORDER BY timestamp DESC
        """, (campaign_id,))
        
        rows = cursor.fetchall()
        
        if not rows:
            raise HTTPException(status_code=404, detail="No results found for this campaign")
        
        results = []
        for row in rows:
            results.append({
                "id": str(row[0]),
                "campaign_id": str(row[1]),
                "variant_results": row[2],
                "metrics": row[3],
                "summary": row[4],
                "timestamp": row[5]
            })
        
        return results