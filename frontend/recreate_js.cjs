const fs = require('fs');

const routerContent = `import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/dashboard", name: "Dashboard", component: () => import("../views/Dashboard.vue") },
  { path: "/agents", name: "Agents", component: () => import("../views/Agents.vue") },
  { path: "/ab-testing", name: "ABTesting", component: () => import("../views/ABTesting.vue") },
  { path: "/", redirect: "/dashboard" }
];

const router = createRouter({ history: createWebHistory(), routes });
export default router;`;

const mainContent = `import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import { createPinia } from "pinia";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import VChart from "vue-echarts";
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { PieChart, LineChart, BarChart } from "echarts/charts";
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from "echarts/components";

use([CanvasRenderer, PieChart, LineChart, BarChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent]);

const app = createApp(App);
app.use(createPinia());
app.use(router);
app.use(ElementPlus);
app.component("VChart", VChart);
app.mount("#app");`;

const apiContent = `import axios from "axios";

const instance = axios.create({ baseURL: "/api", timeout: 10000 });

instance.interceptors.response.use(
  (response) => response.data,
  (error) => { console.error("API Error:", error); return Promise.reject(error); }
);

export const agentApi = {
  list: (params = {}) => instance.get("/agents", { params }),
  create: (data) => instance.post("/agents", data),
  get: (id) => instance.get("/agents/" + id),
  delete: (id) => instance.delete("/agents/" + id)
};

export const campaignApi = {
  list: (params = {}) => instance.get("/campaigns", { params }),
  create: (data) => instance.post("/campaigns", data),
  get: (id) => instance.get("/campaigns/" + id),
  start: (id) => instance.post("/campaigns/" + id + "/start"),
  results: (id) => instance.get("/campaigns/" + id + "/results")
};

export default instance;`;

