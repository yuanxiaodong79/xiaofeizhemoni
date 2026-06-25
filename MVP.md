﻿﻿﻿# 营销风洞智能体沙盘平台 - MVP设计文档

## 1. MVP目标

聚焦核心价值：**在虚拟环境中完成营销策略的快速验证**，打造一个"可运行的最小沙盘"。

## 2. MVP核心功能范围

### 2.1 功能模块裁剪

| 层级 | 完整功能 | MVP保留 | MVP说明 |
|-----|---------|--------|--------|
| **数据与基座层** | 真实数据湖、LLM网关、向量数据库 | 简化数据湖、本地LLM模拟 | 使用Mock数据，暂不接入真实LLM |
| **智能体工厂层** | 画像生成器、记忆管理、决策引擎、注册中心 | 简化画像生成、规则引擎决策 | 基于规则的决策，暂不用LLM |
| **模拟环境引擎层** | 推荐模拟器、时间调度器、交互总线 | 推荐模拟器、简单时间控制 | 简化调度逻辑 |
| **业务应用层** | A/B测试、受众洞察、生态评估 | 虚拟A/B测试工作台 | 聚焦核心使用场景 |
| **现实对齐层** | 差距分析器、智能体校准器 | 暂不实现 | MVP阶段暂不考虑 |

### 2.2 MVP核心功能清单

#### 2.2.1 智能体工厂（简化版）
- **Agent创建**：支持手动创建虚拟消费者
- **画像模板**：预设几种典型用户画像（价格敏感型、冲动消费型、品牌忠诚型）
- **简单记忆**：记录最近3次交互行为

#### 2.2.2 模拟环境引擎（简化版）
- **推荐算法**：随机推荐、热门推荐两种基线算法
- **时间控制**：按"轮次"推进模拟，每轮模拟一次曝光
- **交互总线**：同步消息分发机制

#### 2.2.3 虚拟A/B测试工作台
- **营销活动创建**：支持创建A/B测试活动
- **素材管理**：上传广告素材信息（标题、描述、价格）
- **模拟运行**：选择目标Agent群体，启动模拟
- **结果展示**：CTR、CVR指标计算与展示

## 3. MVP技术架构

### 3.1 技术栈（简化版）

| 层级 | 技术 | 版本 | 说明 |
|-----|------|-----|-----|
| 前端框架 | Vue.js | 3.x | 响应式开发 |
| 前端UI | Element Plus | 2.x | 快速构建界面 |
| 后端框架 | Node.js + Express | 4.x | 轻量快速 |
| 数据库 | PostgreSQL | 16.x | 关系型数据库 |
| 实时通信 | Socket.io | 4.x | 模拟进度推送 |

### 3.2 核心数据模型（简化版）

#### 3.2.1 Agent（智能体）模型
```json
{
  "id": "agent-uuid",
  "name": "虚拟用户001",
  "personaType": "price_sensitive",
  "demographics": {
    "age": 25,
    "gender": "female",
    "location": "一线城市"
  },
  "interests": ["美妆", "护肤"],
  "behaviorScore": {
    "clickRate": 0.05,
    "conversionRate": 0.02
  },
  "memory": ["最近点击了美妆广告"],
  "status": "active",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

#### 3.2.2 Campaign（营销活动）模型
```json
{
  "id": "campaign-uuid",
  "name": "测试活动A",
  "type": "ab_test",
  "variants": [
    { "id": "A", "title": "广告A", "price": 99 },
    { "id": "B", "title": "广告B", "price": 199 }
  ],
  "targetAudience": {"personaTypes": ["price_sensitive"]},
  "agentCount": 100,
  "status": "completed",
  "createdAt": "2024-01-01T00:00:00Z"
}
```

#### 3.2.3 SimulationResult（模拟结果）模型
```json
{
  "id": "result-uuid",
  "campaignId": "campaign-uuid",
  "variantResults": [
    { "variantId": "A", "impressions": 100, "clicks": 8, "conversions": 2 },
    { "variantId": "B", "impressions": 100, "clicks": 5, "conversions": 1 }
  ],
  "metrics": {
    "ctrA": 0.08, "cvrA": 0.02,
    "ctrB": 0.05, "cvrB": 0.01
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 4. MVP页面结构

### 4.1 页面清单

| 页面 | 路径 | 功能 |
|-----|-----|------|
| 仪表盘 | `/dashboard` | 核心指标概览 |
| Agent管理 | `/agents` | Agent列表与创建 |
| A/B测试 | `/ab-testing` | 创建活动、运行模拟、查看结果 |

### 4.2 页面详细设计

#### 4.2.1 仪表盘
- 总Agent数量统计
- 最近模拟活动列表
- 快捷入口（创建活动、查看结果）

#### 4.2.2 Agent管理
- Agent列表（支持分页）
- 创建Agent表单（选择画像类型、填写基本信息）
- 预设画像模板选择

#### 4.2.3 A/B测试工作台
- 活动创建表单
  - 活动名称
  - 添加多个变体（标题、描述、价格）
  - 选择目标受众类型
  - 设置参与Agent数量
- 模拟控制
  - 启动模拟按钮
  - 实时进度展示
- 结果展示
  - 各变体对比表格（曝光、点击、转化）
  - CTR/CVR计算与对比

## 5. MVP API接口设计

### 5.1 Agent接口

| API路径 | 方法 | 功能 |
|--------|-----|------|
| `/api/agents` | GET | 获取Agent列表 |
| `/api/agents` | POST | 创建Agent |
| `/api/agents/:id` | GET | 获取单个Agent |

### 5.2 Campaign接口

| API路径 | 方法 | 功能 |
|--------|-----|------|
| `/api/campaigns` | GET | 获取活动列表 |
| `/api/campaigns` | POST | 创建活动 |
| `/api/campaigns/:id` | GET | 获取活动详情 |
| `/api/campaigns/:id/start` | POST | 启动模拟 |
| `/api/campaigns/:id/results` | GET | 获取模拟结果 |

## 6. MVP决策引擎逻辑（规则简化版）

### 6.1 点击决策逻辑
```
点击概率 = base_click_rate 
          * (1 + price_factor) 
          * (1 + interest_factor) 
          * random_noise

price_factor: 价格越低，正向影响越大
interest_factor: 兴趣匹配度（0-1）
random_noise: 随机噪声（模拟非理性行为）
```

### 6.2 转化决策逻辑
```
转化概率 = base_conversion_rate 
          * (1 + price_factor) 
          * (1 + brand_factor)

brand_factor: 品牌忠诚度影响
```

## 7. MVP项目计划

| 阶段 | 时间 | 目标 |
|-----|-----|-----|
| 第一阶段 | 1周 | 后端基础架构 + 数据库设计 |
| 第二阶段 | 1周 | Agent管理 + 模拟引擎核心 |
| 第三阶段 | 1周 | 前端页面开发 |
| 第四阶段 | 1周 | 测试与部署 |

## 8. MVP成功标准

- 成功创建Agent并保存到数据库
- 成功创建A/B测试活动
- 运行模拟并生成结果
- 展示CTR/CVR对比数据
- 模拟进度实时推送

---

**文档版本**: v1.0  
**创建日期**: 2024年  
**状态**: MVP设计完成
