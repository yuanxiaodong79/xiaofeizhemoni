import express from 'express';
import { getCampaigns, getCampaign, createCampaign, startSimulation, getSimulationResults, getCampaignStats } from '../controllers/campaignController.js';

const router = express.Router();

router.get('/', getCampaigns);
router.get('/stats', getCampaignStats);
router.get('/:id', getCampaign);
router.get('/:id/results', getSimulationResults);
router.post('/', createCampaign);
router.post('/:id/start', startSimulation);

export default router;