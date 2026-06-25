import express from 'express';
import cors from 'cors';
import agentRoutes from './routes/agentRoutes.js';
import campaignRoutes from './routes/campaignRoutes.js';
import simulationEngine from './engine/simulationEngine.js';

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

app.use('/api/agents', agentRoutes);
app.use('/api/campaigns', campaignRoutes);

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', message: '营销风洞智能体沙盘平台后端服务正常运行' });
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Internal Server Error' });
});

const startServer = async () => {
  try {
    await simulationEngine.loadAgentsFromDB();
    console.log('智能体数据加载完成');
  } catch (error) {
    console.warn('启动时加载数据库失败，将使用Mock数据:', error.message);
  }
  
  app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
  });
};

startServer();