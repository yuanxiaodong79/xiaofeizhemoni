-- 营销风洞智能体沙盘平台 - 数据库初始化脚本
-- PostgreSQL 16.x

-- 创建数据库
-- CREATE DATABASE marketing_windtunnel;

-- 切换到数据库
-- \c marketing_windtunnel;

-- 1. Agent（智能体）表
CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    persona_type VARCHAR(50) NOT NULL,
    demographics JSONB NOT NULL,
    interests TEXT[] NOT NULL,
    behavior_score JSONB NOT NULL,
    memory TEXT[],
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent表索引
CREATE INDEX IF NOT EXISTS idx_agents_persona_type ON agents(persona_type);
CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
CREATE INDEX IF NOT EXISTS idx_agents_persona_type_status ON agents(persona_type, status);

-- 2. Campaign（营销活动）表
CREATE TABLE IF NOT EXISTS campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50) NOT NULL,
    variants JSONB NOT NULL,
    target_audience JSONB NOT NULL,
    agent_count INTEGER DEFAULT 1000,
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL
);

-- Campaign表索引
CREATE INDEX IF NOT EXISTS idx_campaigns_type ON campaigns(type);
CREATE INDEX IF NOT EXISTS idx_campaigns_status ON campaigns(status);
CREATE INDEX IF NOT EXISTS idx_campaigns_created_at ON campaigns(created_at);
CREATE INDEX IF NOT EXISTS idx_campaigns_status_created_at ON campaigns(status, created_at DESC);

-- 3. SimulationResult（模拟结果）表
CREATE TABLE IF NOT EXISTS simulation_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    variant_results JSONB NOT NULL,
    metrics JSONB NOT NULL,
    summary TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SimulationResult表索引
CREATE INDEX IF NOT EXISTS idx_simulation_results_campaign_id ON simulation_results(campaign_id);
CREATE INDEX IF NOT EXISTS idx_simulation_results_timestamp ON simulation_results(timestamp);
CREATE INDEX IF NOT EXISTS idx_simulation_results_campaign_id_timestamp ON simulation_results(campaign_id, timestamp DESC);

-- 4. Materials（物料）表
CREATE TABLE IF NOT EXISTS materials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50) NOT NULL,
    content TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Materials表索引
CREATE INDEX IF NOT EXISTS idx_materials_type ON materials(type);

-- 插入初始数据：画像类型配置
-- 创建配置表存储预设值
CREATE TABLE IF NOT EXISTS persona_templates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    default_behavior JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 插入预设画像模板
INSERT INTO persona_templates (type, name, description, default_behavior) VALUES
('price_sensitive', '价格敏感型', '对价格非常敏感，倾向于购买低价商品', '{"click_rate": 0.03, "conversion_rate": 0.01, "brand_loyalty": 0.2, "impulsivity": 0.1}'),
('impulse', '冲动消费型', '容易被促销活动吸引，购买决策快', '{"click_rate": 0.08, "conversion_rate": 0.04, "brand_loyalty": 0.3, "impulsivity": 0.8}'),
('brand_loyal', '品牌忠诚型', '对特定品牌有较高忠诚度', '{"click_rate": 0.06, "conversion_rate": 0.05, "brand_loyalty": 0.9, "impulsivity": 0.2}'),
('rational', '理性决策型', '购买前会仔细比较，决策较为理性', '{"click_rate": 0.04, "conversion_rate": 0.03, "brand_loyalty": 0.5, "impulsivity": 0.1}'),
('deal_seeker', '优惠追寻型', '喜欢寻找优惠券和促销活动', '{"click_rate": 0.09, "conversion_rate": 0.06, "brand_loyalty": 0.1, "impulsivity": 0.5}')
ON CONFLICT (type) DO NOTHING;

