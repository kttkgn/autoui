<template>
  <div class="environment-management">
    <h1>环境管理</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div class="environment-list">
        <h2>环境列表</h2>
        <ul>
          <li v-for="env in environments" :key="env.name">
            <p>名称: {{ env.name }}</p>
            <p>描述: {{ env.description }}</p>
            <button @click="getEnvironmentDetails(env.name)">查看详情</button>
            <button @click="updateEnvironment(env.name)">更新</button>
            <button @click="deleteEnvironment(env.name)">删除</button>
            <button @click="switchEnvironment(env.name)">切换</button>
            <button @click="validateEnvironment(env.name)">验证</button>
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
      environments: [],
      loading: true
    };
  },
  async created() {
    await this.fetchEnvironments();
  },
  methods: {
    async fetchEnvironments() {
      try {
        const response = await axios.get('/api/v1/environments');
        this.environments = response.data.environments;
        this.loading = false;
      } catch (error) {
        console.error('获取环境列表失败:', error);
        this.loading = false;
      }
    },
    async getEnvironmentDetails(name) {
      try {
        const response = await axios.get(`/api/v1/environments/${name}`);
        console.log('环境详情:', response.data);
      } catch (error) {
        console.error('获取环境详情失败:', error);
      }
    },
    async updateEnvironment(name) {
      try {
        const response = await axios.put(`/api/v1/environments/${name}`, { config: {}, description: 'Updated Description' });
        console.log('环境已更新:', response.data);
      } catch (error) {
        console.error('更新环境失败:', error);
      }
    },
    async deleteEnvironment(name) {
      try {
        await axios.delete(`/api/v1/environments/${name}`);
        console.log('环境已删除');
      } catch (error) {
        console.error('删除环境失败:', error);
      }
    },
    async switchEnvironment(name) {
      try {
        const response = await axios.post(`/api/v1/environments/${name}/switch`);
        console.log('环境已切换:', response.data);
      } catch (error) {
        console.error('切换环境失败:', error);
      }
    },
    async validateEnvironment(name) {
      try {
        const response = await axios.get(`/api/v1/environments/${name}/validate`);
        console.log('环境验证结果:', response.data);
      } catch (error) {
        console.error('验证环境失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.environment-management {
  padding: 20px;
}
.environment-list {
  margin-bottom: 20px;
}
</style> 