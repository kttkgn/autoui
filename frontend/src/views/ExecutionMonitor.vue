<template>
  <div class="execution-monitor">
    <h1>执行监控</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div class="execution-list">
        <h2>执行列表</h2>
        <div v-for="execution in executions" :key="execution.id" class="execution-item">
          <p>执行ID: {{ execution.id }}</p>
          <p>状态: {{ execution.status }}</p>
          <p>开始时间: {{ execution.start_time }}</p>
          <p>结束时间: {{ execution.end_time }}</p>
        </div>
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
        const response = await axios.get('/api/v1/executions');
        this.executions = response.data;
        this.loading = false;
      } catch (error) {
        console.error('获取执行列表失败:', error);
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.execution-monitor {
  padding: 20px;
}
.execution-list {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}
.execution-item {
  margin-bottom: 10px;
}
</style> 