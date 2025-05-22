<template>
  <div class="task-management">
    <h1>任务管理</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div class="task-list">
        <h2>任务列表</h2>
        <ul>
          <li v-for="task in tasks" :key="task.id">
            <p>任务ID: {{ task.id }}</p>
            <p>名称: {{ task.name }}</p>
            <button @click="createTask">创建任务</button>
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
      tasks: [],
      loading: true
    };
  },
  async created() {
    await this.fetchTasks();
  },
  methods: {
    async fetchTasks() {
      try {
        const response = await axios.get('/api/v1/tasks/');
        this.tasks = response.data;
        this.loading = false;
      } catch (error) {
        console.error('获取任务列表失败:', error);
        this.loading = false;
      }
    },
    async createTask() {
      try {
        const response = await axios.post('/api/v1/tasks/', { name: 'New Task' });
        console.log('任务已创建:', response.data);
      } catch (error) {
        console.error('创建任务失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.task-management {
  padding: 20px;
}
.task-list {
  margin-bottom: 20px;
}
</style> 