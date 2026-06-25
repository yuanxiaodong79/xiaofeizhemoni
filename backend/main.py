from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import engine, get_db_connection
from routers import agents, campaigns

app = FastAPI(
    title="营销风洞智能体沙盘平台",
    description="营销策略的虚拟A/B测试平台后端API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents.router, prefix="/api/agents", tags=["智能体"])
app.include_router(campaigns.router, prefix="/api/campaigns", tags=["营销活动"])

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "营销风洞智能体沙盘平台后端服务正常运行"}

@app.get("/api/llm/status")
async def llm_status():
    from services.llm_service import llm_service
    return {
        "provider": llm_service.provider,
        "model": llm_service.model,
        "enabled": llm_service.client is not None
    }

@app.on_event("startup")
async def startup_event():
    try:
        conn = get_db_connection()
        conn.close()
        print("数据库连接成功")
    except Exception as e:
        print(f"数据库连接失败: {e}")
    
    from services.llm_service import llm_service
    llm_service.initialize()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)