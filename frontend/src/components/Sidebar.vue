<template>
  <aside class="sidebar">
    <div class="sidebar-header">
      <h2>营销风洞</h2>
      <p class="subtitle">智能体沙盘平台</p>
    </div>
    <el-menu :default-active="activeMenu" mode="vertical" @select="handleSelect">
      <el-menu-item index="/dashboard">
        <el-icon><PieChart /></el-icon>
        <span>仪表盘</span>
      </el-menu-item>
      <el-menu-item index="/agents">
        <el-icon><User /></el-icon>
        <span>Agent管理</span>
      </el-menu-item>
      <el-menu-item index="/ab-testing">
        <el-icon><TrendCharts /></el-icon>
        <span>A/B测试</span>
      </el-menu-item>
    </el-menu>
  </aside>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { PieChart, User, TrendCharts } from '@element-plus/icons-vue';

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