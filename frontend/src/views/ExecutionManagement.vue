<template>
  <div class="execution-management">
    <h1>执行管理</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div class="execution-list">
        <h2>执行列表</h2>
        <ul>
          <li v-for="execution in executions" :key="execution.id">
            <p>执行ID: {{ execution.id }}</p>
            <p>状态: {{ execution.status }}</p>
            <button @click="getExecutionDetails(execution.id)">查看详情</button>
            <button @click="getExecutionStatus(execution.id)">查看状态</button>
            <button @click="getExecutionResult(execution.id)">查看结果</button>
            <button @click="stopExecution(execution.id)">停止执行</button>
          </li>
        </ul>
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
      loading: true
    };
  },
  async created() {
    await this.fetchExecutions();
  },
  methods: {
    async fetchExecutions() {
      try {
        const response = await axios.get('/api/v1/execution');
        this.executions = response.data.executions;
        this.loading = false;
      } catch (error) {
        console.error('获取执行列表失败:', error);
        this.loading = false;
      }
    },
    async getExecutionDetails(executionId) {
      try {
        const response = await axios.get(`/api/v1/execution/${executionId}`);
        console.log('执行详情:', response.data);
      } catch (error) {
        console.error('获取执行详情失败:', error);
      }
    },
    async getExecutionStatus(executionId) {
      try {
        const response = await axios.get(`/api/v1/execution/${executionId}/status`);
        console.log('执行状态:', response.data);
      } catch (error) {
        console.error('获取执行状态失败:', error);
      }
    },
    async getExecutionResult(executionId) {
      try {
        const response = await axios.get(`/api/v1/execution/${executionId}/result`);
        console.log('执行结果:', response.data);
      } catch (error) {
        console.error('获取执行结果失败:', error);
      }
    },
    async stopExecution(executionId) {
      try {
        await axios.post(`/api/v1/execution/stop`, { execution_id: executionId });
        console.log('执行已停止');
      } catch (error) {
        console.error('停止执行失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.execution-management {
  padding: 20px;
}
.execution-list {
  margin-bottom: 20px;
}
</style> 