<template>
  <div class="dashboard">
    <div class="stats-row">
      <el-card class="stat-card">
        <div class="stat-icon users-icon">
          <el-icon><User /></el-icon>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ agentCount }}</p>
          <p class="stat-label">活跃智能体</p>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon campaign-icon">
          <el-icon><PieChart /></el-icon>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ campaignCount }}</p>
          <p class="stat-label">进行中实验</p>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon result-icon">
          <el-icon><ArrowUp /></el-icon>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ avgCtr }}%</p>
          <p class="stat-label">平均点击率</p>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon conversion-icon">
          <el-icon><ShoppingCart /></el-icon>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ conversionRate }}%</p>
          <p class="stat-label">转化率</p>
        </div>
      </el-card>
    </div>

    <div class="charts-row">
      <el-card class="chart-card">
        <template #header>
          <span>智能体画像分布</span>
        </template>
        <div class="persona-chart">
          <v-chart :option="personaChartOption" style="height: 250px;" />
        </div>
      </el-card>
      <el-card class="chart-card">
        <template #header>
          <span>最近实验记录</span>
        </template>
        <div class="recent-campaigns">
          <el-table :data="recentCampaigns" border :show-header="false">
            <el-table-column prop="name" label="实验名称" />
            <el-table-column prop="status" label="状态">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'completed' ? 'success' : 'warning'">
                  {{ scope.row.status === 'completed' ? '已完成' : '进行中' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="ctr" label="CTR">
              <template #default="scope">{{ scope.row.ctr }}%</template>
            </el-table-column>
            <el-table-column prop="date" label="时间" />
          </el-table>
        </div>
      </el-card>
    </div>

    <div class="quick-actions">
      <el-card>
        <template #header>
          <span>快捷操作</span>
        </template>
        <div class="action-buttons">
          <el-button type="primary" @click="goToCreateAgent">
            <el-icon><Plus /></el-icon>
            创建智能体
          </el-button>
          <el-button type="success" @click="goToCreateCampaign">
            <el-icon><Plus /></el-icon>
            创建实验
          </el-button>
          <el-button type="info" @click="goToResults">
            <el-icon><PieChart /></el-icon>
            查看结果
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { User, PieChart, ArrowUp, ShoppingCart, Plus } from '@element-plus/icons-vue';

const router = useRouter();

const agentCount = ref(0);
const campaignCount = ref(0);
const avgCtr = ref(0);
const conversionRate = ref(0);

const recentCampaigns = ref([
  { name: '春季新品推广A/B测试', status: 'completed', ctr: 8.5, date: '2024-01-15' },
  { name: '美妆素材赛马', status: 'completed', ctr: 6.2, date: '2024-01-14' },
  { name: '价格敏感度测试', status: 'running', ctr: 4.8, date: '2024-01-13' },
  { name: '品牌对比实验', status: 'completed', ctr: 10.1, date: '2024-01-12' }
]);

const personaChartOption = {
  tooltip: { trigger: 'item' },
  legend: { orient: 'horizontal', bottom: '0%' },
  series: [{
    name: '画像分布',
    type: 'pie',
    radius: ['40%', '70%'],
    avoidLabelOverlap: false,
    itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
    label: { show: true, formatter: '{b}: {c} ({d}%)' },
    data: [
      { value: 35, name: '价格敏感型', itemStyle: { color: '#5470c6' } },
      { value: 25, name: '冲动消费型', itemStyle: { color: '#91cc75' } },
      { value: 20, name: '品牌忠诚型', itemStyle: { color: '#fac858' } },
      { value: 15, name: '理性决策型', itemStyle: { color: '#ee6666' } },
      { value: 5, name: '优惠追逐型', itemStyle: { color: '#73c0de' } }
    ]
  }]
};

const goToCreateAgent = () => { router.push('/agents'); };
const goToCreateCampaign = () => { router.push('/ab-testing'); };
const goToResults = () => { router.push('/ab-testing'); };

onMounted(() => {
  agentCount.value = 100;
  campaignCount.value = 3;
  avgCtr.value = 7.8;
  conversionRate.value = 2.5;
});
</script>

<style scoped>
.dashboard { padding: 20px; }
.stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 20px; }
.stat-card { display: flex; align-items: center; gap: 15px; padding: 20px; }
.stat-icon { width: 50px; height: 50px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px; }
.users-icon { background: linear-gradient(135deg, #5470c6 0%, #83bff6 100%); color: #fff; }
.campaign-icon { background: linear-gradient(135deg, #91cc75 0%, #b3e5fc 100%); color: #fff; }
.result-icon { background: linear-gradient(135deg, #fac858 0%, #ff9966 100%); color: #fff; }
.conversion-icon { background: linear-gradient(135deg, #ee6666 0%, #ff9966 100%); color: #fff; }
.stat-info { flex: 1; }
.stat-value { font-size: 28px; font-weight: 600; color: #333; margin: 0; }
.stat-label { font-size: 14px; color: #999; margin: 5px 0 0; }
.charts-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.chart-card { height: 100%; }
.persona-chart { padding: 10px; }
.recent-campaigns { max-height: 250px; overflow-y: auto; }
.action-buttons { display: flex; gap: 15px; padding: 10px 0; }
</style>