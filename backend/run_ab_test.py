import requests
import json

print("=== 夏季护肤品推广A/B测试 ===")
print("=" * 50)

# 创建实验
create_response = requests.post(
    'http://localhost:3000/api/campaigns',
    headers={'Content-Type': 'application/json'},
    data=json.dumps({
        "name": "夏季护肤品推广A/B测试",
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
        "agent_count": 200
    })
)

if create_response.status_code == 201:
    campaign = create_response.json()
    print(f"✅ 实验创建成功!")
    print(f"   ID: {campaign['id']}")
    print(f"   名称: {campaign['name']}")
    print(f"   状态: {campaign['status']}")
    
    print("\n=== 启动LLM模拟 ===")
    print("目标受众: 价格敏感型、冲动消费型、优惠追逐型")
    print(f"样本数量: 200个智能体")
    print("使用LLM决策推理: ✅")
    print("\n正在运行模拟...")
    
    start_response = requests.post(f"http://localhost:3000/api/campaigns/{campaign['id']}/start?use_llm=true")
    
    if start_response.status_code == 200:
        result = start_response.json()
        
        print("\n✅ 模拟完成!")
        print("=" * 50)
        
        # 计算总计
        total_impressions = sum(v["impressions"] for v in result["variant_results"])
        total_clicks = sum(v["clicks"] for v in result["variant_results"])
        total_conversions = sum(v["conversions"] for v in result["variant_results"])
        
        print(f"\n📊 总体数据:")
        print(f"   总曝光: {total_impressions}")
        print(f"   总点击: {total_clicks}")
        print(f"   总转化: {total_conversions}")
        print(f"   整体CTR: {(total_clicks / total_impressions * 100):.2f}%")
        print(f"   整体CVR: {(total_conversions / total_clicks * 100):.2f}%")
        
        print("\n📈 变体对比:")
        print("-" * 50)
        
        for v in result["variant_results"]:
            ctr = (v["clicks"] / v["impressions"] * 100) if v["impressions"] > 0 else 0
            cvr = (v["conversions"] / v["clicks"] * 100) if v["clicks"] > 0 else 0
            
            print(f"\n   变体 {v['variant_id']}:")
            variant_info = "原价版" if v["variant_id"] == "A" else "折扣版"
            print(f"   类型: {variant_info}")
            print(f"   曝光: {v['impressions']}")
            print(f"   点击: {v['clicks']}")
            print(f"   转化: {v['conversions']}")
            print(f"   CTR: {ctr:.2f}%")
            print(f"   CVR: {cvr:.2f}%")
        
        print("\n🏆 结果分析:")
        variant_a = result["variant_results"][0]
        variant_b = result["variant_results"][1]
        
        a_ctr = (variant_a["clicks"] / variant_a["impressions"] * 100) if variant_a["impressions"] > 0 else 0
        b_ctr = (variant_b["clicks"] / variant_b["impressions"] * 100) if variant_b["impressions"] > 0 else 0
        
        if a_ctr > b_ctr:
            print(f"   变体A (原价版)表现更好，CTR比变体B高 {(a_ctr - b_ctr):.2f}个百分点")
        else:
            print(f"   变体B (折扣版)表现更好，CTR比变体A高 {(b_ctr - a_ctr):.2f}个百分点")
        
        print(f"\n📝 总结: {result['summary']}")
        print(f"🔧 使用LLM: {'是' if result.get('used_llm') else '否'}")
        
    else:
        print(f"❌ 启动模拟失败: {start_response.text}")
else:
    print(f"❌ 创建实验失败: {create_response.text}")