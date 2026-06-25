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
                <el-button type="text" @click="addVariant" v-if="newCampaign.variants.length < 5" style="border: 1px dashed #d9d9d9; color: #606266; padding: 8px 20px;">
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
          <el-table-column prop="variant_id" label="变体" />
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
import { useAppStore } from '../store';

const campaignStore = useAppStore();

const activeTab = ref('create');
const showResultsModal = ref(false);
const selectedCampaign = ref(null);
const useLLM = ref(true);

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
    activeTab.value = 'running';
  } catch (error) {
    console.error('创建实验失败:', error);
  }
};

const viewCampaign = async (campaign) => {
  const detailed = await campaignStore.getCampaignById(campaign.id);
  selectedCampaign.value = detailed || campaign;
  showResultsModal.value = true;
};

const viewResults = async (campaign) => {
  const detailed = await campaignStore.getCampaignById(campaign.id);
  selectedCampaign.value = detailed || campaign;
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