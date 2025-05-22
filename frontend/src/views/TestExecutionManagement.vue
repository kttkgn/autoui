<template>
  <div class="test-execution-management">
    <h1>测试执行管理</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div v-for="execution in executions" :key="execution.id" class="execution-item">
        <h3>{{ execution.name }}</h3>
        <p>状态: {{ execution.status }}</p>
        <button @click="getExecutionResult(execution.id)">获取执行结果</button>
        <button @click="getStepResults(execution.id)">获取步骤结果</button>
        <button @click="startExecution(execution.id)">开始执行</button>
        <button @click="stopExecution(execution.id)">停止执行</button>
        <button @click="getExecutionHistory(execution.test_case_id)">获取执行历史</button>
        <button @click="getProjectSummary(execution.project_id)">获取项目汇总</button>
        <button @click="exportProjectSummary(execution.project_id)">导出项目汇总</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      executions: [],
      loading: true,
    };
  },
  methods: {
    async fetchExecutions() {
      try {
        const response = await axios.get('/api/v1/executions');
        this.executions = response.data;
      } catch (error) {
        console.error('获取测试执行列表失败:', error);
      } finally {
        this.loading = false;
      }
    },
    async getExecutionResult(executionId) {
      try {
        const response = await axios.get(`/api/v1/executions/${executionId}`);
        alert('执行结果: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('获取执行结果失败:', error);
      }
    },
    async getStepResults(executionId) {
      try {
        const response = await axios.get(`/api/v1/executions/${executionId}/steps`);
        alert('步骤结果: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('获取步骤结果失败:', error);
      }
    },
    async startExecution(executionId) {
      try {
        const response = await axios.post(`/api/v1/executions/${executionId}/start`);
        alert('开始执行成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('开始执行失败:', error);
      }
    },
    async stopExecution(executionId) {
      try {
        const response = await axios.post(`/api/v1/executions/${executionId}/stop`);
        alert('停止执行成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('停止执行失败:', error);
      }
    },
    async getExecutionHistory(testCaseId) {
      try {
        const response = await axios.get(`/api/v1/test-cases/${testCaseId}/history`);
        alert('执行历史: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('获取执行历史失败:', error);
      }
    },
    async getProjectSummary(projectId) {
      try {
        const response = await axios.get(`/api/v1/projects/${projectId}/summary`);
        alert('项目汇总: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('获取项目汇总失败:', error);
      }
    },
    async exportProjectSummary(projectId) {
      try {
        const response = await axios.get(`/api/v1/projects/${projectId}/export`);
        alert('导出项目汇总成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('导出项目汇总失败:', error);
      }
    },
  },
  mounted() {
    this.fetchExecutions();
  },
};
</script>

<style scoped>
.test-execution-management {
  padding: 20px;
}
.execution-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style> 