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
import { useAppStore } from '../store';

const agentStore = useAppStore();

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