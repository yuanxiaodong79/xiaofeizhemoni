import requests
import json

print("=== 调试API调用流程 ===")

# 创建实验
create_response = requests.post(
    'http://localhost:3000/api/campaigns',
    headers={'Content-Type': 'application/json'},
    data=json.dumps({
        "name": "调试实验",
        "type": "ab_test",
        "variants": [
            {"id": "A", "title": "测试广告A", "description": "描述A", "price": 199},
            {"id": "B", "title": "测试广告B", "description": "描述B", "price": 139}
        ],
        "target_audience": {"persona_types": ["price_sensitive", "impulse", "deal_seeker"]},
        "agent_count": 200
    })
)

print(f"创建实验状态码: {create_response.status_code}")
if create_response.status_code == 201:
    campaign = create_response.json()
    print(f"创建的实验数据:")
    print(f"  id: {campaign['id']}")
    print(f"  variants: {campaign['variants']}")
    print(f"  target_audience: {campaign['target_audience']}")
    print(f"  type(variants): {type(campaign['variants'])}")
    print(f"  type(target_audience): {type(campaign['target_audience'])}")
    
    # 获取实验详情
    get_response = requests.get(f"http://localhost:3000/api/campaigns/{campaign['id']}")
    print(f"\n获取实验状态码: {get_response.status_code}")
    if get_response.status_code == 200:
        campaign_detail = get_response.json()
        print(f"从API获取的实验数据:")
        print(f"  variants: {campaign_detail['variants']}")
        print(f"  target_audience: {campaign_detail['target_audience']}")
        print(f"  type(variants): {type(campaign_detail['variants'])}")
        print(f"  type(target_audience): {type(campaign_detail['target_audience'])}")