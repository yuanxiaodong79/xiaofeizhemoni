import random
from config.database import get_db

MOCK_AGENTS = [
    {"id": "agent-001", "name": "虚拟用户001", "persona_type": "price_sensitive", "demographics": {"age": 25, "gender": "female", "location": "一线城市"}, "interests": ["美妆", "护肤"], "behavior_score": {"click_rate": 0.03, "conversion_rate": 0.01}, "status": "active"},
    {"id": "agent-002", "name": "虚拟用户002", "persona_type": "impulse", "demographics": {"age": 22, "gender": "female", "location": "二线城市"}, "interests": ["服饰", "美食"], "behavior_score": {"click_rate": 0.08, "conversion_rate": 0.04}, "status": "active"},
    {"id": "agent-003", "name": "虚拟用户003", "persona_type": "brand_loyal", "demographics": {"age": 30, "gender": "male", "location": "一线城市"}, "interests": ["数码", "运动"], "behavior_score": {"click_rate": 0.06, "conversion_rate": 0.05}, "status": "active"},
    {"id": "agent-004", "name": "虚拟用户004", "persona_type": "rational", "demographics": {"age": 35, "gender": "female", "location": "三线城市"}, "interests": ["家居", "母婴"], "behavior_score": {"click_rate": 0.04, "conversion_rate": 0.03}, "status": "active"},
    {"id": "agent-005", "name": "虚拟用户005", "persona_type": "deal_seeker", "demographics": {"age": 28, "gender": "male", "location": "二线城市"}, "interests": ["游戏", "数码"], "behavior_score": {"click_rate": 0.09, "conversion_rate": 0.06}, "status": "active"},
    {"id": "agent-006", "name": "虚拟用户006", "persona_type": "price_sensitive", "demographics": {"age": 40, "gender": "female", "location": "一线城市"}, "interests": ["健康", "美妆"], "behavior_score": {"click_rate": 0.03, "conversion_rate": 0.01}, "status": "active"},
    {"id": "agent-007", "name": "虚拟用户007", "persona_type": "impulse", "demographics": {"age": 19, "gender": "male", "location": "三线城市"}, "interests": ["游戏", "服饰"], "behavior_score": {"click_rate": 0.08, "conversion_rate": 0.04}, "status": "active"},
    {"id": "agent-008", "name": "虚拟用户008", "persona_type": "brand_loyal", "demographics": {"age": 32, "gender": "female", "location": "二线城市"}, "interests": ["美妆", "时尚"], "behavior_score": {"click_rate": 0.06, "conversion_rate": 0.05}, "status": "active"},
    {"id": "agent-009", "name": "虚拟用户009", "persona_type": "rational", "demographics": {"age": 45, "gender": "male", "location": "一线城市"}, "interests": ["数码", "汽车"], "behavior_score": {"click_rate": 0.04, "conversion_rate": 0.03}, "status": "active"},
    {"id": "agent-010", "name": "虚拟用户010", "persona_type": "deal_seeker", "demographics": {"age": 26, "gender": "female", "location": "二线城市"}, "interests": ["美食", "旅游"], "behavior_score": {"click_rate": 0.09, "conversion_rate": 0.06}, "status": "active"},
]

DEFAULT_BEHAVIOR = {
    "price_sensitive": {"click_rate": 0.03, "conversion_rate": 0.01, "brand_loyalty": 0.2, "impulsivity": 0.1},
    "impulse": {"click_rate": 0.08, "conversion_rate": 0.04, "brand_loyalty": 0.3, "impulsivity": 0.8},
    "brand_loyal": {"click_rate": 0.06, "conversion_rate": 0.05, "brand_loyalty": 0.9, "impulsivity": 0.2},
    "rational": {"click_rate": 0.04, "conversion_rate": 0.03, "brand_loyalty": 0.5, "impulsivity": 0.1},
    "deal_seeker": {"click_rate": 0.09, "conversion_rate": 0.06, "brand_loyalty": 0.1, "impulsivity": 0.5}
}


