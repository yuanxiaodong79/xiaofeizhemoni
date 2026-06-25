import express from 'express';
import { getAgents, getAgent, createAgent, updateAgent, deleteAgent, getPersonaTemplates, getAgentStats } from '../controllers/agentController.js';

const router = express.Router();

router.get('/', getAgents);
router.get('/stats', getAgentStats);
router.get('/persona-templates', getPersonaTemplates);
router.get('/:id', getAgent);
router.post('/', createAgent);
router.put('/:id', updateAgent);
router.delete('/:id', deleteAgent);

export default router;