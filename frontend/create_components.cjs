const fs = require('fs');

const headerContent = `
<template>
  <header class="header">
    <div class="header-left">
      <span class="title">{{ pageTitle }}</span>
    </div>
    <div class="header-right">
      <el-button type="primary" @click="handleRefresh">
        <el-icon><Refresh /></el-icon>
        刷新
      </el-button>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { Refresh } from '@element-plus/icons-vue';

const router = useRouter();

const pageTitle = computed(() => {
  const titles = {
    '/dashboard': '仪表盘',
    '/agents': 'Agent管理',
    '/ab-testing': '虚拟A/B测试工作台'
  };
  return titles[router.currentRoute.value.path] || '营销风洞';
});

const handleRefresh = () => {
  router.go(0);
};
</script>

<style scoped>
.header { height: 60px; background: #fff; border-bottom: 1px solid #e8e8e8; display: flex; justify-content: space-between; align-items: center; padding: 0 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.header-left .title { font-size: 18px; font-weight: 600; color: #333; }
.header-right { display: flex; align-items: center; gap: 10px; }
</style>
`.trim();

const sidebarContent = `
<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h2>营销风洞</h2>
      <p class="subtitle">智能体沙盘平台</p>
    </div>
    <el-menu :default-active="activeMenu" mode="vertical" @select="handleSelect">
      <el-menu-item index="/dashboard">
        <el-icon><Dashboard /></el-icon>
        <span>仪表盘</span>
      </el-menu-item>
      <el-menu-item index="/agents">
        <el-icon><Users /></el-icon>
        <span>Agent管理</span>
      </el-menu-item>
      <el-menu-item index="/ab-testing">
        <el-icon><BarChart /></el-icon>
        <span>A/B测试</span>
      </el-menu-item>
    </el-menu>
  </aside>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { Dashboard, Users, BarChart } from '@element-plus/icons-vue';

const router = useRouter();
const activeMenu = ref('/dashboard');

watch(() => router.currentRoute.value.path, (newPath) => {
  activeMenu.value = newPath;
});

const handleSelect = (index) => {
  router.push(index);
};
</script>

<style scoped>
.sidebar { width: 220px; background: #001529; color: #fff; display: flex; flex-direction: column; }
.sidebar-header { padding: 20px; border-bottom: 1px solid #1890ff; }
.sidebar-header h2 { font-size: 18px; margin: 0; color: #1890ff; }
.sidebar-header .subtitle { font-size: 12px; color: #8c8c8c; margin-top: 5px; }
:deep(.el-menu) { border-right: none; background: transparent; }
:deep(.el-menu-item) { color: rgba(255,255,255,0.7); }
:deep(.el-menu-item:hover) { background: rgba(255,255,255,0.1); }
:deep(.el-menu-item.is-active) { background: #1890ff; color: #fff; }
</style>
`.trim();

const appContent = `
<template>
  <div class="app-container">
    <Sidebar />
    <div class="main-content">
      <Header />
      <div class="content-wrapper">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import Sidebar from './components/Sidebar.vue';
import Header from './components/Header.vue';
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
.app-container { display: flex; height: 100vh; overflow: hidden; }
.main-content { flex: 1; display: flex; flex-direction: column; background: #f5f7fa; }
.content-wrapper { flex: 1; padding: 20px; overflow-y: auto; }
</style>
`.trim();

const dashboardContent = `
<template>
  <div class="dashboard">
    <div class="stats-row">
      <el-card class="stat-card">
        <div class="stat-icon users-icon">
          <el-icon><Users /></el-icon>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ agentCount }}</p>
          <p class="stat-label">活跃智能体</p>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon campaign-icon">
          <el-icon><BarChart /></el-icon>
        </div>
        <div class="stat-info">
          <p class="stat-value">{{ campaignCount }}</p>
          <p class="stat-label">进行中实验</p>
        </div>
      </el-card>
      <el-card class="stat-card">
        <div class="stat-icon result-icon">
          <el-icon><TrendingUp /></el-icon>
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
          <el-chart :option="personaChartOption" style="height: 250px;" />
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
            <el-icon><UserPlus /></el-icon>
            创建智能体
          </el-button>
          <el-button type="success" @click="goToCreateCampaign">
            <el-icon><Plus /></el-icon>
            创建实验
          </el-button>
          <el-button type="info" @click="goToResults">
            <el-icon><BarChart /></el-icon>
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
import { Users, BarChart, TrendingUp, ShoppingCart, UserPlus, Plus } from '@element-plus/icons-vue';

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
`.trim();

