import asyncio
import random
from services.simulation_engine import run_simulation, MOCK_AGENTS, get_target_agents

async def test_debug():
    print("=== 调试模拟引擎 ===")
    
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
    
    print("目标受众:", campaign["target_audience"]["persona_types"])
    target_agents = get_target_agents(campaign["target_audience"]["persona_types"], MOCK_AGENTS)
    print(f"符合条件的智能体数量: {len(target_agents)}")
    for agent in target_agents:
        print(f"  - {agent['name']}: {agent['persona_type']}")
    
    print("\n=== 测试规则引擎决策 ===")
    from services.simulation_engine import calculate_click_probability, calculate_conversion_probability
    
    for agent in target_agents[:3]:
        for variant in campaign["variants"]:
            click_prob = calculate_click_probability(agent, variant)
            conv_prob = calculate_conversion_probability(agent, variant)
            clicked = random.random() < click_prob
            converted = random.random() < conv_prob if clicked else False
            
            print(f"{agent['name']} ({agent['persona_type']})")
            print(f"  广告: {variant['id']} - {variant['title']}")
            print(f"  点击概率: {click_prob:.4f}, 实际点击: {clicked}")
            print(f"  转化概率: {conv_prob:.4f}, 实际转化: {converted}")
            print()

if __name__ == "__main__":
    asyncio.run(test_debug())