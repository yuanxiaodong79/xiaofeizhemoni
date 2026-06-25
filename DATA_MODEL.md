# 营销风洞智能体沙盘平台 - MVP数据模型设计

## 1. 数据库整体架构

### 1.1 实体关系图（ERD）

```
┌──────────────────┐        ┌──────────────────┐        ┌──────────────────────┐
│     Agent        │        │    Campaign      │        │  SimulationResult    │
├──────────────────┤        ├──────────────────┤        ├──────────────────────┤
│ id (PK)          │        │ id (PK)          │        │ id (PK)              │
│ name             │        │ name             │        │ campaign_id (FK)     │
│ persona_type     │        │ type             │        │ variant_results (JSONB)│
│ demographics     │        │ variants (JSONB) │        │ metrics (JSONB)      │
│ interests        │        │ target_audience  │        │ timestamp            │
│ behavior_score   │        │ agent_count      │        └──────────────────────┘
│ memory           │        │ status           │
│ status           │        │ created_at       │
│ created_at       │        │ updated_at       │
└──────────────────┘        └──────────────────┘
                                    │
                                    │ 1:N
                                    ▼
                         ┌──────────────────┐
                         │   Variant        │
                         ├──────────────────┤
                         │ id (PK)          │
                         │ campaign_id (FK) │
                         │ title            │
                         │ description      │
                         │ price            │
                         └──────────────────┘
```

### 1.2 核心实体关系

| 关系 | 描述 | 基数 |
|-----|------|-----|
| Agent ↔ Campaign | Agent参与Campaign模拟 | N:N（通过SimulationResult关联） |
| Campaign ↔ Variant | Campaign包含多个变体 | 1:N |
| Campaign ↔ SimulationResult | Campaign产生模拟结果 | 1:1 |

---

## 2. 数据表设计

### 2.1 Agent（智能体）表

```sql
CREATE TABLE agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    persona_type VARCHAR(50) NOT NULL,  -- price_sensitive, impulse, brand_loyal
    demographics JSONB NOT NULL,
    interests TEXT[] NOT NULL,
    behavior_score JSONB NOT NULL,
    memory TEXT[],
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_agents_persona_type ON agents(persona_type);
CREATE INDEX idx_agents_status ON agents(status);
```

**字段说明**：

| 字段 | 类型 | 约束 | 说明 |
|-----|------|-----|-----|
| id | UUID | PK | 唯一标识 |
| name | VARCHAR(100) | NOT NULL | Agent名称 |
| persona_type | VARCHAR(50) | NOT NULL | 画像类型 |
| demographics | JSONB | NOT NULL | 人口统计学信息 |
| interests | TEXT[] | NOT NULL | 兴趣标签列表 |
| behavior_score | JSONB | NOT NULL | 行为评分（点击率、转化率基准） |
| memory | TEXT[] | NULL | 记忆列表（最近3次交互） |
| status | VARCHAR(20) | DEFAULT 'active' | 状态：active/inactive |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 更新时间 |

**persona_type枚举值**：

| 值 | 描述 |
|-----|-----|
| price_sensitive | 价格敏感型 |
| impulse | 冲动消费型 |
| brand_loyal | 品牌忠诚型 |
| rational | 理性决策型 |
| deal_seeker | 优惠追寻型 |

**demographics结构**：

```json
{
  "age": 25,
  "gender": "female",
  "location": "一线城市",
  "income": "中高收入",
  "occupation": "白领"
}
```

**behavior_score结构**：

```json
{
  "click_rate": 0.05,
  "conversion_rate": 0.02,
  "brand_loyalty": 0.7,
  "impulsivity": 0.3
}
```

---

### 2.2 Campaign（营销活动）表

```sql
CREATE TABLE campaigns (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50) NOT NULL,  -- ab_test, single, multi_variant
    variants JSONB NOT NULL,
    target_audience JSONB NOT NULL,
    agent_count INTEGER DEFAULT 1000,
    status VARCHAR(20) DEFAULT 'draft',  -- draft, running, completed, cancelled
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL
);

CREATE INDEX idx_campaigns_type ON campaigns(type);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_created_at ON campaigns(created_at);
```

