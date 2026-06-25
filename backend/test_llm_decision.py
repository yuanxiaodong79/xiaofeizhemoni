import asyncio
from services.llm_service import llm_service

async def test_llm_decision():
    print("=== 测试LLM决策 ===")
    
    agent = {
        "id": "agent-001",
        "name": "虚拟用户001",
        "persona_type": "price_sensitive",
        "demographics": {"age": 25, "gender": "female", "location": "一线城市"},
        "interests": ["美妆", "护肤"],
        "behavior_score": {"click_rate": 0.03, "conversion_rate": 0.01},
        "status": "active"
    }
    
    variant = {
        "id": "A",
        "title": "夏日肌肤保卫战",
        "description": "清爽补水，持久保湿，让肌肤水润一夏",
        "price": 199
    }
    
    print(f"智能体类型: {agent['persona_type']}")
    print(f"广告标题: {variant['title']}")
    print(f"广告价格: {variant['price']}元")
    print(f"智能体兴趣: {agent['interests']}")
    print()
    
    print("LLM服务状态:")
    print(f"  客户端: {llm_service.client}")
    print(f"  API Key: {'已配置' if llm_service.api_key else '未配置'}")
    print(f"  模型: {llm_service.model}")
    print()
    
    print("正在调用LLM决策...")
    result = await llm_service.generate_decision_with_reason(agent, variant)
    
    print("决策结果:")
    print(f"  决策: {result['decision']}")
    print(f"  思考过程: {result['thinking']}")
    print(f"  是否使用LLM: {result.get('used_llm', '未知')}")

if __name__ == "__main__":
    asyncio.run(test_llm_decision())