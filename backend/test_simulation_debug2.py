import asyncio
import random
from services.simulation_engine import run_simulation, MOCK_AGENTS, get_target_agents, calculate_click_probability

async def test_simulation_debug2():
    print("=== 调试模拟引擎内部逻辑 ===")
    
    # 模拟从数据库读取的数据格式（字符串）
    import json
    campaign_str = {
        "id": "test-123",
        "name": "测试实验",
        "type": "ab_test",
        "variants": json.dumps([
            {"id": "A", "title": "夏日肌肤保卫战", "description": "清爽补水", "price": 199},
            {"id": "B", "title": "限时特惠", "description": "买一送一", "price": 139}
        ]),
        "target_audience": json.dumps({"persona_types": ["price_sensitive", "impulse", "deal_seeker"]}),
        "agent_count": 200,
        "status": "draft"
    }
    
    print("原始数据（字符串格式）:")
    print(f"  variants: {campaign_str['variants']}")
    print(f"  type: {type(campaign_str['variants'])}")
    
    # 解析JSON
    campaign_data = {
        "id": campaign_str["id"],
        "name": campaign_str["name"],
        "type": campaign_str["type"],
        "variants": json.loads(campaign_str["variants"]),
        "target_audience": json.loads(campaign_str["target_audience"]),
        "agent_count": campaign_str["agent_count"]
    }
    
    print("\n解析后数据（对象格式）:")
    print(f"  variants: {campaign_data['variants']}")
    print(f"  type: {type(campaign_data['variants'])}")
    
    # 测试计算点击概率
    print("\n=== 测试点击概率计算 ===")
    target_agents = get_target_agents(campaign_data["target_audience"]["persona_types"], MOCK_AGENTS)
    
    for agent in target_agents[:2]:
        for variant in campaign_data["variants"]:
            click_prob = calculate_click_probability(agent, variant)
            print(f"{agent['name']} 对 {variant['id']}: 点击概率={click_prob:.4f}")
    
    # 测试模拟
    print("\n=== 测试模拟 ===")
    result = await run_simulation(campaign_data, agents=MOCK_AGENTS, use_llm=True)
    
    print("\n模拟结果:")
    for res in result["variant_results"]:
        print(f"变体 {res['variant_id']}: 曝光={res['impressions']}, 点击={res['clicks']}, 转化={res['conversions']}")

if __name__ == "__main__":
    asyncio.run(test_simulation_debug2())