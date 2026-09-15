import api from "./api";

/**
 * GET /executions
 */
export async function getExecutions() {
  const { data } = await api.get("/executions");
  return data;
}

/**
 * GET /executions/{id}
 */
export async function getExecution(executionId) {
  const { data } = await api.get(`/executions/${executionId}`);
  return data;
}

/**
 * POST /executions/{id}/rerun
 */
export async function rerunExecution(executionId) {
  const { data } = await api.post(`/executions/${executionId}/rerun`);
  return data;
}

/**
 * DELETE /executions/{id}
 */
export async function deleteExecution(executionId) {
  const { data } = await api.delete(`/executions/${executionId}`);
  return data;
}