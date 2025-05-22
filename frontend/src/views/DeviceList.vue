<template>
  <div class="device-list">
    <h1>设备列表</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div v-for="device in devices" :key="device.id" class="device-card">
        <h2>{{ device.name }}</h2>
        <p>类型: {{ device.type }}</p>
        <p>状态: {{ device.status }}</p>
        <button @click="updateDeviceStatus(device.id, 'online')">上线</button>
        <button @click="updateDeviceStatus(device.id, 'offline')">下线</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      devices: [],
      loading: true
    };
  },
  async created() {
    await this.fetchDevices();
  },
  methods: {
    async fetchDevices() {
      try {
        const response = await axios.get('/api/v1/devices');
        this.devices = response.data;
        this.loading = false;
      } catch (error) {
        console.error('获取设备列表失败:', error);
        this.loading = false;
      }
    },
    async updateDeviceStatus(deviceId, status) {
      try {
        await axios.put(`/api/v1/devices/${deviceId}/status`, { status });
        await this.fetchDevices();
      } catch (error) {
        console.error('更新设备状态失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.device-list {
  padding: 20px;
}
.device-card {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}
button {
  margin-right: 10px;
}
</style> 