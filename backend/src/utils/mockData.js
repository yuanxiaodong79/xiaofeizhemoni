import { v4 as uuidv4 } from 'uuid';

export const personaTemplates = [
  { type: 'price_sensitive', name: '价格敏感型', description: '对价格非常敏感，倾向于购买低价商品' },
  { type: 'impulse', name: '冲动消费型', description: '容易被促销活动吸引，购买决策快' },
  { type: 'brand_loyal', name: '品牌忠诚型', description: '对特定品牌有较高忠诚度' },
  { type: 'rational', name: '理性决策型', description: '购买前会仔细比较，决策较为理性' },
  { type: 'deal_seeker', name: '优惠追寻型', description: '喜欢寻找优惠券和促销活动' }
];

export const defaultBehavior = {
  price_sensitive: { click_rate: 0.03, conversion_rate: 0.01, brand_loyalty: 0.2, impulsivity: 0.1 },
  impulse: { click_rate: 0.08, conversion_rate: 0.04, brand_loyalty: 0.3, impulsivity: 0.8 },
  brand_loyal: { click_rate: 0.06, conversion_rate: 0.05, brand_loyalty: 0.9, impulsivity: 0.2 },
  rational: { click_rate: 0.04, conversion_rate: 0.03, brand_loyalty: 0.5, impulsivity: 0.1 },
  deal_seeker: { click_rate: 0.09, conversion_rate: 0.06, brand_loyalty: 0.1, impulsivity: 0.5 }
};

export const mockAgents = [
  { id: 'agent-001', name: '虚拟用户001', personaType: 'price_sensitive', demographics: { age: 25, gender: 'female', location: '一线城市' }, interests: ['美妆', '护肤'], behaviorScore: { clickRate: 0.03, conversionRate: 0.01 }, memory: [], status: 'active', createdAt: '2024-01-01T00:00:00Z' },
  { id: 'agent-002', name: '虚拟用户002', personaType: 'impulse', demographics: { age: 22, gender: 'female', location: '二线城市' }, interests: ['服饰', '美食'], behaviorScore: { clickRate: 0.08, conversionRate: 0.04 }, memory: [], status: 'active', createdAt: '2024-01-01T00:00:00Z' },
  { id: 'agent-003', name: '虚拟用户003', personaType: 'brand_loyal', demographics: { age: 30, gender: 'male', location: '一线城市' }, interests: ['数码', '运动'], behaviorScore: { clickRate: 0.06, conversionRate: 0.05 }, memory: [], status: 'active', createdAt: '2024-01-01T00:00:00Z' },
  { id: 'agent-004', name: '虚拟用户004', personaType: 'rational', demographics: { age: 35, gender: 'female', location: '三线城市' }, interests: ['家居', '母婴'], behaviorScore: { clickRate: 0.04, conversionRate: 0.03 }, memory: [], status: 'active', createdAt: '2024-01-01T00:00:00Z' },
  { id: 'agent-005', name: '虚拟用户005', personaType: 'deal_seeker', demographics: { age: 28, gender: 'male', location: '二线城市' }, interests: ['游戏', '数码'], behaviorScore: { clickRate: 0.09, conversionRate: 0.06 }, memory: [], status: 'active', createdAt: '2024-01-01T00:00:00Z' },
  { id: 'agent-006', name: '虚拟用户006', personaType: 'price_sensitive', demographics: { age: 40, gender: 'female', location: '一线城市' }, interests: ['健康', '美妆'], behaviorScore: { clickRate: 0.03, conversionRate: 0.01 }, memory: [], status: 'active', createdAt: '2024-01-01T00:00:00Z' },
  { id: 'agent-007', name: '虚拟用户007', personaType: 'impulse', demographics: { age: 19, gender: 'male', location: '三线城市' }, interests: ['游戏', '服饰'], behaviorScore: { clickRate: 0.08, conversionRate: 0.04 }, memory: [], status: 'active', createdAt: '2024-01-01T00:00:00Z' },
  { id: 'agent-008', name: '虚拟用户008', personaType: 'brand_loyal', demographics: { age: 32, gender: 'female', location: '二线城市' }, interests: ['美妆', '时尚'], behaviorScore: { clickRate: 0.06, conversionRate: 0.05 }, memory: [], status: 'active', createdAt: '2024-01-01T00:00:00Z' },
  { id: 'agent-009', name: '虚拟用户009', personaType: 'rational', demographics: { age: 45, gender: 'male', location: '一线城市' }, interests: ['数码', '汽车'], behaviorScore: { clickRate: 0.04, conversionRate: 0.03 }, memory: [], status: 'active', createdAt: '2024-01-01T00:00:00Z' },
  { id: 'agent-010', name: '虚拟用户010', personaType: 'deal_seeker', demographics: { age: 26, gender: 'female', location: '二线城市' }, interests: ['美食', '旅游'], behaviorScore: { clickRate: 0.09, conversionRate: 0.06 }, memory: [], status: 'active', createdAt: '2024-01-01T00:00:00Z' }
];

export const mockCampaigns = [
  { id: 'campaign-001', name: '春季新品推广A/B测试', type: 'ab_test', variants: [{ id: 'A', title: '原价展示', description: '直接展示原价', price: 99 }, { id: 'B', title: '折扣优惠', description: '展示折扣价', price: 79 }], targetAudience: { personaTypes: ['price_sensitive', 'deal_seeker'] }, agentCount: 500, status: 'completed', createdAt: '2024-01-10T00:00:00Z' },
  { id: 'campaign-002', name: '会员专属活动测试', type: 'ab_test', variants: [{ id: 'A', title: '普通文案', description: '常规宣传文案', price: 199 }, { id: 'B', title: '个性化文案', description: '针对会员的个性化文案', price: 199 }], targetAudience: { personaTypes: ['brand_loyal'] }, agentCount: 300, status: 'completed', createdAt: '2024-01-08T00:00:00Z' },
  { id: 'campaign-003', name: '首页Banner测试', type: 'ab_test', variants: [{ id: 'A', title: '方案一', description: '红色主题Banner', price: 149 }, { id: 'B', title: '方案二', description: '蓝色主题Banner', price: 149 }], targetAudience: { personaTypes: ['all'] }, agentCount: 800, status: 'completed', createdAt: '2024-01-05T00:00:00Z' },
  { id: 'campaign-004', name: '促销文案测试', type: 'ab_test', variants: [{ id: 'A', title: '限时特惠', description: '限时促销文案', price: 69 }, { id: 'B', title: '限量抢购', description: '限量抢购文案', price: 69 }], targetAudience: { personaTypes: ['impulse'] }, agentCount: 400, status: 'running', createdAt: '2024-01-15T00:00:00Z' }
];

export const generateUUID = () => uuidv4();