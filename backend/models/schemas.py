from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class Demographics(BaseModel):
    age: int = 30
    gender: str = "male"
    location: str = "一线城市"

class BehaviorScore(BaseModel):
    click_rate: float = 0.05
    conversion_rate: float = 0.02
    brand_loyalty: float = 0.5
    impulsivity: float = 0.3

class AgentBase(BaseModel):
    name: str
    persona_type: str
    demographics: Demographics = Demographics()
    interests: List[str] = []
    behavior_score: Optional[BehaviorScore] = None
    status: str = "active"

class AgentCreate(AgentBase):
    pass

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    persona_type: Optional[str] = None
    demographics: Optional[Demographics] = None
    interests: Optional[List[str]] = None
    status: Optional[str] = None

class AgentResponse(AgentBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    memory: List[str] = []

    class Config:
        from_attributes = True

class Variant(BaseModel):
    id: str = "A"
    title: str = ""
    description: str = ""
    price: float = 100

class TargetAudience(BaseModel):
    persona_types: List[str] = ["all"]

class CampaignBase(BaseModel):
    name: str
    type: str = "ab_test"
    variants: List[Variant] = []
    target_audience: TargetAudience = TargetAudience()
    agent_count: int = 100

class CampaignCreate(CampaignBase):
    pass

class CampaignResponse(CampaignBase):
    id: str
    status: str = "draft"
    created_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    variant_results: List["VariantResult"] = []
    metrics: Dict[str, float] = {}
    summary: Optional[str] = None

    class Config:
        from_attributes = True

class RejectionReason(BaseModel):
    agent_id: str
    reason: str
    category: str = "other"
    confidence: float = 0.0
    thinking: str = ""
    used_llm: bool = False

class VariantResult(BaseModel):
    variant_id: str
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    rejection_reasons: List[RejectionReason] = []

class SimulationMetrics(BaseModel):
    ctrA: Optional[float] = None
    cvrA: Optional[float] = None
    ctrB: Optional[float] = None
    cvrB: Optional[float] = None

class SimulationResultResponse(BaseModel):
    id: str
    campaign_id: str
    variant_results: List[VariantResult] = []
    metrics: Dict[str, float] = {}
    summary: str = ""
    timestamp: Optional[datetime] = None
    used_llm: bool = False

    class Config:
        from_attributes = True

class PersonaTemplate(BaseModel):
    type: str
    name: str
    description: str

class StatsResponse(BaseModel):
    total: int = 0
    active: int = 0
    by_persona: Dict[str, int] = {}

class CampaignStatsResponse(BaseModel):
    total: int = 0
    running: int = 0
    completed: int = 0
    draft: int = 0

class PaginatedResponse(BaseModel):
    data: List[Any] = []
    total: int = 0
    page: int = 1
    page_size: int = 10