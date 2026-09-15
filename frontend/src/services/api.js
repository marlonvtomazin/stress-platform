import axios from "axios";
import {
  logApi,
  logSuccess,
  logError,
} from "../config/logger";

const api = axios.create({
  baseURL: "http://localhost:8080",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});

api.interceptors.request.use((config) => {
  logApi(`${config.method?.toUpperCase()} ${config.url}`, config.params || config.data);
  return config;
});

api.interceptors.response.use(
  (response) => {
    logSuccess(
      `${response.status} ${response.config.method?.toUpperCase()} ${response.config.url}`
    );

    return response;
  },
  (error) => {
    logError(
      `${error.response?.status || "NETWORK"} ${error.config?.url}`,
      error.response?.data || error.message
    );

    return Promise.reject(error);
  }
);

export default api;