import requests
import json

print("=== 测试创建实验 ===")
create_response = requests.post(
    'http://localhost:3000/api/campaigns',
    headers={'Content-Type': 'application/json'},
    data=json.dumps({
        "name": "Price Sensitivity Test",
        "type": "ab_test",
        "variants": [
            {"id": "A", "title": "原价版", "description": "原价销售", "price": 199},
            {"id": "B", "title": "折扣版", "description": "限时优惠", "price": 139}
        ],
        "target_audience": {"persona_types": ["all"]},
        "agent_count": 100
    })
)

print(f"创建实验状态码: {create_response.status_code}")
if create_response.status_code == 201:
    campaign = create_response.json()
    print(f"创建成功! ID: {campaign['id']}")
    
    print("\n=== 测试启动模拟 ===")
    start_response = requests.post(f"http://localhost:3000/api/campaigns/{campaign['id']}/start?use_llm=true")
    print(f"启动模拟状态码: {start_response.status_code}")
    if start_response.status_code == 200:
        result = start_response.json()
        print("模拟成功!")
        print(f"变体结果: {json.dumps(result['variant_results'], indent=2, ensure_ascii=False)}")
        print(f"指标: {result['metrics']}")
        print(f"总结: {result['summary']}")
    else:
        print(f"启动失败: {start_response.text}")
else:
    print(f"创建失败: {create_response.text}")