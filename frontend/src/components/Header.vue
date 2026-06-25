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