**字段说明**：

| 字段 | 类型 | 约束 | 说明 |
|-----|------|-----|-----|
| id | UUID | PK | 唯一标识 |
| name | VARCHAR(200) | NOT NULL | 活动名称 |
| type | VARCHAR(50) | NOT NULL | 活动类型 |
| variants | JSONB | NOT NULL | 变体列表 |
| target_audience | JSONB | NOT NULL | 目标受众条件 |
| agent_count | INTEGER | DEFAULT 1000 | 参与Agent数量 |
| status | VARCHAR(20) | DEFAULT 'draft' | 活动状态 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 更新时间 |
| started_at | TIMESTAMP | NULL | 开始时间 |
| completed_at | TIMESTAMP | NULL | 完成时间 |

**type枚举值**：

| 值 | 描述 |
|-----|-----|
| ab_test | A/B测试 |
| single | 单版本测试 |
| multi_variant | 多变体测试 |

**status枚举值**：

| 值 | 描述 |
|-----|-----|
| draft | 草稿 |
| running | 运行中 |
| completed | 已完成 |
| cancelled | 已取消 |

**variants结构**：

```json
[
  {
    "id": "A",
    "title": "广告A",
    "description": "限时特惠",
    "price": 99,
    "image_url": "https://example.com/img/a.jpg"
  },
  {
    "id": "B",
    "title": "广告B",
    "description": "新品上市",
    "price": 199,
    "image_url": "https://example.com/img/b.jpg"
  }
]
```

**target_audience结构**：

```json
{
  "persona_types": ["price_sensitive", "impulse"],
  "age_range": [18, 35],
  "interests": ["美妆", "护肤"]
}
```

---

### 2.3 SimulationResult（模拟结果）表

```sql
CREATE TABLE simulation_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
    variant_results JSONB NOT NULL,
    metrics JSONB NOT NULL,
    summary TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_simulation_results_campaign_id ON simulation_results(campaign_id);
CREATE INDEX idx_simulation_results_timestamp ON simulation_results(timestamp);
```

**字段说明**：

| 字段 | 类型 | 约束 | 说明 |
|-----|------|-----|-----|
| id | UUID | PK | 唯一标识 |
| campaign_id | UUID | FK → campaigns | 关联活动ID |
| variant_results | JSONB | NOT NULL | 各变体结果 |
| metrics | JSONB | NOT NULL | 聚合指标 |
| summary | TEXT | NULL | 结果摘要 |
| timestamp | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 生成时间 |

**variant_results结构**：

```json
[
  {
    "variant_id": "A",
    "impressions": 1000,
    "clicks": 80,
    "conversions": 20,
    "revenue": 1980
  },
  {
    "variant_id": "B",
    "impressions": 1000,
    "clicks": 50,
    "conversions": 10,
    "revenue": 1990
  }
]
```

**metrics结构**：

```json
{
  "ctr_a": 0.08,
  "cvr_a": 0.02,
  "ctr_b": 0.05,
  "cvr_b": 0.01,
  "total_impressions": 2000,
  "total_clicks": 130,
  "total_conversions": 30,
  "best_variant": "A",
  "lift": {
    "ctr": 0.03,
    "cvr": 0.01
  }
}
```

---

### 2.4 物料表（可选）

```sql
CREATE TABLE materials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(200) NOT NULL,
    type VARCHAR(50) NOT NULL,  -- image, video, text
    content TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_materials_type ON materials(type);
```

---

## 3. 实体模型类定义

### 3.1 Agent 模型

```typescript
interface Demographics {
  age: number;
  gender: string;
  location: string;
  income?: string;
  occupation?: string;
}

interface BehaviorScore {
  click_rate: number;
  conversion_rate: number;
  brand_loyalty: number;
  impulsivity: number;
}

interface Agent {
  id: string;
  name: string;
  persona_type: 'price_sensitive' | 'impulse' | 'brand_loyal' | 'rational' | 'deal_seeker';
  demographics: Demographics;
  interests: string[];
  behavior_score: BehaviorScore;
  memory: string[];
  status: 'active' | 'inactive';
  created_at: Date;
  updated_at: Date;
}
```

