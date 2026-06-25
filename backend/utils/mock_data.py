PERSONA_TEMPLATES = [
    {"type": "price_sensitive", "name": "价格敏感型", "description": "对价格非常敏感，倾向于购买低价商品"},
    {"type": "impulse", "name": "冲动消费型", "description": "容易被促销活动吸引，购买决策快"},
    {"type": "brand_loyal", "name": "品牌忠诚型", "description": "对特定品牌有较高忠诚度"},
    {"type": "rational", "name": "理性决策型", "description": "购买前会仔细比较，决策较为理性"},
    {"type": "deal_seeker", "name": "优惠追寻型", "description": "喜欢寻找优惠券和促销活动"}
]

DEFAULT_BEHAVIOR = {
    "price_sensitive": {"click_rate": 0.03, "conversion_rate": 0.01, "brand_loyalty": 0.2, "impulsivity": 0.1},
    "impulse": {"click_rate": 0.08, "conversion_rate": 0.04, "brand_loyalty": 0.3, "impulsivity": 0.8},
    "brand_loyal": {"click_rate": 0.06, "conversion_rate": 0.05, "brand_loyalty": 0.9, "impulsivity": 0.2},
    "rational": {"click_rate": 0.04, "conversion_rate": 0.03, "brand_loyalty": 0.5, "impulsivity": 0.1},
    "deal_seeker": {"click_rate": 0.09, "conversion_rate": 0.06, "brand_loyalty": 0.1, "impulsivity": 0.5}
}