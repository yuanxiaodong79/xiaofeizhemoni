from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from models.schemas import (
    AgentCreate, AgentUpdate, AgentResponse, 
    PersonaTemplate, StatsResponse, PaginatedResponse
)
from config.database import get_db

router = APIRouter()

PERSONA_TEMPLATES = [
    {"type": "price_sensitive", "name": "价格敏感型", "description": "对价格非常敏感，倾向于购买低价商品"},
    {"type": "impulse", "name": "冲动消费型", "description": "容易被促销活动吸引，购买决策快"},
    {"type": "brand_loyal", "name": "品牌忠诚型", "description": "对特定品牌有较高忠诚度"},
    {"type": "rational", "name": "理性决策型", "description": "购买前会仔细比较，决策较为理性"},
    {"type": "deal_seeker", "name": "优惠追寻型", "description": "喜欢寻找优惠券和促销活动"}
]

DEFAULT_BEHAVIOR = {
    "price_sensitive": {"click_rate": 0.03, "conversion_rate": 0.01, "brand_loyalty": 0.2, "impulsivity": 0.1},
    "impulse": {"click_rate": 0.08, "conversion_rate": 0.04, "brand_loyalty": 0.3, "impulsivity": 0.8},
    "brand_loyal": {"click_rate": 0.06, "conversion_rate": 0.05, "brand_loyalty": 0.9, "impulsivity": 0.2},
    "rational": {"click_rate": 0.04, "conversion_rate": 0.03, "brand_loyalty": 0.5, "impulsivity": 0.1},
    "deal_seeker": {"click_rate": 0.09, "conversion_rate": 0.06, "brand_loyalty": 0.1, "impulsivity": 0.5}
}

@router.get("/", response_model=PaginatedResponse)
async def get_agents(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    persona_type: Optional[str] = None
):
    offset = (page - 1) * page_size
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        count_query = "SELECT COUNT(*) FROM agents WHERE status = 'active'"
        params = []
        if persona_type:
            count_query += " AND persona_type = %s"
            params.append(persona_type)
        
        cursor.execute(count_query, params)
        total = cursor.fetchone()[0]
        
        query = """
            SELECT * FROM agents 
            WHERE status = 'active'
        """
        if persona_type:
            query += " AND persona_type = %s"
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            cursor.execute(query, [persona_type, page_size, offset])
        else:
            query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
            cursor.execute(query, [page_size, offset])
        
        rows = cursor.fetchall()
        
        agents = []
        for row in rows:
            agents.append({
                "id": str(row[0]),
                "name": row[1],
                "personaType": row[2],
                "demographics": row[3],
                "interests": row[4],
                "behaviorScore": row[5],
                "memory": row[6] or [],
                "status": row[7],
                "createdAt": row[8].isoformat() if row[8] else None
            })
        
        return {"data": agents, "total": total, "page": page, "page_size": page_size}

@router.get("/persona-templates", response_model=list[PersonaTemplate])
async def get_persona_templates():
    return PERSONA_TEMPLATES

@router.get("/stats", response_model=StatsResponse)
async def get_agent_stats():
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM agents")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM agents WHERE status = 'active'")
        active = cursor.fetchone()[0]
        
        cursor.execute("SELECT persona_type, COUNT(*) FROM agents GROUP BY persona_type")
        rows = cursor.fetchall()
        
        by_persona = {}
        for row in rows:
            by_persona[row[0]] = row[1]
        
        return {"total": total, "active": active, "by_persona": by_persona}

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agents WHERE id = %s", (agent_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        return {
            "id": str(row[0]),
            "name": row[1],
            "persona_type": row[2],
            "demographics": row[3],
            "interests": row[4],
            "behavior_score": row[5],
            "memory": row[6] or [],
            "status": row[7],
            "created_at": row[8]
        }

@router.post("/", response_model=AgentResponse, status_code=201)
async def create_agent(agent: AgentCreate, use_llm: bool = False):
    from services.llm_service import llm_service
    
    if use_llm:
        agent_profile = {
            "name": agent.name,
            "persona_type": agent.persona_type,
            "demographics": agent.demographics.model_dump() if agent.demographics else {"age": 30, "gender": "male", "location": "一线城市"},
            "interests": agent.interests or ["购物"]
        }
        llm_result = await llm_service.generate_behavior_score(agent_profile)
        behavior = llm_result.get("behavior_score", DEFAULT_BEHAVIOR.get(agent.persona_type, DEFAULT_BEHAVIOR["rational"]))
    else:
        behavior = DEFAULT_BEHAVIOR.get(agent.persona_type, DEFAULT_BEHAVIOR["rational"])
    
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO agents (name, persona_type, demographics, interests, behavior_score, memory, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            agent.name,
            agent.persona_type,
            agent.demographics.model_dump() if agent.demographics else {"age": 30, "gender": "male", "location": "一线城市"},
            agent.interests or ["购物"],
            behavior,
            [],
            "active"
        ))
        
        row = cursor.fetchone()
        
        return {
            "id": str(row[0]),
            "name": row[1],
            "persona_type": row[2],
            "demographics": row[3],
            "interests": row[4],
            "behavior_score": row[5],
            "memory": row[6] or [],
            "status": row[7],
            "created_at": row[8]
        }

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, agent: AgentUpdate):
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM agents WHERE id = %s", (agent_id,))
        existing = cursor.fetchone()
        
        if not existing:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        updates = []
        params = []
        
        if agent.name is not None:
            updates.append("name = %s")
            params.append(agent.name)
        if agent.persona_type is not None:
            updates.append("persona_type = %s")
            params.append(agent.persona_type)
        if agent.demographics is not None:
            updates.append("demographics = %s")
            params.append(agent.demographics.model_dump())
        if agent.interests is not None:
            updates.append("interests = %s")
            params.append(agent.interests)
        if agent.status is not None:
            updates.append("status = %s")
            params.append(agent.status)
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(agent_id)
        
        cursor.execute(f"""
            UPDATE agents SET {', '.join(updates)}
            WHERE id = %s
            RETURNING *
        """, params)
        
        row = cursor.fetchone()
        
        return {
            "id": str(row[0]),
            "name": row[1],
            "persona_type": row[2],
            "demographics": row[3],
            "interests": row[4],
            "behavior_score": row[5],
            "memory": row[6] or [],
            "status": row[7],
            "created_at": row[8],
            "updated_at": row[9]
        }

@router.delete("/{agent_id}", status_code=204)
async def delete_agent(agent_id: str):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM agents WHERE id = %s", (agent_id,))
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        return None