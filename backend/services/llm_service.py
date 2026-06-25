import os
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv
import json

load_dotenv()

class LLMService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def initialize(self):
        if self._initialized:
            return
        
        self.provider = os.getenv("LLM_PROVIDER", "deepseek").lower()
        self.api_key = os.getenv("LLM_API_KEY")
        self.model = os.getenv("LLM_MODEL")
        self.base_url = os.getenv("LLM_BASE_URL")
        
        if not self.api_key:
            print("LLM_API_KEY not set, LLM functionality will be disabled")
            self.client = None
            self._initialized = True
            return
        
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            http_client=self._create_http_client()
        )
        
        self._initialized = True
        print(f"LLM Service initialized with provider: {self.provider}")
    
    def _create_http_client(self):
        import httpx
        return httpx.AsyncClient(
            timeout=60.0,
            follow_redirects=True,
        )
    
    async def generate_behavior_score(self, agent_profile: dict) -> dict:
        """
        根据用户画像动态生成行为参数
        """
        if not self.client or not self.api_key:
            return self._get_fallback_behavior(agent_profile)
        
        try:
            prompt = self._build_prompt(agent_profile)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个专业的消费者行为分析师。请根据用户画像，精确预测其消费行为参数。输出必须是纯JSON格式，不要包含其他解释文字。"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            try:
                result = json.loads(content)
                return result
            except json.JSONDecodeError:
                print(f"LLM response parse error: {content}")
                return self._get_fallback_behavior(agent_profile)
                
        except Exception as e:
            print(f"LLM API error: {str(e)}")
            return self._get_fallback_behavior(agent_profile)
    
    def _build_prompt(self, profile: dict) -> str:
        """
        构建Prompt
        """
        demographics = profile.get("demographics", {})
        interests = profile.get("interests", [])
        persona_type = profile.get("persona_type", "unknown")
        
        return f"""
请根据以下用户画像，生成该用户的行为参数。输出JSON格式，不要添加任何额外解释。

用户画像：
- 画像类型：{persona_type}
- 年龄：{demographics.get('age', 30)}
- 性别：{demographics.get('gender', 'unknown')}
- 城市：{demographics.get('location', 'unknown')}
- 收入：{demographics.get('income', 'unknown')}
- 职业：{demographics.get('occupation', 'unknown')}
- 兴趣：{', '.join(interests) if interests else '无'}

输出格式：
{{
    "behavior_score": {{
        "click_rate": 0.05,
        "conversion_rate": 0.02,
        "brand_loyalty": 0.5,
        "impulsivity": 0.3,
        "price_sensitivity": 0.7,
        "ad_fatigue": 0.2
    }}
}}
"""
    
    def _get_fallback_behavior(self, profile: dict) -> dict:
        """
        LLM不可用时的降级行为参数
        """
        from utils.mock_data import DEFAULT_BEHAVIOR
        
        persona_type = profile.get("persona_type", "rational")
        default = DEFAULT_BEHAVIOR.get(persona_type, DEFAULT_BEHAVIOR["rational"])
        
        return {
            "behavior_score": {
                "click_rate": default.get("click_rate", 0.05),
                "conversion_rate": default.get("conversion_rate", 0.02),
                "brand_loyalty": default.get("brand_loyalty", 0.5),
                "impulsivity": default.get("impulsivity", 0.3),
                "price_sensitivity": 0.7,
                "ad_fatigue": 0.2
            }
        }
    
    async def generate_decision(self, agent, ad_content: str) -> str:
        """
        生成智能体决策（点击/不点击）
        """
        client = getattr(self, 'client', None)
        if not client or not self.api_key:
            return "不点击"
        
        try:
            persona_type = agent.get("persona_type", "unknown")
            interests = agent.get("interests", [])
            
            prompt = f"""
你是一个{persona_type}类型的消费者。
你的兴趣：{', '.join(interests)}

现在看到以下广告：
{ad_content}

你会点击这个广告吗？请回答"点击"或"不点击"。
"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个真实的消费者，请根据广告内容和你的性格做出决策。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=10
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"LLM decision error: {str(e)}")
            return "不点击"
    
    async def generate_decision_with_reason(self, agent, variant: dict, decision_type: str = "click") -> dict:
        """
        使用LLM进行决策推理（含CoT思维链）
        decision_type: "click" 点击决策, "convert" 转化决策
        返回决策结果和推理过程
        """
        client = getattr(self, 'client', None)
        if not client or not self.api_key:
            return self._get_fallback_decision(agent, variant, decision_type)
        
        try:
            persona_type = agent.get("persona_type", "unknown")
            interests = agent.get("interests", [])
            demographics = agent.get("demographics", {})
            
            age = demographics.get("age", "未知")
            gender = demographics.get("gender", "未知")
            location = demographics.get("location", "未知")
            
            persona_desc = {
                "price_sensitive": "价格敏感型：对价格极其敏感，超过100元的商品通常不会点击，即使非常感兴趣也会因为价格过高而放弃点击，购买决策更加谨慎",
                "impulse": "冲动消费型：容易被营销刺激打动，看到感兴趣的商品就会立即点击，不太考虑价格，容易冲动购买",
                "brand_loyal": "品牌忠诚型：只购买特定品牌的产品，对其他品牌的广告不会点击，更愿意为信任的品牌付费",
                "rational": "理性决策型：会仔细分析产品参数和性价比，只有确实需要且价格合理才会点击，购买决策需要充分理由",
                "deal_seeker": "优惠追逐型：热衷于寻找优惠券和折扣信息，没有看到明确折扣信息就不会点击，有优惠时更容易下单"
            }.get(persona_type, "普通消费者：根据兴趣和价格综合判断")
            
            action_click = "点击这个广告" if decision_type == "click" else "购买这个产品"
            action_yes = "点击" if decision_type == "click" else "转化"
            action_no = "不点击" if decision_type == "click" else "不转化"
            
            prompt = f"""
