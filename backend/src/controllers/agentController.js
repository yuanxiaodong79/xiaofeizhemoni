import pool from '../config/database.js';
import { personaTemplates, defaultBehavior } from '../utils/mockData.js';

export const getAgents = async (req, res) => {
  const { page = 1, pageSize = 10, personaType } = req.query;
  const offset = (page - 1) * pageSize;
  
  try {
    let query = `SELECT * FROM agents WHERE status = 'active'`;
    let countQuery = `SELECT COUNT(*) FROM agents WHERE status = 'active'`;
    let params = [];
    
    if (personaType) {
      query += ` AND persona_type = $1`;
      countQuery += ` AND persona_type = $1`;
      params.push(personaType);
    }
    
    query += ` ORDER BY created_at DESC LIMIT $${params.length + 1} OFFSET $${params.length + 2}`;
    params.push(pageSize, offset);
    
    const result = await pool.query(query, params);
    const countResult = await pool.query(countQuery, personaType ? [personaType] : []);
    
    const agents = result.rows.map(row => ({
      id: row.id,
      name: row.name,
      personaType: row.persona_type,
      demographics: row.demographics,
      interests: row.interests,
      behaviorScore: row.behavior_score,
      memory: row.memory || [],
      status: row.status,
      createdAt: row.created_at.toISOString()
    }));
    
    res.json({
      data: agents,
      total: parseInt(countResult.rows[0].count),
      page: parseInt(page),
      pageSize: parseInt(pageSize)
    });
  } catch (error) {
    console.error('Error fetching agents:', error);
    res.status(500).json({ error: 'Failed to fetch agents' });
  }
};

export const getAgent = async (req, res) => {
  const { id } = req.params;
  
  try {
    const result = await pool.query('SELECT * FROM agents WHERE id = $1', [id]);
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Agent not found' });
    }
    
    const row = result.rows[0];
    res.json({
      id: row.id,
      name: row.name,
      personaType: row.persona_type,
      demographics: row.demographics,
      interests: row.interests,
      behaviorScore: row.behavior_score,
      memory: row.memory || [],
      status: row.status,
      createdAt: row.created_at.toISOString()
    });
  } catch (error) {
    console.error('Error fetching agent:', error);
    res.status(500).json({ error: 'Failed to fetch agent' });
  }
};

export const createAgent = async (req, res) => {
  const { name, personaType, demographics, interests } = req.body;
  
  if (!name || !personaType) {
    return res.status(400).json({ error: 'Name and personaType are required' });
  }
  
  const behavior = defaultBehavior[personaType] || defaultBehavior.rational;
  
  try {
    const result = await pool.query(
      `INSERT INTO agents (name, persona_type, demographics, interests, behavior_score, memory, status)
       VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *`,
      [
        name,
        personaType,
        demographics || { age: 30, gender: 'male', location: '一线城市' },
        interests || ['购物'],
        { click_rate: behavior.click_rate, conversion_rate: behavior.conversion_rate, brand_loyalty: behavior.brand_loyalty, impulsivity: behavior.impulsivity },
        [],
        'active'
      ]
    );
    
    const row = result.rows[0];
    res.status(201).json({
      id: row.id,
      name: row.name,
      personaType: row.persona_type,
      demographics: row.demographics,
      interests: row.interests,
      behaviorScore: row.behavior_score,
      memory: row.memory,
      status: row.status,
      createdAt: row.created_at.toISOString()
    });
  } catch (error) {
    console.error('Error creating agent:', error);
    res.status(500).json({ error: 'Failed to create agent' });
  }
};

export const updateAgent = async (req, res) => {
  const { id } = req.params;
  const { name, personaType, demographics, interests, status } = req.body;
  
  try {
    const result = await pool.query(
      `UPDATE agents SET name = COALESCE($1, name), persona_type = COALESCE($2, persona_type),
                        demographics = COALESCE($3, demographics), interests = COALESCE($4, interests),
                        status = COALESCE($5, status), updated_at = CURRENT_TIMESTAMP
       WHERE id = $6 RETURNING *`,
      [name, personaType, demographics, interests, status, id]
    );
    
    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Agent not found' });
    }
    
    const row = result.rows[0];
    res.json({
      id: row.id,
      name: row.name,
      personaType: row.persona_type,
      demographics: row.demographics,
      interests: row.interests,
      behaviorScore: row.behavior_score,
      memory: row.memory,
      status: row.status,
      createdAt: row.created_at.toISOString(),
      updatedAt: row.updated_at.toISOString()
    });
  } catch (error) {
    console.error('Error updating agent:', error);
    res.status(500).json({ error: 'Failed to update agent' });
  }
};

export const deleteAgent = async (req, res) => {
  const { id } = req.params;
  
  try {
    const result = await pool.query('DELETE FROM agents WHERE id = $1', [id]);
    
    if (result.rowCount === 0) {
      return res.status(404).json({ error: 'Agent not found' });
    }
    
    res.status(204).send();
  } catch (error) {
    console.error('Error deleting agent:', error);
    res.status(500).json({ error: 'Failed to delete agent' });
  }
};

export const getPersonaTemplates = (req, res) => {
  res.json(personaTemplates);
};

export const getAgentStats = async (req, res) => {
  try {
    const totalResult = await pool.query('SELECT COUNT(*) FROM agents');
    const activeResult = await pool.query('SELECT COUNT(*) FROM agents WHERE status = $1', ['active']);
    const personaResult = await pool.query('SELECT persona_type, COUNT(*) as count FROM agents GROUP BY persona_type');
    
    const byPersona = {};
    personaResult.rows.forEach(row => {
      byPersona[row.persona_type] = parseInt(row.count);
    });
    
    res.json({
      total: parseInt(totalResult.rows[0].count),
      active: parseInt(activeResult.rows[0].count),
      byPersona
    });
  } catch (error) {
    console.error('Error fetching agent stats:', error);
    res.status(500).json({ error: 'Failed to fetch agent stats' });
  }
};