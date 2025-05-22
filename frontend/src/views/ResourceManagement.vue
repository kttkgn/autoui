<template>
  <div class="resource-management">
    <h1>资源管理</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div class="resource-list">
        <h2>资源列表</h2>
        <ul>
          <li v-for="resource in resources" :key="resource.id">
            <p>资源ID: {{ resource.id }}</p>
            <p>类型: {{ resource.type }}</p>
            <p>状态: {{ resource.status }}</p>
            <button @click="getResourceDetails(resource.id)">查看详情</button>
            <button @click="checkResourceHealth(resource.id)">检查健康状态</button>
            <button @click="allocateResource(resource.type)">分配资源</button>
            <button @click="releaseResource(resource.id)">释放资源</button>
            <button @click="updateResourceStatus(resource.id)">更新状态</button>
            <button @click="removeResource(resource.id)">移除资源</button>
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
      resources: [],
      loading: true
    };
  },
  async created() {
    await this.fetchResources();
  },
  methods: {
    async fetchResources() {
      try {
        const response = await axios.get('/api/v1/resources');
        this.resources = response.data.resources;
        this.loading = false;
      } catch (error) {
        console.error('获取资源列表失败:', error);
        this.loading = false;
      }
    },
    async getResourceDetails(resourceId) {
      try {
        const response = await axios.get(`/api/v1/resources/${resourceId}`);
        console.log('资源详情:', response.data);
      } catch (error) {
        console.error('获取资源详情失败:', error);
      }
    },
    async checkResourceHealth(resourceId) {
      try {
        const response = await axios.get(`/api/v1/resources/${resourceId}/health`);
        console.log('资源健康状态:', response.data);
      } catch (error) {
        console.error('检查资源健康状态失败:', error);
      }
    },
    async allocateResource(type) {
      try {
        const response = await axios.post('/api/v1/resources/allocate', { type });
        console.log('资源分配成功:', response.data);
      } catch (error) {
        console.error('分配资源失败:', error);
      }
    },
    async releaseResource(resourceId) {
      try {
        await axios.post(`/api/v1/resources/${resourceId}/release`);
        console.log('资源已释放');
      } catch (error) {
        console.error('释放资源失败:', error);
      }
    },
    async updateResourceStatus(resourceId) {
      try {
        const response = await axios.put(`/api/v1/resources/${resourceId}/status`, { status: 'available' });
        console.log('资源状态已更新:', response.data);
      } catch (error) {
        console.error('更新资源状态失败:', error);
      }
    },
    async removeResource(resourceId) {
      try {
        await axios.delete(`/api/v1/resources/${resourceId}`);
        console.log('资源已移除');
      } catch (error) {
        console.error('移除资源失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.resource-management {
  padding: 20px;
}
.resource-list {
  margin-bottom: 20px;
}
</style> 