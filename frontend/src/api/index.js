import axios from "axios";

const instance = axios.create({ baseURL: "/api", timeout: 60000 });

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
  start: (id, useLLM = false) => instance.post(`/campaigns/${id}/start?use_llm=${useLLM}`),
  results: (id) => instance.get("/campaigns/" + id + "/results")
};

export default instance;