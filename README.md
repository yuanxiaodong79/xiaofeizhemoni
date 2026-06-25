# 营销风洞智能体沙盘平台 - Python后端

基于FastAPI的现代化后端服务

## 技术栈

- **语言**: Python 3.8+
- **框架**: FastAPI
- **数据库**: PostgreSQL 16.x
- **LLM**: DeepSeek / Qwen（通过OpenAI兼容API）

## 项目结构

```
backend/
├── main.py                    # FastAPI主入口
├── requirements.txt            # Python依赖
├── .env                        # 环境变量配置
├── start.bat                   # Windows启动脚本
├── config/
│   ├── database.py            # 数据库连接配置
│   └── __init__.py
├── models/
│   ├── schemas.py             # Pydantic数据模型
│   └── __init__.py
├── routers/
│   ├── agents.py              # 智能体API路由
│   ├── campaigns.py           # 营销活动API路由
│   └── __init__.py
├── services/
│   ├── simulation_engine.py   # 模拟引擎
│   ├── llm_service.py         # LLM服务（支持DeepSeek/Qwen）
│   └── __init__.py
└── utils/
    ├── mock_data.py           # Mock数据
    └── __init__.py
```

## 快速开始

### 1. 安装Python依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

编辑 `.env` 文件：

```ini
# 数据库配置
DB_HOST=localhost
DB_PORT=5432
DB_NAME=marketing_windtunnel
DB_USER=postgres
DB_PASSWORD=your_password

# LLM配置 - DeepSeek示例
LLM_PROVIDER=deepseek
LLM_API_KEY=your-deepseek-api-key
LLM_MODEL=deepseek-chat
LLM_BASE_URL=https://api.deepseek.com/v1

# LLM配置 - Qwen示例（取消注释使用）
# LLM_PROVIDER=qwen
# LLM_API_KEY=your-qwen-api-key
# LLM_MODEL=qwen-plus
# LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 3. 初始化数据库

```bash
psql -U postgres -d marketing_windtunnel -f src/config/init.sql
```

### 4. 启动服务

```bash
python main.py
```

## API文档

启动服务后访问：
- Swagger UI: http://localhost:3000/docs
- ReDoc: http://localhost:3000/redoc

## API接口

### 智能体接口

| 路径 | 方法 | 功能 |
|------|------|------|
| `/api/agents` | GET | 获取智能体列表 |
| `/api/agents` | POST | 创建智能体 |
| `/api/agents/{id}` | GET | 获取单个智能体 |
| `/api/agents/{id}` | PUT | 更新智能体 |
| `/api/agents/{id}` | DELETE | 删除智能体 |
| `/api/agents/stats` | GET | 获取统计信息 |
| `/api/agents/persona-templates` | GET | 获取画像模板 |

### 营销活动接口

| 路径 | 方法 | 功能 |
|------|------|------|
| `/api/campaigns` | GET | 获取活动列表 |
| `/api/campaigns` | POST | 创建活动 |
| `/api/campaigns/{id}` | GET | 获取活动详情 |
| `/api/campaigns/{id}/start` | POST | 启动模拟 |
| `/api/campaigns/{id}/results` | GET | 获取模拟结果 |
| `/api/campaigns/stats` | GET | 获取统计信息 |

### LLM状态接口

| 路径 | 方法 | 功能 |
|------|------|------|
| `/api/llm/status` | GET | 获取LLM服务状态 |

## LLM配置说明

### DeepSeek配置

```ini
LLM_PROVIDER=deepseek
LLM_API_KEY=sk-xxx
LLM_MODEL=deepseek-chat
LLM_BASE_URL=https://api.deepseek.com/v1
```

### Qwen配置

```ini
LLM_PROVIDER=qwen
LLM_API_KEY=your-qwen-api-key
LLM_MODEL=qwen-plus
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

### 阶段一：使用LLM生成行为参数

创建智能体时添加 `use_llm=true` 参数：

```bash
curl -X POST "http://localhost:3000/api/agents?use_llm=true" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "虚拟用户",
    "persona_type": "price_sensitive",
    "demographics": {"age": 25, "gender": "female", "location": "一线城市"},
    "interests": ["美妆", "护肤"]
  }'
```

### 阶段二：LLM决策推理（CoT思维链）

启动模拟时添加 `use_llm=true` 参数，使用LLM进行决策推理：

```bash
curl -X POST "http://localhost:3000/api/campaigns/{campaign_id}/start?use_llm=true"
```

LLM会模拟消费者思考过程：
1. 分析广告内容是否符合兴趣
2. 考虑价格是否在预算范围内
3. 综合判断是否应该点击/转化

### 阶段三：LLM生成拒绝理由

当智能体不点击或不转化时，LLM会生成详细的拒绝原因：

```json
{
  "rejection_reasons": [
    {
      "agent_id": "agent-001",
      "reason": "价格太高了，超出我的预算",
      "thinking": "我是价格敏感型消费者，这个产品价格超过了我的心理价位"
    }
  ]
}
```

### 降级机制

当LLM服务不可用时（如API Key未配置），系统会自动降级到预设的行为参数模板和规则引擎。

## 启动脚本

- `start.bat` - Windows启动脚本

## 环境要求

- Python 3.8+
- PostgreSQL 16.x
- Windows/Linux/macOS