const agentsContent = `
<template>
  <div class="agents-page">
    <div class="page-header">
      <h2>智能体管理</h2>
      <el-button type="primary" @click="showCreateModal = true">
        <el-icon><Plus /></el-icon>
        创建智能体
      </el-button>
    </div>

    <el-card>
      <div class="filter-bar">
        <el-select v-model="filterPersona" placeholder="选择画像类型" class="filter-select">
          <el-option label="全部" value="" />
          <el-option label="价格敏感型" value="price_sensitive" />
          <el-option label="冲动消费型" value="impulse" />
          <el-option label="品牌忠诚型" value="brand_loyal" />
          <el-option label="理性决策型" value="rational" />
          <el-option label="优惠追逐型" value="deal_seeker" />
        </el-select>
        <el-input v-model="searchQuery" placeholder="搜索智能体名称" class="search-input" />
      </div>

      <el-table :data="filteredAgents" border>
        <el-table-column prop="id" label="ID" width="120" />
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="persona_type" label="画像类型">
          <template #default="scope">
            <el-tag :type="getPersonaType(scope.row.persona_type)">
              {{ getPersonaLabel(scope.row.persona_type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="demographics" label="年龄">
          <template #default="scope">{{ scope.row.demographics?.age || '-' }}</template>
        </el-table-column>
        <el-table-column prop="demographics" label="性别">
          <template #default="scope">{{ scope.row.demographics?.gender || '-' }}</template>
        </el-table-column>
        <el-table-column prop="interests" label="兴趣">
          <template #default="scope">{{ (scope.row.interests || []).join(', ') }}</template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'active' ? 'success' : 'warning'">
              {{ scope.row.status === 'active' ? '活跃' : '停用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" />
        <el-table-column label="操作">
          <template #default="scope">
            <el-button size="small" @click="viewAgent(scope.row)">查看</el-button>
            <el-button size="small" type="danger" @click="deleteAgent(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination 
        :current-page="currentPage" 
        :page-size="pageSize" 
        :total="total"
        @current-change="handlePageChange"
        layout="total, prev, pager, next"
      />
    </el-card>

    <el-dialog title="创建智能体" v-model="showCreateModal" width="500px">
      <el-form :model="newAgent" label-width="100px">
        <el-form-item label="名称">
          <el-input v-model="newAgent.name" placeholder="请输入智能体名称" />
        </el-form-item>
        <el-form-item label="画像类型">
          <el-select v-model="newAgent.persona_type" placeholder="请选择画像类型">
            <el-option label="价格敏感型" value="price_sensitive" />
            <el-option label="冲动消费型" value="impulse" />
            <el-option label="品牌忠诚型" value="brand_loyal" />
            <el-option label="理性决策型" value="rational" />
            <el-option label="优惠追逐型" value="deal_seeker" />
          </el-select>
        </el-form-item>
        <el-form-item label="年龄">
          <el-input type="number" v-model="newAgent.demographics.age" placeholder="请输入年龄" />
        </el-form-item>
        <el-form-item label="性别">
          <el-select v-model="newAgent.demographics.gender">
            <el-option label="男" value="male" />
            <el-option label="女" value="female" />
          </el-select>
        </el-form-item>
        <el-form-item label="城市">
          <el-input v-model="newAgent.demographics.location" placeholder="请输入城市" />
        </el-form-item>
        <el-form-item label="兴趣标签">
          <el-input v-model="interestInput" placeholder="多个标签用逗号分隔" />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="useLLM">使用LLM生成行为参数</el-checkbox>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateModal = false">取消</el-button>
        <el-button type="primary" @click="createAgent">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { Plus } from '@element-plus/icons-vue';
import { useAgentStore } from '../store';

const agentStore = useAgentStore();

const showCreateModal = ref(false);
const searchQuery = ref('');
const filterPersona = ref('');
const currentPage = ref(1);
const pageSize = ref(10);

const newAgent = ref({
  name: '',
  persona_type: 'price_sensitive',
  demographics: {
    age: 25,
    gender: 'female',
    location: '一线城市'
  },
  interests: []
});

const interestInput = ref('');
const useLLM = ref(false);

const filteredAgents = computed(() => {
  let result = agentStore.agents;
  if (searchQuery.value) {
    result = result.filter(a => a.name?.toLowerCase().includes(searchQuery.value.toLowerCase()));
  }
  if (filterPersona.value) {
    result = result.filter(a => a.persona_type === filterPersona.value);
  }
  return result.slice((currentPage.value - 1) * pageSize.value, currentPage.value * pageSize.value);
});

const total = computed(() => agentStore.agents.length);

const personaTypes = {
  price_sensitive: { label: '价格敏感型', type: 'warning' },
  impulse: { label: '冲动消费型', type: 'success' },
  brand_loyal: { label: '品牌忠诚型', type: 'primary' },
  rational: { label: '理性决策型', type: 'info' },
  deal_seeker: { label: '优惠追逐型', type: 'danger' }
};

const getPersonaLabel = (type) => personaTypes[type]?.label || type;
const getPersonaType = (type) => personaTypes[type]?.type || 'default';

const viewAgent = (agent) => {
  console.log('查看智能体:', agent);
};

const deleteAgent = async (id) => {
  try {
    await agentStore.deleteAgent(id);
  } catch (error) {
    console.error('删除失败:', error);
  }
};

const createAgent = async () => {
  newAgent.value.interests = interestInput.value.split(',').map(i => i.trim()).filter(i => i);
  try {
    await agentStore.createAgent(newAgent.value, useLLM.value);
    showCreateModal.value = false;
    newAgent.value = {
      name: '',
      persona_type: 'price_sensitive',
      demographics: { age: 25, gender: 'female', location: '一线城市' },
      interests: []
    };
    interestInput.value = '';
    useLLM.value = false;
  } catch (error) {
    console.error('创建失败:', error);
  }
};

const handlePageChange = (page) => {
  currentPage.value = page;
};

onMounted(async () => {
  try {
    await agentStore.fetchAgents();
  } catch (error) {
    console.error('加载智能体失败:', error);
  }
});
</script>

<style scoped>
.agents-page { padding: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { margin: 0; }
.filter-bar { display: flex; gap: 15px; margin-bottom: 20px; }
.filter-select { width: 150px; }
.search-input { width: 200px; }
</style>
`.trim();

