import asyncio
import random
from services.simulation_engine import MOCK_AGENTS, get_target_agents, calculate_click_probability

async def debug_persona_factor():
    print("=== 调试Persona Factor逻辑 ===")
    
    target_agents = get_target_agents(["price_sensitive", "impulse", "deal_seeker"], MOCK_AGENTS)
    
    print("测试画像因子概率:")
    for agent in target_agents:
        persona_type = agent.get("persona_type", "rational")
        persona_factor = {
            "price_sensitive": 0.2,
            "impulse": 0.9,
            "brand_loyal": 0.5,
            "rational": 0.6,
            "deal_seeker": 0.7
        }.get(persona_type, 0.6)
        
        print(f"\n{agent['name']} ({persona_type})")
        print(f"  画像因子: {persona_factor}")
        
        # 测试多次随机结果
        results = []
        for i in range(10):
            rand_val = random.random()
            clicked = rand_val < persona_factor
            results.append(clicked)
            print(f"  测试{i+1}: random={rand_val:.4f}, clicked={clicked}")
        
        click_count = sum(results)
        print(f"  点击次数: {click_count}/10 ({click_count/10*100}%)")

if __name__ == "__main__":
    asyncio.run(debug_persona_factor())