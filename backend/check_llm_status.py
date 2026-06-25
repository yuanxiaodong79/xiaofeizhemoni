import asyncio
from services.llm_service import llm_service

async def check_status():
    print("=== 检查LLM服务状态 ===")
    
    # 检查属性是否存在
    print("属性检查:")
    print(f"  client属性存在: {'client' in dir(llm_service)}")
    print(f"  api_key属性存在: {'api_key' in dir(llm_service)}")
    print(f"  _initialized属性存在: {'_initialized' in dir(llm_service)}")
    
    # 获取实际值
    client = getattr(llm_service, 'client', None)
    api_key = getattr(llm_service, 'api_key', None)
    _initialized = getattr(llm_service, '_initialized', None)
    
    print(f"\n实际值:")
    print(f"  client: {client}")
    print(f"  api_key: {'已设置' if api_key else '未设置'}")
    print(f"  _initialized: {_initialized}")
    
    # 测试降级决策
    print("\n=== 测试降级决策 ===")
    agent = {
        "id": "test",
        "persona_type": "price_sensitive",
        "interests": ["美妆"],
        "behavior_score": {"click_rate": 0.03, "conversion_rate": 0.01}
    }
    
    variant = {"title": "测试广告", "description": "测试描述", "price": 100}
    
    results = []
    for i in range(10):
        decision = await llm_service.generate_decision_with_reason(agent, variant)
        results.append(decision["decision"])
    
    click_count = results.count("点击")
    print(f"10次测试结果: {results}")
    print(f"点击次数: {click_count}/10")
    print(f"点击率: {click_count/10*100}%")

if __name__ == "__main__":
    asyncio.run(check_status())