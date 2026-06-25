import asyncio
import random
from services.simulation_engine import run_simulation, MOCK_AGENTS, get_target_agents, calculate_click_probability

async def test_simulation_debug():
    print("=== 调试完整模拟流程 ===")
    
    campaign = {
        "id": "test-123",
        "name": "测试实验",
        "type": "ab_test",
        "variants": [
            {
                "id": "A",
                "title": "夏日肌肤保卫战",
                "description": "清爽补水，持久保湿，让肌肤水润一夏",
                "price": 199
            },
            {
                "id": "B",
                "title": "限时特惠！夏日护肤套装",
                "description": "买一送一，限时7折，错过等一年",
                "price": 139
            }
        ],
        "target_audience": {
            "persona_types": ["price_sensitive", "impulse", "deal_seeker"]
        },
        "agent_count": 200,
        "status": "draft"
    }
    
    print("\n=== 手动模拟单个智能体 ===")
    
    target_agents = get_target_agents(campaign["target_audience"]["persona_types"], MOCK_AGENTS)
    
    for agent in target_agents:
        print(f"\n智能体: {agent['name']} ({agent['persona_type']})")
        for variant in campaign["variants"]:
            click_prob = calculate_click_probability(agent, variant)
            clicked = random.random() < click_prob
            print(f"  广告 {variant['id']}: 点击概率={click_prob:.4f}, 点击={clicked}")
    
    print("\n=== 调用run_simulation ===")
    
    # 添加调试信息到模拟引擎
    result = await run_simulation(campaign, agents=MOCK_AGENTS, use_llm=True)
    
    print("\n模拟结果:")
    for res in result["variant_results"]:
        print(f"变体 {res['variant_id']}: 曝光={res['impressions']}, 点击={res['clicks']}, 转化={res['conversions']}")
    
    print(f"\n使用LLM: {result['used_llm']}")

if __name__ == "__main__":
    asyncio.run(test_simulation_debug())