### 3.2 Campaign 模型

```typescript
interface Variant {
  id: string;
  title: string;
  description?: string;
  price: number;
  image_url?: string;
}

interface TargetAudience {
  persona_types?: string[];
  age_range?: [number, number];
  interests?: string[];
}

interface Campaign {
  id: string;
  name: string;
  type: 'ab_test' | 'single' | 'multi_variant';
  variants: Variant[];
  target_audience: TargetAudience;
  agent_count: number;
  status: 'draft' | 'running' | 'completed' | 'cancelled';
  created_at: Date;
  updated_at: Date;
  started_at?: Date;
  completed_at?: Date;
}
```

### 3.3 SimulationResult 模型

```typescript
interface VariantResult {
  variant_id: string;
  impressions: number;
  clicks: number;
  conversions: number;
  revenue: number;
}

interface Metrics {
  ctr_a: number;
  cvr_a: number;
  ctr_b: number;
  cvr_b: number;
  total_impressions: number;
  total_clicks: number;
  total_conversions: number;
  best_variant: string;
  lift: {
    ctr: number;
    cvr: number;
  };
}

interface SimulationResult {
  id: string;
  campaign_id: string;
  variant_results: VariantResult[];
  metrics: Metrics;
  summary?: string;
  timestamp: Date;
}
```

---

## 4. 数据访问对象（DAO）接口

### 4.1 AgentDAO

| 方法 | 功能 | 参数 | 返回值 |
|-----|------|-----|-------|
| create | 创建Agent | Agent对象 | 创建的Agent |
| findById | 按ID查询 | id: string | Agent或null |
| findAll | 查询所有Agent | filters?: object | Agent列表 |
| findByPersonaType | 按画像类型查询 | persona_type: string | Agent列表 |
| update | 更新Agent | id: string, data: object | 更新后的Agent |
| delete | 删除Agent | id: string | 删除成功标识 |
| count | 统计Agent数量 | filters?: object | 数量 |

### 4.2 CampaignDAO

| 方法 | 功能 | 参数 | 返回值 |
|-----|------|-----|-------|
| create | 创建活动 | Campaign对象 | 创建的Campaign |
| findById | 按ID查询 | id: string | Campaign或null |
| findAll | 查询所有活动 | filters?: object | Campaign列表 |
| findByStatus | 按状态查询 | status: string | Campaign列表 |
| update | 更新活动 | id: string, data: object | 更新后的Campaign |
| delete | 删除活动 | id: string | 删除成功标识 |
| updateStatus | 更新状态 | id: string, status: string | 更新后的Campaign |

### 4.3 SimulationResultDAO

| 方法 | 功能 | 参数 | 返回值 |
|-----|------|-----|-------|
| create | 创建结果 | SimulationResult对象 | 创建的结果 |
| findByCampaignId | 按活动ID查询 | campaign_id: string | SimulationResult或null |
| findAll | 查询所有结果 | filters?: object | SimulationResult列表 |
| update | 更新结果 | id: string, data: object | 更新后的结果 |

---

## 5. 索引优化建议

### 5.1 查询场景分析

| 查询场景 | 频率 | 优化策略 |
|---------|-----|---------|
| 按persona_type筛选Agent | 高 | 复合索引 idx_agents_persona_type_status |
| 按状态筛选Campaign | 高 | 索引 idx_campaigns_status |
| 查询最近模拟结果 | 中 | 索引 idx_simulation_results_timestamp |
| 按活动ID查询结果 | 高 | 主键索引 + 外键索引 |

### 5.2 推荐索引

```sql
-- Agent表
CREATE INDEX idx_agents_persona_type_status ON agents(persona_type, status);

-- Campaign表
CREATE INDEX idx_campaigns_status_created_at ON campaigns(status, created_at DESC);

-- SimulationResult表
CREATE INDEX idx_simulation_results_campaign_id_timestamp ON simulation_results(campaign_id, timestamp DESC);
```

---

**文档版本**: v1.0  
**创建日期**: 2024年  
**状态**: 待评审