你是一个虚拟消费者，以下是你的个人信息：
- 画像类型：{persona_type}（{persona_desc}）
- 年龄：{age}
- 性别：{gender}
- 城市：{location}
- 兴趣爱好：{', '.join(interests) if interests else '无'}

现在你看到一个广告：
标题：{variant.get('title', '')}
描述：{variant.get('description', '')}
价格：{variant.get('price', 0)}元

请根据你的画像类型特点，按照以下格式输出你的决策和思考过程：

思考过程：
1. 分析广告内容是否符合我的兴趣
2. 考虑价格是否符合我的消费习惯
3. 根据我的画像类型特点做出判断

最终决策：{action_yes}/{action_no}
"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": f"你是一个真实的消费者，必须严格按照你的画像类型做出决策。价格敏感型用户应该经常因为价格高而拒绝。优惠追逐型用户只在有折扣时才{action_yes}。理性决策型用户需要综合考虑性价比。"
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.4,
                max_tokens=500
            )
            
            content = response.choices[0].message.content.strip()
            
            return self._parse_decision_response(content, decision_type)
            
        except Exception as e:
            print(f"LLM decision with reason error: {str(e)}")
            return self._get_fallback_decision(agent, variant, decision_type)
    
    async def generate_rejection_reason(self, agent, variant: dict) -> dict:
        """
        阶段三：生成拒绝理由（CoT思维链）
        当用户不点击或不转化时，生成详细的拒绝原因
        返回JSON结构化输出
        """
        client = getattr(self, 'client', None)
        if not client or not self.api_key:
            reason = self._get_fallback_rejection_reason(agent, variant)
            return {
                "reason": reason,
                "category": self._classify_rejection_reason(reason),
                "confidence": 0.8,
                "used_llm": False
            }
        
        try:
            persona_type = agent.get("persona_type", "unknown")
            interests = agent.get("interests", [])
            demographics = agent.get("demographics", {})
            
            prompt = f"""
你是一个{persona_type}类型的消费者。
你的兴趣：{', '.join(interests)}

你看到了一个广告但决定不点击/不购买：
广告标题：{variant.get('title', '')}
广告描述：{variant.get('description', '')}
价格：{variant.get('price', 0)}元

请输出JSON格式的拒绝理由分析，包含以下字段：
- reason: 拒绝的具体原因（自然语言描述）
- category: 拒绝原因分类（可选值：price, interest, brand, timing, need, quality, other）
- confidence: 置信度（0-1）

输出示例：
{{
    "reason": "价格太高了，超出我的预算",
    "category": "price",
    "confidence": 0.9
}}
"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": "你是一个真实的消费者分析专家。请严格按照JSON格式输出拒绝理由分析，不要添加任何额外解释文字。"
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            content = response.choices[0].message.content.strip()
            
            try:
                result = json.loads(content)
                return {
                    "reason": result.get("reason", ""),
                    "category": result.get("category", "other"),
                    "confidence": result.get("confidence", 0.8),
                    "used_llm": True
                }
            except json.JSONDecodeError:
                print(f"LLM rejection reason parse error: {content}")
                reason = self._get_fallback_rejection_reason(agent, variant)
                return {
                    "reason": reason,
                    "category": self._classify_rejection_reason(reason),
                    "confidence": 0.7,
                    "used_llm": False
                }
            
        except Exception as e:
            print(f"LLM rejection reason error: {str(e)}")
            reason = self._get_fallback_rejection_reason(agent, variant)
            return {
                "reason": reason,
                "category": self._classify_rejection_reason(reason),
                "confidence": 0.7,
                "used_llm": False
            }
    
    def _classify_rejection_reason(self, reason: str) -> str:
        """
        分类拒绝理由
        """
        reason_lower = reason.lower()
        if any(word in reason_lower for word in ["价格", "贵", "便宜", "预算", "钱"]):
            return "price"
        elif any(word in reason_lower for word in ["兴趣", "喜欢", "感兴趣", "符合", "需求"]):
            return "interest"
        elif any(word in reason_lower for word in ["品牌", "牌子", "信任"]):
            return "brand"
        elif any(word in reason_lower for word in ["现在", "暂时", "等待", "以后"]):
            return "timing"
        elif any(word in reason_lower for word in ["需要", "用", "需求"]):
            return "need"
        elif any(word in reason_lower for word in ["质量", "品质", "好", "差"]):
            return "quality"
        else:
            return "other"
    
    def _parse_decision_response(self, content: str, decision_type: str = "click") -> dict:
        """
        解析LLM决策响应
        """
        thinking = ""
        decision = "不点击" if decision_type == "click" else "不转化"
        
        action_yes = "点击" if decision_type == "click" else "转化"
        action_no = "不点击" if decision_type == "click" else "不转化"
        
        lines = content.split('\n')
        in_thinking = False
        
        for line in lines:
            if "思考过程" in line or "思考" in line:
                in_thinking = True
                continue
            if "最终决策" in line:
                in_thinking = False
                if action_yes in line and action_no not in line:
                    decision = action_yes
                elif action_no in line:
                    decision = action_no
                elif action_yes in line:
                    decision = action_yes
                continue
            if in_thinking:
                thinking += line.strip() + " "
        
        if not thinking:
            thinking = "根据广告内容和个人特征做出决策"
        
        return {
            "decision": decision,
            "thinking": thinking.strip(),
            "used_llm": True
        }
    
    def _get_fallback_decision(self, agent, variant, decision_type: str = "click") -> dict:
        """
        LLM不可用时的降级决策
        """
        from utils.mock_data import DEFAULT_BEHAVIOR
        
        persona_type = agent.get("persona_type", "rational")
        behavior = DEFAULT_BEHAVIOR.get(persona_type, DEFAULT_BEHAVIOR["rational"])
        
        if decision_type == "click":
            rate = behavior.get("click_rate", 0.05)
            action_yes = "点击"
            action_no = "不点击"
        else:
            rate = behavior.get("conversion_rate", 0.02)
            action_yes = "转化"
            action_no = "不转化"
        
        import random
        decision = action_yes if random.random() < rate else action_no
        
        return {
            "decision": decision,
            "thinking": f"使用规则引擎决策，{persona_type}类型用户基础{action_yes}率{rate}",
            "used_llm": False
        }
    
    def _get_fallback_rejection_reason(self, agent, variant) -> str:
        """
        LLM不可用时的降级拒绝理由
        """
        persona_type = agent.get("persona_type", "rational")
        
        reasons = {
            "price_sensitive": "价格太高了，超出我的预算",
            "impulse": "虽然有点兴趣，但现在不需要",
            "brand_loyal": "这个品牌不是我喜欢的",
            "rational": "经过考虑，这个产品不符合我的需求",
            "deal_seeker": "没有折扣优惠，再等等看"
        }
        
        return reasons.get(persona_type, "暂时不需要")

llm_service = LLMService()