async def load_agents_from_db():
    try:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM agents WHERE status = 'active'")
            rows = cursor.fetchall()
            
            agents = []
            for row in rows:
                if isinstance(row, dict):
                    agents.append({
                        "id": str(row["id"]),
                        "name": row["name"],
                        "persona_type": row["persona_type"],
                        "demographics": row["demographics"],
                        "interests": row["interests"],
                        "behavior_score": row["behavior_score"],
                        "status": row["status"]
                    })
                else:
                    agents.append({
                        "id": str(row[0]),
                        "name": row[1],
                        "persona_type": row[2],
                        "demographics": row[3],
                        "interests": row[4],
                        "behavior_score": row[5],
                        "status": row[7]
                    })
            print(f"Loaded {len(agents)} agents from DB")
            return agents
    except Exception as e:
        print(f"Failed to load agents from DB: {str(e)}")
        return MOCK_AGENTS


def get_target_agents(persona_types, agents=None):
    source_agents = agents or MOCK_AGENTS
    
    if "all" in persona_types:
        return [a for a in source_agents if a.get("status") == "active"]
    return [a for a in source_agents if a.get("status") == "active" and a.get("persona_type") in persona_types]


def calculate_click_probability(agent, variant):
    behavior = agent.get("behavior_score") or DEFAULT_BEHAVIOR.get(agent.get("persona_type"), DEFAULT_BEHAVIOR["rational"])
    base_click_rate = behavior.get("click_rate", 0.05)
    
    avg_price = 100
    price = variant.get("price", 100) if isinstance(variant, dict) else getattr(variant, "price", 100)
    price_factor = 1 + (avg_price - price) / avg_price * 0.5
    
    interests = agent.get("interests", [])
    title = variant.get("title", "") if isinstance(variant, dict) else getattr(variant, "title", "")
    description = variant.get("description", "") if isinstance(variant, dict) else getattr(variant, "description", "")
    
    interest_match = any(
        i.lower() in title.lower() or i.lower() in description.lower()
        for i in interests
    )
    
    random_noise = 0.8 + random.random() * 0.4
    
    return base_click_rate * price_factor * (1 + (0.5 if interest_match else 0)) * random_noise


def calculate_conversion_probability(agent, variant):
    behavior = agent.get("behavior_score") or DEFAULT_BEHAVIOR.get(agent.get("persona_type"), DEFAULT_BEHAVIOR["rational"])
    base_conversion_rate = behavior.get("conversion_rate", 0.02)
    
    avg_price = 100
    price = variant.get("price", 100) if isinstance(variant, dict) else getattr(variant, "price", 100)
    price_factor = 1 + (avg_price - price) / avg_price * 0.3
    
    brand_factor = behavior.get("brand_loyalty", 0.5)
    
    return base_conversion_rate * price_factor * (1 + brand_factor)


