import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/dashboard", name: "Dashboard", component: () => import("../views/Dashboard.vue") },
  { path: "/agents", name: "Agents", component: () => import("../views/Agents.vue") },
  { path: "/ab-testing", name: "ABTesting", component: () => import("../views/ABTesting.vue") },
  { path: "/", redirect: "/dashboard" }
];

const router = createRouter({ history: createWebHistory(), routes });
export default router;