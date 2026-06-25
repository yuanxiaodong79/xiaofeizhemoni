import asyncio
from services.llm_service import llm_service

async def test_llm_response():
    print("=== 测试LLM实际响应 ===")
    
    # 确保LLM服务已初始化
    llm_service.initialize()
    
    print(f"LLM服务状态:")
    print(f"  client: {getattr(llm_service, 'client', None)}")
    print(f"  api_key: {'已设置' if getattr(llm_service, 'api_key', None) else '未设置'}")
    
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
    
    print(f"\n测试智能体: {agent['persona_type']}")
    print(f"测试广告: {variant['title']}")
    print(f"价格: {variant['price']}元")
    
    print("\n=== 测试LLM决策 ===")
    decisions = []
    for i in range(5):
        result = await llm_service.generate_decision_with_reason(agent, variant)
        decisions.append(result["decision"])
        print(f"测试 {i+1}: 决策={result['decision']}")
        if "thinking" in result and result["thinking"]:
            print(f"       思考: {result['thinking'][:50]}...")
    
    click_count = decisions.count("点击")
    print(f"\n点击次数: {click_count}/5 ({click_count/5*100}%)")

if __name__ == "__main__":
    asyncio.run(test_llm_response())