async def run_simulation(campaign, agents=None, use_llm=False):
    target_agents = get_target_agents(campaign["target_audience"]["persona_types"], agents)
    sample_size = min(campaign["agent_count"], len(target_agents))
    sampled_agents = random.sample(target_agents, min(sample_size, len(target_agents)))
    
    impressions_per_variant = sample_size // len(campaign["variants"])
    
    results = [
        {
            "variant_id": v["id"],
            "impressions": impressions_per_variant,
            "clicks": 0,
            "conversions": 0,
            "rejection_reasons": []
        }
        for v in campaign["variants"]
    ]
    
    llm_service = None
    if use_llm:
        from services.llm_service import llm_service as llm
        llm_service = llm
    
    agent_index = 0
    for variant_index, variant in enumerate(campaign["variants"]):
        end_index = sample_size if variant_index == len(campaign["variants"]) - 1 else (variant_index + 1) * impressions_per_variant
        
        for i in range(agent_index, min(end_index, len(sampled_agents))):
            agent = sampled_agents[i]
            
            llm_client = getattr(llm_service, 'client', None) if llm_service else None
            
            if use_llm and llm_client:
                llm_decision = await llm_service.generate_decision_with_reason(agent, variant)
                llm_clicked = llm_decision["decision"] == "点击"
                
                persona_type = agent.get("persona_type", "rational")
                base_prob = {
                    "price_sensitive": 0.2,
                    "impulse": 0.7,
                    "brand_loyal": 0.4,
                    "rational": 0.5,
                    "deal_seeker": 0.6
                }.get(persona_type, 0.5)
                
                if llm_clicked:
                    final_prob = min(base_prob * 1.5, 1.0)
                else:
                    final_prob = base_prob * 0.3
                
                clicked = random.random() < final_prob
                
                if not clicked:
                    rejection_result = await llm_service.generate_rejection_reason(agent, variant)
                    results[variant_index]["rejection_reasons"].append({
                        "agent_id": agent["id"],
                        "reason": rejection_result.get("reason", ""),
                        "category": rejection_result.get("category", "other"),
                        "confidence": rejection_result.get("confidence", 0.0),
                        "thinking": llm_decision.get("thinking", ""),
                        "used_llm": rejection_result.get("used_llm", False)
                    })
            else:
                click_prob = calculate_click_probability(agent, variant)
                clicked = random.random() < click_prob
                
                if not clicked:
                    rejection_reasons = [
                        "价格太高", "不感兴趣", "预算不足", "已有同类产品", "不信任品牌"
                    ]
                    reason = rejection_reasons[random.randint(0, len(rejection_reasons)-1)]
                    results[variant_index]["rejection_reasons"].append({
                        "agent_id": agent["id"],
                        "reason": reason,
                        "category": "other",
                        "confidence": random.uniform(0.5, 0.9),
                        "thinking": "规则引擎决策",
                        "used_llm": False
                    })
            
            if clicked:
                results[variant_index]["clicks"] += 1
                
                if use_llm and llm_client:
                    conv_decision = await llm_service.generate_decision_with_reason(agent, variant, "convert")
                    llm_converted = conv_decision["decision"] == "转化"
                    
                    conversion_base_prob = {
                        "price_sensitive": 0.15,
                        "impulse": 0.5,
                        "brand_loyal": 0.35,
                        "rational": 0.4,
                        "deal_seeker": 0.45
                    }.get(persona_type, 0.4)
                    
                    if llm_converted:
                        conv_final_prob = min(conversion_base_prob * 1.5, 1.0)
                    else:
                        conv_final_prob = conversion_base_prob * 0.3
                    
                    converted = random.random() < conv_final_prob
                    
                    if not converted:
                        rejection_result = await llm_service.generate_rejection_reason(agent, variant)
                        results[variant_index]["rejection_reasons"].append({
                            "agent_id": agent["id"],
                            "reason": f"点击后未转化: {rejection_result.get('reason', '')}",
                            "category": rejection_result.get("category", "other"),
                            "confidence": rejection_result.get("confidence", 0.0),
                            "thinking": conv_decision.get("thinking", ""),
                            "used_llm": rejection_result.get("used_llm", False)
                        })
                else:
                    conversion_prob = calculate_conversion_probability(agent, variant)
                    converted = random.random() < conversion_prob
                    
                    if not converted:
                        conversion_reasons = [
                            "价格超出预期", "功能不符合需求", "竞品更优", "暂时不需要", "等待优惠"
                        ]
                        reason = conversion_reasons[random.randint(0, len(conversion_reasons)-1)]
                        results[variant_index]["rejection_reasons"].append({
                            "agent_id": agent["id"],
                            "reason": f"点击后未转化: {reason}",
                            "category": "conversion",
                            "confidence": random.uniform(0.5, 0.9),
                            "thinking": "规则引擎决策",
                            "used_llm": False
                        })
                    
                if converted:
                    results[variant_index]["conversions"] += 1
        
        agent_index = end_index
    
    metrics = {}
    for variant_index, variant in enumerate(campaign["variants"]):
        result = results[variant_index]
        ctr = (result["clicks"] / result["impressions"] * 100) if result["impressions"] > 0 else 0
        cvr = (result["conversions"] / result["clicks"] * 100) if result["clicks"] > 0 else 0
        
        metrics[f"ctr{variant['id']}"] = round(ctr, 2)
        metrics[f"cvr{variant['id']}"] = round(cvr, 2)
    
    return {
        "variant_results": results,
        "metrics": metrics,
        "summary": f"模拟完成：共{sample_size}个智能体参与，{len(campaign['variants'])}个变体",
        "used_llm": use_llm
    }