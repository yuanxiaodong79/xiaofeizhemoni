const fs = require('fs');

const appVue = `<template>
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
`;

fs.writeFileSync('./frontend/src/App.vue', appVue);
console.log('App.vue created');