-- 插入示例Agent数据（10个）
INSERT INTO agents (name, persona_type, demographics, interests, behavior_score, memory) VALUES
('虚拟用户001', 'price_sensitive', '{"age": 25, "gender": "female", "location": "一线城市", "income": "中高收入", "occupation": "白领"}', '{"美妆", "护肤"}', '{"click_rate": 0.03, "conversion_rate": 0.01, "brand_loyalty": 0.2, "impulsivity": 0.1}', '{}'),
('虚拟用户002', 'impulse', '{"age": 22, "gender": "female", "location": "二线城市", "income": "中等收入", "occupation": "学生"}', '{"服饰", "美食"}', '{"click_rate": 0.08, "conversion_rate": 0.04, "brand_loyalty": 0.3, "impulsivity": 0.8}', '{}'),
('虚拟用户003', 'brand_loyal', '{"age": 30, "gender": "male", "location": "一线城市", "income": "高收入", "occupation": "经理"}', '{"数码", "运动"}', '{"click_rate": 0.06, "conversion_rate": 0.05, "brand_loyalty": 0.9, "impulsivity": 0.2}', '{}'),
('虚拟用户004', 'rational', '{"age": 35, "gender": "female", "location": "三线城市", "income": "中等收入", "occupation": "教师"}', '{"家居", "母婴"}', '{"click_rate": 0.04, "conversion_rate": 0.03, "brand_loyalty": 0.5, "impulsivity": 0.1}', '{}'),
('虚拟用户005', 'deal_seeker', '{"age": 28, "gender": "male", "location": "二线城市", "income": "中低收入", "occupation": "程序员"}', '{"游戏", "数码"}', '{"click_rate": 0.09, "conversion_rate": 0.06, "brand_loyalty": 0.1, "impulsivity": 0.5}', '{}'),
('虚拟用户006', 'price_sensitive', '{"age": 40, "gender": "female", "location": "一线城市", "income": "高收入", "occupation": "医生"}', '{"健康", "美妆"}', '{"click_rate": 0.03, "conversion_rate": 0.01, "brand_loyalty": 0.2, "impulsivity": 0.1}', '{}'),
('虚拟用户007', 'impulse', '{"age": 19, "gender": "male", "location": "三线城市", "income": "低收入", "occupation": "学生"}', '{"游戏", "服饰"}', '{"click_rate": 0.08, "conversion_rate": 0.04, "brand_loyalty": 0.3, "impulsivity": 0.8}', '{}'),
('虚拟用户008', 'brand_loyal', '{"age": 32, "gender": "female", "location": "二线城市", "income": "中高收入", "occupation": "设计师"}', '{"美妆", "时尚"}', '{"click_rate": 0.06, "conversion_rate": 0.05, "brand_loyalty": 0.9, "impulsivity": 0.2}', '{}'),
('虚拟用户009', 'rational', '{"age": 45, "gender": "male", "location": "一线城市", "income": "高收入", "occupation": "工程师"}', '{"数码", "汽车"}', '{"click_rate": 0.04, "conversion_rate": 0.03, "brand_loyalty": 0.5, "impulsivity": 0.1}', '{}'),
('虚拟用户010', 'deal_seeker', '{"age": 26, "gender": "female", "location": "二线城市", "income": "中等收入", "occupation": "销售"}', '{"美食", "旅游"}', '{"click_rate": 0.09, "conversion_rate": 0.06, "brand_loyalty": 0.1, "impulsivity": 0.5}', '{}')
ON CONFLICT DO NOTHING;

-- 创建视图：活动统计视图
CREATE VIEW IF NOT EXISTS campaign_stats AS
SELECT 
    c.id,
    c.name,
    c.type,
    c.status,
    c.agent_count,
    c.created_at,
    COALESCE(SUM(sr.metrics->>'total_impressions')::INT, 0) as total_impressions,
    COALESCE(SUM(sr.metrics->>'total_clicks')::INT, 0) as total_clicks,
    COALESCE(SUM(sr.metrics->>'total_conversions')::INT, 0) as total_conversions
FROM campaigns c
LEFT JOIN simulation_results sr ON c.id = sr.campaign_id
GROUP BY c.id, c.name, c.type, c.status, c.agent_count, c.created_at;

-- 创建视图：Agent画像分布
CREATE VIEW IF NOT EXISTS agent_persona_distribution AS
SELECT 
    persona_type,
    COUNT(*) as count,
    ROUND(COUNT(*)::FLOAT / (SELECT COUNT(*) FROM agents) * 100, 2) as percentage
FROM agents
WHERE status = 'active'
GROUP BY persona_type
ORDER BY count DESC;

-- 创建函数：计算CTR
CREATE OR REPLACE FUNCTION calculate_ctr(clicks INT, impressions INT) 
RETURNS NUMERIC AS $$
BEGIN
    IF impressions = 0 THEN
        RETURN 0;
    END IF;
    RETURN ROUND(clicks::FLOAT / impressions * 100, 2);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- 创建函数：计算CVR
CREATE OR REPLACE FUNCTION calculate_cvr(conversions INT, clicks INT) 
RETURNS NUMERIC AS $$
BEGIN
    IF clicks = 0 THEN
        RETURN 0;
    END IF;
    RETURN ROUND(conversions::FLOAT / clicks * 100, 2);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

COMMIT;

SELECT '数据库初始化完成' AS result;
