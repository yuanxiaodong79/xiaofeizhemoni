import pool from '../config/database.js';
import simulationEngine from '../engine/simulationEngine.js';

export const getCampaigns = async (req, res) => {
  const { page = 1, pageSize = 10, status } = req.query;
  const offset = (page - 1) * pageSize;
  
  try {
    let query = 'SELECT * FROM campaigns';
    let countQuery = 'SELECT COUNT(*) FROM campaigns';
    let params = [];
    
    if (status) {
      query += ' WHERE status = $1';
      countQuery += ' WHERE status = $1';
      params.push(status);
    }
    
    query += ` ORDER BY created_at DESC LIMIT $${params.length + 1} OFFSET $${params.length + 2}`;
    params.push(pageSize, offset);
    
    const result = await pool.query(query, params);
    const countResult = await pool.query(countQuery, status ? [status] : []);
    
    const campaigns = result.rows.map(row => ({
      id: row.id,
      name: row.name,
      type: row.type,
      variants: row.variants,
      targetAudience: row.target_audience,
      agentCount: row.agent_count,
      status: row.status,
      createdAt: row.created_at.toISOString(),
      startedAt: row.started_at ? row.started_at.toISOString() : null,
      completedAt: row.completed_at ? row.completed_at.toISOString() : null
    }));
    
    res.json({
      data: campaigns,
      total: parseInt(countResult.rows[0].count),
      page: parseInt(page),
      pageSize: parseInt(pageSize)
    });
  } catch (error) {
    console.error('Error fetching campaigns:', error);
    res.status(500).json({ error: 'Failed to fetch campaigns' });
  }
};

export const getCampaign = async (req, res) => {
  const { id } = req.params;
  
  try {
    const result = await pool.query('SELECT * FROM campaigns WHERE id = $1', [id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Campaign not found' });
    }
    
    const row = result.rows[0];
    res.json({
      id: row.id,
      name: row.name,
      type: row.type,
      variants: row.variants,
      targetAudience: row.target_audience,
      agentCount: row.agent_count,
      status: row.status,
      createdAt: row.created_at.toISOString(),
      startedAt: row.started_at ? row.started_at.toISOString() : null,
      completedAt: row.completed_at ? row.completed_at.toISOString() : null
    });
  } catch (error) {
    console.error('Error fetching campaign:', error);
    res.status(500).json({ error: 'Failed to fetch campaign' });
  }
};

export const createCampaign = async (req, res) => {
  const { name, type = 'ab_test', variants, targetAudience, agentCount = 100 } = req.body;
  
  if (!name || !variants || variants.length < 2) {
    return res.status(400).json({ error: 'Name and at least 2 variants are required' });
  }
  
  try {
    const result = await pool.query(
      `INSERT INTO campaigns (name, type, variants, target_audience, agent_count, status)
       VALUES ($1, $2, $3, $4, $5, $6) RETURNING *`,
      [
        name,
        type,
        variants.map((v, i) => ({ id: v.id || String.fromCharCode(65 + i), ...v })),
        targetAudience || { personaTypes: ['all'] },
        agentCount,
        'draft'
      ]
    );
    
    const row = result.rows[0];
    res.status(201).json({
      id: row.id,
      name: row.name,
      type: row.type,
      variants: row.variants,
      targetAudience: row.target_audience,
      agentCount: row.agent_count,
      status: row.status,
      createdAt: row.created_at.toISOString()
    });
  } catch (error) {
    console.error('Error creating campaign:', error);
    res.status(500).json({ error: 'Failed to create campaign' });
  }
};

export const startSimulation = async (req, res) => {
  const { id } = req.params;
  
  try {
    const campaignResult = await pool.query('SELECT * FROM campaigns WHERE id = $1', [id]);
    
    if (campaignResult.rows.length === 0) {
      return res.status(404).json({ error: 'Campaign not found' });
    }
    
    const campaign = campaignResult.rows[0];
    
    if (campaign.status === 'running') {
      return res.status(400).json({ error: 'Campaign is already running' });
    }
    
    await pool.query(
      'UPDATE campaigns SET status = $1, started_at = CURRENT_TIMESTAMP WHERE id = $2',
      ['running', id]
    );
    
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const campaignData = {
      id: campaign.id,
      name: campaign.name,
      type: campaign.type,
      variants: campaign.variants,
      targetAudience: campaign.target_audience,
      agentCount: campaign.agent_count
    };
    
    const results = simulationEngine.runSimulation(campaignData);
    
    await pool.query(
      'UPDATE campaigns SET status = $1, completed_at = CURRENT_TIMESTAMP WHERE id = $2',
      ['completed', id]
    );
    
    const result = await pool.query(
      `INSERT INTO simulation_results (campaign_id, variant_results, metrics, summary)
       VALUES ($1, $2, $3, $4) RETURNING *`,
      [id, results.variantResults, results.metrics, results.summary]
    );
    
    const row = result.rows[0];
    res.json({
      id: row.id,
      campaignId: row.campaign_id,
      variantResults: row.variant_results,
      metrics: row.metrics,
      summary: row.summary,
      timestamp: row.timestamp.toISOString()
    });
  } catch (error) {
    console.error('Error starting simulation:', error);
    await pool.query('UPDATE campaigns SET status = $1 WHERE id = $2', ['failed', id]);
    res.status(500).json({ error: 'Simulation failed' });
  }
};

export const getSimulationResults = async (req, res) => {
  const { id } = req.params;
  
  try {
    const result = await pool.query('SELECT * FROM simulation_results WHERE campaign_id = $1 ORDER BY timestamp DESC', [id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'No results found for this campaign' });
    }
    
    const results = result.rows.map(row => ({
      id: row.id,
      campaignId: row.campaign_id,
      variantResults: row.variant_results,
      metrics: row.metrics,
      summary: row.summary,
      timestamp: row.timestamp.toISOString()
    }));
    
    res.json(results);
  } catch (error) {
    console.error('Error fetching simulation results:', error);
    res.status(500).json({ error: 'Failed to fetch simulation results' });
  }
};

export const getCampaignStats = async (req, res) => {
  try {
    const totalResult = await pool.query('SELECT COUNT(*) FROM campaigns');
    const runningResult = await pool.query('SELECT COUNT(*) FROM campaigns WHERE status = $1', ['running']);
    const completedResult = await pool.query('SELECT COUNT(*) FROM campaigns WHERE status = $1', ['completed']);
    const draftResult = await pool.query('SELECT COUNT(*) FROM campaigns WHERE status = $1', ['draft']);
    
    res.json({
      total: parseInt(totalResult.rows[0].count),
      running: parseInt(runningResult.rows[0].count),
      completed: parseInt(completedResult.rows[0].count),
      draft: parseInt(draftResult.rows[0].count)
    });
  } catch (error) {
    console.error('Error fetching campaign stats:', error);
    res.status(500).json({ error: 'Failed to fetch campaign stats' });
  }
};