const abTestingContent = `
<template>
  <div class="ab-testing-page">
    <div class="page-header">
      <h2>虚拟A/B测试工作台</h2>
    </div>

    <div class="tabs-container">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="创建实验" name="create">
          <el-card>
            <el-form :model="newCampaign" label-width="120px">
              <el-form-item label="实验名称">
                <el-input v-model="newCampaign.name" placeholder="请输入实验名称" />
              </el-form-item>
              <el-form-item label="目标受众">
                <el-select v-model="newCampaign.targetAudience" multiple placeholder="选择目标受众类型">
                  <el-option label="全部" value="all" />
                  <el-option label="价格敏感型" value="price_sensitive" />
                  <el-option label="冲动消费型" value="impulse" />
                  <el-option label="品牌忠诚型" value="brand_loyal" />
                  <el-option label="理性决策型" value="rational" />
                  <el-option label="优惠追逐型" value="deal_seeker" />
                </el-select>
              </el-form-item>
              <el-form-item label="样本数量">
                <el-input type="number" v-model="newCampaign.agentCount" placeholder="参与实验的智能体数量" />
              </el-form-item>
              <el-form-item label="广告变体">
                <div v-for="(variant, index) in newCampaign.variants" :key="index" class="variant-item">
                  <div class="variant-header">
                    <span>变体 {{ String.fromCharCode(65 + index) }}</span>
                    <el-button size="small" type="danger" @click="removeVariant(index)" v-if="newCampaign.variants.length > 2">删除</el-button>
                  </div>
                  <el-input v-model="variant.title" placeholder="广告标题" class="variant-input" />
                  <el-input v-model="variant.description" placeholder="广告描述" class="variant-input" />
                  <el-input type="number" v-model="variant.price" placeholder="价格" class="variant-input" />
                </div>
                <el-button type="dashed" @click="addVariant" v-if="newCampaign.variants.length < 5">
                  添加变体
                </el-button>
              </el-form-item>
              <el-form-item>
                <el-checkbox v-model="useLLM">使用LLM决策推理</el-checkbox>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="createCampaign">创建实验</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-tab-pane>

        <el-tab-pane label="进行中实验" name="running">
          <el-card v-if="runningCampaigns.length > 0">
            <el-table :data="runningCampaigns" border>
              <el-table-column prop="name" label="实验名称" />
              <el-table-column prop="variants" label="变体数量">
                <template #default="scope">{{ scope.row.variants?.length || 0 }}</template>
              </el-table-column>
              <el-table-column prop="agentCount" label="样本数" />
              <el-table-column prop="status" label="状态">
                <template #default="scope">
                  <el-tag type="warning">进行中</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="progress" label="进度">
                <template #default="scope">
                  <el-progress :percentage="scope.row.progress || 0" :show-text="false" />
                </template>
              </el-table-column>
              <el-table-column label="操作">
                <template #default="scope">
                  <el-button size="small" @click="viewCampaign(scope.row)">查看</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
          <div v-else class="empty-state">暂无进行中的实验</div>
        </el-tab-pane>

        <el-tab-pane label="历史结果" name="results">
          <el-card v-if="completedCampaigns.length > 0">
            <el-table :data="completedCampaigns" border @row-click="viewResults">
              <el-table-column prop="name" label="实验名称" />
              <el-table-column prop="variants" label="变体数量">
                <template #default="scope">{{ scope.row.variants?.length || 0 }}</template>
              </el-table-column>
              <el-table-column prop="agentCount" label="样本数" />
              <el-table-column prop="status" label="状态">
                <template #default="scope">
                  <el-tag type="success">已完成</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="metrics" label="最优CTR">
                <template #default="scope">
                  {{ scope.row.metrics?.bestCtr || '-' }}%
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="创建时间" />
            </el-table>
          </el-card>
          <div v-else class="empty-state">暂无实验结果</div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <el-dialog title="实验结果" v-model="showResultsModal" width="800px">
      <div v-if="selectedCampaign" class="results-content">
        <h3>{{ selectedCampaign.name }}</h3>
        <div class="results-summary">
          <div class="summary-item">
            <span class="summary-label">总曝光</span>
            <span class="summary-value">{{ totalImpressions }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">总点击</span>
            <span class="summary-value">{{ totalClicks }}</span>
          </div>
          <div class="summary-item">
            <span class="summary-label">总转化</span>
            <span class="summary-value">{{ totalConversions }}</span>
          </div>
        </div>
        <el-table :data="selectedCampaign.variantResults" border>
          <el-table-column prop="variantId" label="变体" />
          <el-table-column prop="impressions" label="曝光" />
          <el-table-column prop="clicks" label="点击" />
          <el-table-column prop="conversions" label="转化" />
          <el-table-column prop="ctr" label="CTR">
            <template #default="scope">{{ ((scope.row.clicks / scope.row.impressions) * 100).toFixed(2) }}%</template>
          </el-table-column>
          <el-table-column prop="cvr" label="CVR">
            <template #default="scope">{{ ((scope.row.conversions / scope.row.clicks) * 100).toFixed(2) }}%</template>
          </el-table-column>
        </el-table>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useCampaignStore } from '../store';

const campaignStore = useCampaignStore();

const activeTab = ref('create');
const showResultsModal = ref(false);
const selectedCampaign = ref(null);
const useLLM = ref(false);

const newCampaign = ref({
  name: '',
  targetAudience: ['all'],
  agentCount: 100,
  variants: [
    { id: 'A', title: '', description: '', price: 99 },
    { id: 'B', title: '', description: '', price: 199 }
  ]
});

const runningCampaigns = computed(() => 
  campaignStore.campaigns.filter(c => c.status === 'running')
);

const completedCampaigns = computed(() => 
  campaignStore.campaigns.filter(c => c.status === 'completed')
);

const totalImpressions = computed(() => {
  if (!selectedCampaign.value?.variantResults) return 0;
  return selectedCampaign.value.variantResults.reduce((sum, r) => sum + (r.impressions || 0), 0);
});

const totalClicks = computed(() => {
  if (!selectedCampaign.value?.variantResults) return 0;
  return selectedCampaign.value.variantResults.reduce((sum, r) => sum + (r.clicks || 0), 0);
});

const totalConversions = computed(() => {
  if (!selectedCampaign.value?.variantResults) return 0;
  return selectedCampaign.value.variantResults.reduce((sum, r) => sum + (r.conversions || 0), 0);
});

const addVariant = () => {
  if (newCampaign.value.variants.length < 5) {
    const nextId = String.fromCharCode(65 + newCampaign.value.variants.length);
    newCampaign.value.variants.push({ id: nextId, title: '', description: '', price: 99 });
  }
};

const removeVariant = (index) => {
  newCampaign.value.variants.splice(index, 1);
  newCampaign.value.variants.forEach((v, i) => {
    v.id = String.fromCharCode(65 + i);
  });
};

const createCampaign = async () => {
  try {
    await campaignStore.createCampaign(newCampaign.value);
    const campaign = campaignStore.campaigns.find(c => c.name === newCampaign.value.name);
    if (campaign) {
      await campaignStore.startSimulation(campaign.id, useLLM.value);
    }
    newCampaign.value = {
      name: '',
      targetAudience: ['all'],
      agentCount: 100,
      variants: [
        { id: 'A', title: '', description: '', price: 99 },
        { id: 'B', title: '', description: '', price: 199 }
      ]
    };
    useLLM.value = false;
    activeTab.value = 'running';
  } catch (error) {
    console.error('创建实验失败:', error);
  }
};

const viewCampaign = (campaign) => {
  selectedCampaign.value = campaign;
  showResultsModal.value = true;
};

const viewResults = (campaign) => {
  selectedCampaign.value = campaign;
  showResultsModal.value = true;
};

onMounted(async () => {
  try {
    await campaignStore.fetchCampaigns();
  } catch (error) {
    console.error('加载实验失败:', error);
  }
});
</script>

<style scoped>
.ab-testing-page { padding: 20px; }
.page-header { margin-bottom: 20px; }
.page-header h2 { margin: 0; }
.tabs-container { height: calc(100vh - 180px); }
.variant-item { margin-bottom: 15px; padding: 15px; background: #f9fafb; border-radius: 8px; }
.variant-header { display: flex; justify-content: space-between; margin-bottom: 10px; font-weight: 600; }
.variant-input { width: 100%; margin-bottom: 10px; }
.empty-state { text-align: center; padding: 50px; color: #999; }
.results-content { padding: 10px; }
.results-summary { display: flex; gap: 30px; margin-bottom: 20px; }
.summary-item { display: flex; flex-direction: column; }
.summary-label { font-size: 14px; color: #999; }
.summary-value { font-size: 24px; font-weight: 600; color: #333; }
</style>
`.trim();

// 创建目录
if (!fs.existsSync('src/components')) fs.mkdirSync('src/components', { recursive: true });
if (!fs.existsSync('src/views')) fs.mkdirSync('src/views', { recursive: true });

// 写入文件
fs.writeFileSync('src/components/Header.vue', headerContent, 'utf8');
console.log('Header.vue created');

fs.writeFileSync('src/components/Sidebar.vue', sidebarContent, 'utf8');
console.log('Sidebar.vue created');

fs.writeFileSync('src/App.vue', appContent, 'utf8');
console.log('App.vue created');

fs.writeFileSync('src/views/Dashboard.vue', dashboardContent, 'utf8');
console.log('Dashboard.vue created');

fs.writeFileSync('src/views/Agents.vue', agentsContent, 'utf8');
console.log('Agents.vue created');

fs.writeFileSync('src/views/ABTesting.vue', abTestingContent, 'utf8');
console.log('ABTesting.vue created');

console.log('All Vue components created successfully!');
