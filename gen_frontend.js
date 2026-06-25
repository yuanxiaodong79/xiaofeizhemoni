const fs = require('fs');

const ensureDir = (path) => {
  if (!fs.existsSync(path)) {
    fs.mkdirSync(path, { recursive: true });
  }
};

ensureDir('./frontend/src/views');
ensureDir('./frontend/src/components');
ensureDir('./frontend/src/router');
ensureDir('./frontend/src/api');
ensureDir('./frontend/src/store');
ensureDir('./frontend/src/utils');

const dashboardVue = `<template>
  <div class="dashboard">
    <div class="stats-row">
      <el-card class="stat-card">
        <div class="stat-icon users-icon"><el-icon><Users /></el-icon></div>
        <div class="stat-info"><p class="stat-value">{{ agentCount }}</p><p class="stat-label">总Agent数量</p></div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon campaign-icon"><el-icon><BarChart /></el-icon></div>
        <div class="stat-info"><p class="stat-value">{{ campaignCount }}</p><p class="stat-label">营销活动</p></div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon result-icon"><el-icon><TrendingUp /></el-icon></div>
        <div class="stat-info"><p class="stat-value">{{ avgCtr }}%</p><p class="stat-label">平均CTR</p></div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon conversion-icon"><el-icon><ShoppingCart /></el-icon></div>
        <div class="stat-info"><p class="stat-value">{{ avgCvr }}%</p><p class="stat-label">平均CVR</p></div>
      </el-card>
    </div>
    <div class="content-row">
      <el-card title="最近活动">
        <el-table :data="recentCampaigns" border>
          <el-table-column prop="name" label="活动名称" />
          <el-table-column prop="type" label="类型" />
          <el-table-column prop="status" label="状态" />
          <el-table-column prop="createdAt" label="创建时间" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" @click="viewCampaign(scope.row)">查看</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
      <el-card title="画像分布">
        <div class="persona-chart">
          <div v-for="item in personaDistribution" :key="item.type" class="persona-item">
            <div class="persona-bar"><div class="persona-fill" :style="{ width: item.percentage + '%' }"></div></div>
            <div class="persona-info"><span class="persona-name">{{ item.name }}</span><span class="persona-count">{{ item.count }} ({{ item.percentage }}%)</span></div>
          </div>
        </div>
      </el-card>
    </div>
    <div class="quick-actions">
      <el-card title="快捷操作">
        <el-row :gutter="20">
          <el-col :span="8"><el-button type="primary" @click="goToAgents"><el-icon><Plus /></el-icon>创建Agent</el-button></el-col>
          <el-col :span="8"><el-button type="success" @click="goToABTesting"><el-icon><PlayCircle /></el-icon>开始A/B测试</el-button></el-col>
        </el-row>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { Users, BarChart, TrendingUp, ShoppingCart, Plus, PlayCircle } from '@element-plus/icons-vue';
import { agentApi, campaignApi } from '../api';
import { personaTypeMap, formatDate } from '../utils';

const router = useRouter();
const agentCount = ref(0);
const campaignCount = ref(0);
const avgCtr = ref('5.2');
const avgCvr = ref('2.1');
const recentCampaigns = ref([]);
const personaDistribution = ref([]);

onMounted(async () => {
  try {
    const [agentsRes, campaignsRes] = await Promise.all([agentApi.list(), campaignApi.list({ limit: 5 })]);
    agentCount.value = agentsRes.total || 0;
    recentCampaigns.value = campaignsRes.data?.map(c => ({ ...c, createdAt: formatDate(c.created_at) })) || [];
    campaignCount.value = campaignsRes.total || 0;
    
    const personaCounts = {};
    agentsRes.data?.forEach(a => { personaCounts[a.persona_type] = (personaCounts[a.persona_type] || 0) + 1; });
    const total = Object.values(personaCounts).reduce((a, b) => a + b, 0);
    personaDistribution.value = Object.entries(personaCounts).map(([type, count]) => ({
      type, name: personaTypeMap[type] || type, count,
      percentage: total > 0 ? ((count / total) * 100).toFixed(1) : 0
    }));
  } catch (error) { console.error('Failed to load dashboard data:', error); }
});

const viewCampaign = (campaign) => { router.push('/ab-testing'); };
const goToAgents = () => router.push('/agents');
const goToABTesting = () => router.push('/ab-testing');
</script>

<style scoped>
.dashboard { padding: 20px; }
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 20px; }
.stat-card { display: flex; align-items: center; gap: 15px; padding: 20px; }
.stat-icon { width: 50px; height: 50px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.users-icon { background: #e6f7ff; color: #1890ff; }
.campaign-icon { background: #f6ffed; color: #52c41a; }
.result-icon { background: #fff7e6; color: #fa8c16; }
.conversion-icon { background: #f9f0ff; color: #722ed1; }
.stat-value { font-size: 24px; font-weight: 600; color: #333; margin: 0; }
.stat-label { font-size: 14px; color: #999; margin: 5px 0 0; }
.content-row { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; margin-bottom: 20px; }
.persona-chart { display: flex; flex-direction: column; gap: 10px; }
.persona-item { display: flex; flex-direction: column; gap: 5px; }
.persona-bar { height: 20px; background: #f0f0f0; border-radius: 10px; overflow: hidden; }
.persona-fill { height: 100%; background: linear-gradient(90deg, #1890ff, #69c0ff); }
.persona-info { display: flex; justify-content: space-between; font-size: 13px; }
.persona-name { color: #666; }
.persona-count { color: #999; }
.quick-actions { margin-top: 20px; }
</style>
`;

fs.writeFileSync('./frontend/src/views/Dashboard.vue', dashboardVue);
console.log('Dashboard.vue created');
