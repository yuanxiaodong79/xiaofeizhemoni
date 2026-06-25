import pool from '../config/database.js';
import { mockAgents, defaultBehavior } from '../utils/mockData.js';

export class SimulationEngine {
  constructor() {
    this.agents = [...mockAgents];
  }

  async loadAgentsFromDB() {
    try {
      const result = await pool.query('SELECT * FROM agents WHERE status = $1', ['active']);
      this.agents = result.rows.map(row => ({
        id: row.id,
        name: row.name,
        personaType: row.persona_type,
        demographics: row.demographics,
        interests: row.interests,
        behaviorScore: row.behavior_score,
        memory: row.memory || [],
        status: row.status
      }));
    } catch (error) {
      console.warn('Failed to load agents from DB, using mock data:', error);
      this.agents = [...mockAgents];
    }
  }

  getTargetAgents(personaTypes, agents = null) {
    const sourceAgents = agents || this.agents;
    
    if (personaTypes.includes('all')) {
      return sourceAgents.filter(a => a.status === 'active');
    }
    return sourceAgents.filter(a => a.status === 'active' && personaTypes.includes(a.personaType));
  }

  calculateClickProbability(agent, variant) {
    const behavior = agent.behaviorScore || defaultBehavior[agent.personaType] || defaultBehavior.rational;
    const baseClickRate = behavior.click_rate || behavior.clickRate || 0.05;
    
    const avgPrice = 100;
    const priceFactor = 1 + (avgPrice - (variant.price || 100)) / avgPrice * 0.5;
    
    const interestMatch = agent.interests.some(i => 
      variant.title && variant.title.toLowerCase().includes(i) || 
      (variant.description && variant.description.toLowerCase().includes(i))
    ) ? 0.5 : 0;
    
    const randomNoise = 0.8 + Math.random() * 0.4;
    
    return baseClickRate * priceFactor * (1 + interestMatch) * randomNoise;
  }

  calculateConversionProbability(agent, variant) {
    const behavior = agent.behaviorScore || defaultBehavior[agent.personaType] || defaultBehavior.rational;
    const baseConversionRate = behavior.conversion_rate || behavior.conversionRate || 0.02;
    
    const avgPrice = 100;
    const priceFactor = 1 + (avgPrice - (variant.price || 100)) / avgPrice * 0.3;
    
    const brandFactor = behavior.brand_loyalty || 0.5;
    
    return baseConversionRate * priceFactor * (1 + brandFactor);
  }

  runSimulation(campaign, customAgents = null) {
    const targetAgents = this.getTargetAgents(campaign.targetAudience.personaTypes, customAgents);
    const sampleSize = Math.min(campaign.agentCount, targetAgents.length);
    const sampledAgents = targetAgents.sort(() => Math.random() - 0.5).slice(0, sampleSize);
    
    const impressionsPerVariant = Math.floor(sampleSize / campaign.variants.length);
    
    const results = campaign.variants.map(variant => ({
      variantId: variant.id,
      impressions: impressionsPerVariant,
      clicks: 0,
      conversions: 0
    }));

    let agentIndex = 0;
    campaign.variants.forEach((variant, variantIndex) => {
      const endIndex = variantIndex === campaign.variants.length - 1 
        ? sampleSize 
        : (variantIndex + 1) * impressionsPerVariant;
      
      for (let i = agentIndex; i < endIndex && i < sampledAgents.length; i++) {
        const agent = sampledAgents[i];
        
        const clickProb = this.calculateClickProbability(agent, variant);
        const clicked = Math.random() < clickProb;
        
        if (clicked) {
          results[variantIndex].clicks++;
          
          const conversionProb = this.calculateConversionProbability(agent, variant);
          const converted = Math.random() < conversionProb;
          
          if (converted) {
            results[variantIndex].conversions++;
          }
        }
      }
      agentIndex = endIndex;
    });

    const metrics = {};
    campaign.variants.forEach((variant, index) => {
      const result = results[index];
      const ctr = result.impressions > 0 ? (result.clicks / result.impressions * 100).toFixed(2) : '0';
      const cvr = result.clicks > 0 ? (result.conversions / result.clicks * 100).toFixed(2) : '0';
      
      metrics[`ctr${variant.id}`] = parseFloat(ctr);
      metrics[`cvr${variant.id}`] = parseFloat(cvr);
    });

    return {
      variantResults: results,
      metrics,
      summary: `模拟完成：共${sampleSize}个智能体参与，${campaign.variants.length}个变体`
    };
  }
}

export default new SimulationEngine();