const storeContent = `import { defineStore } from "pinia";
import { ref } from "vue";
import { agentApi, campaignApi } from "../api";

export const useAppStore = defineStore("app", () => {
  const agents = ref([]);
  const campaigns = ref([]);
  const currentCampaign = ref(null);
  const simulationResults = ref(null);
  const isSimulating = ref(false);

  const fetchAgents = async () => {
    try {
      const data = await agentApi.list();
      agents.value = data || mockAgents;
    } catch {
      agents.value = mockAgents;
    }
  };

  const createAgent = async (data, useLLM = false) => {
    try {
      const result = await agentApi.create({ ...data, use_llm: useLLM });
      agents.value.push(result);
    } catch {
      const newAgent = {
        id: Date.now().toString(),
        ...data,
        status: "active",
        created_at: new Date().toISOString().split("T")[0],
        behavioral_params: useLLM ? generateLLMParams(data) : {}
      };
      agents.value.push(newAgent);
    }
  };

  const deleteAgent = async (id) => {
    try {
      await agentApi.delete(id);
      agents.value = agents.value.filter(a => a.id !== id);
    } catch {
      agents.value = agents.value.filter(a => a.id !== id);
    }
  };

  const fetchCampaigns = async () => {
    try {
      const data = await campaignApi.list();
      campaigns.value = data || mockCampaigns;
    } catch {
      campaigns.value = mockCampaigns;
    }
  };

  const createCampaign = async (data) => {
    try {
      const result = await campaignApi.create(data);
      campaigns.value.push(result);
    } catch {
      const newCampaign = {
        id: Date.now().toString(),
        ...data,
        status: "created",
        progress: 0,
        created_at: new Date().toISOString().split("T")[0],
        variantResults: []
      };
      campaigns.value.push(newCampaign);
    }
  };

  const startSimulation = async (campaignId, useLLM = false) => {
    const campaign = campaigns.value.find(c => c.id === campaignId);
    if (!campaign) return;

    campaign.status = "running";
    campaign.progress = 0;
    isSimulating.value = true;

    for (let i = 0; i <= 100; i += 10) {
      await new Promise(resolve => setTimeout(resolve, 200));
      campaign.progress = i;
    }

    campaign.status = "completed";
    campaign.variantResults = generateMockResults(campaign.variants);
    isSimulating.value = false;
  };

  return { 
    agents, campaigns, currentCampaign, simulationResults, isSimulating,
    fetchAgents, createAgent, deleteAgent,
    fetchCampaigns, createCampaign, startSimulation
  };
});

const mockAgents = [
  { id: "1", name: "User A", persona_type: "price_sensitive", demographics: { age: 28, gender: "female", location: "Tier 1 City" }, interests: ["shopping", "beauty"], status: "active", created_at: "2024-01-15" },
  { id: "2", name: "User B", persona_type: "impulse", demographics: { age: 32, gender: "male", location: "Tier 2 City" }, interests: ["digital", "sports"], status: "active", created_at: "2024-01-14" },
  { id: "3", name: "User C", persona_type: "brand_loyal", demographics: { age: 25, gender: "female", location: "Tier 1 City" }, interests: ["luxury", "fashion"], status: "active", created_at: "2024-01-13" },
  { id: "4", name: "User D", persona_type: "rational", demographics: { age: 40, gender: "male", location: "Tier 3 City" }, interests: ["cars", "finance"], status: "active", created_at: "2024-01-12" },
  { id: "5", name: "User E", persona_type: "deal_seeker", demographics: { age: 35, gender: "female", location: "Tier 2 City" }, interests: ["coupons", "group buy"], status: "active", created_at: "2024-01-11" },
  { id: "6", name: "User F", persona_type: "price_sensitive", demographics: { age: 22, gender: "male", location: "Tier 1 City" }, interests: ["gaming", "anime"], status: "active", created_at: "2024-01-10" },
  { id: "7", name: "User G", persona_type: "impulse", demographics: { age: 29, gender: "female", location: "Tier 3 City" }, interests: ["food", "travel"], status: "active", created_at: "2024-01-09" },
  { id: "8", name: "User H", persona_type: "brand_loyal", demographics: { age: 38, gender: "male", location: "Tier 1 City" }, interests: ["high-end appliances", "home"], status: "active", created_at: "2024-01-08" },
  { id: "9", name: "User I", persona_type: "rational", demographics: { age: 45, gender: "female", location: "Tier 2 City" }, interests: ["education", "parenting"], status: "active", created_at: "2024-01-07" },
  { id: "10", name: "User J", persona_type: "deal_seeker", demographics: { age: 26, gender: "male", location: "Tier 1 City" }, interests: ["electronics", "accessories"], status: "active", created_at: "2024-01-06" }
];

const mockCampaigns = [
  { id: "c1", name: "Spring Promotion A/B Test", status: "completed", agentCount: 100, variants: [{ id: "A" }, { id: "B" }], progress: 100, created_at: "2024-01-15", variantResults: [{ variantId: "A", impressions: 500, clicks: 43, conversions: 8 }, { variantId: "B", impressions: 500, clicks: 52, conversions: 12 }], metrics: { bestCtr: 10.4 } },
  { id: "c2", name: "Beauty Material Competition", status: "completed", agentCount: 80, variants: [{ id: "A" }, { id: "B" }, { id: "C" }], progress: 100, created_at: "2024-01-14", variantResults: [{ variantId: "A", impressions: 267, clicks: 17, conversions: 3 }, { variantId: "B", impressions: 266, clicks: 21, conversions: 5 }, { variantId: "C", impressions: 267, clicks: 15, conversions: 2 }], metrics: { bestCtr: 7.89 } },
  { id: "c3", name: "Price Sensitivity Test", status: "running", agentCount: 120, variants: [{ id: "A" }, { id: "B" }], progress: 45, created_at: "2024-01-13", variantResults: [] }
];

const generateLLMParams = (agent) => ({
  click_probability: parseFloat((Math.random() * 0.3 + 0.1).toFixed(2)),
  conversion_probability: parseFloat((Math.random() * 0.1 + 0.02).toFixed(2)),
  price_sensitivity: parseFloat((Math.random() * 0.5 + 0.2).toFixed(2)),
  brand_preference: Math.random() > 0.5
});

const generateMockResults = (variants) => {
  return variants.map(v => ({
    variantId: v.id,
    impressions: Math.floor(Math.random() * 300) + 200,
    clicks: Math.floor(Math.random() * 50) + 10,
    conversions: Math.floor(Math.random() * 10) + 2
  }));
};`;

fs.writeFileSync('src/router/index.js', routerContent, { encoding: 'utf8' });
console.log('Created: src/router/index.js');

fs.writeFileSync('src/main.js', mainContent, { encoding: 'utf8' });
console.log('Created: src/main.js');

fs.writeFileSync('src/api/index.js', apiContent, { encoding: 'utf8' });
console.log('Created: src/api/index.js');

fs.writeFileSync('src/store/index.js', storeContent, { encoding: 'utf8' });
console.log('Created: src/store/index.js');

console.log('All JS files recreated successfully');