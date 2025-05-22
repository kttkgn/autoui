<template>
  <div class="device-management">
    <h1>设备管理</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div class="device-list">
        <h2>设备列表</h2>
        <div v-for="device in devices" :key="device.id" class="device-item">
          <h3>{{ device.name }}</h3>
          <p>状态: {{ device.status }}</p>
          <button @click="updateDeviceStatus(device.id, 'active')">更新状态</button>
          <button @click="deleteDevice(device.id)">删除设备</button>
          <button @click="startMonitoring(device.id)">开始监控</button>
          <button @click="stopMonitoring(device.id)">停止监控</button>
          <button @click="getScreenStream(device.id)">获取屏幕流</button>
          <div v-if="device.screenStream" class="screen-stream">
            <img :src="device.screenStream" alt="屏幕流" />
          </div>
        </div>
      </div>
      <div class="device-details">
        <h2>设备详情</h2>
        <div v-if="selectedDevice">
          <p>设备ID: {{ selectedDevice.id }}</p>
          <p>类型: {{ selectedDevice.type }}</p>
          <p>状态: {{ selectedDevice.status }}</p>
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
      devices: [],
      selectedDevice: null,
      loading: true,
      websocket: null,
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
      } catch (error) {
        console.error('获取设备列表失败:', error);
      } finally {
        this.loading = false;
      }
    },
    async updateDeviceStatus(deviceId, status) {
      try {
        await axios.put(`/api/v1/devices/${deviceId}/status`, { status });
        this.fetchDevices();
      } catch (error) {
        console.error('更新设备状态失败:', error);
      }
    },
    async deleteDevice(deviceId) {
      try {
        await axios.delete(`/api/v1/devices/${deviceId}`);
        this.fetchDevices();
      } catch (error) {
        console.error('删除设备失败:', error);
      }
    },
    async startMonitoring(deviceId) {
      try {
        await axios.post(`/api/v1/devices/${deviceId}/monitor/start`);
      } catch (error) {
        console.error('开始监控失败:', error);
      }
    },
    async stopMonitoring(deviceId) {
      try {
        await axios.post(`/api/v1/devices/${deviceId}/monitor/stop`);
      } catch (error) {
        console.error('停止监控失败:', error);
      }
    },
    getScreenStream(deviceId) {
      if (this.websocket) {
        this.websocket.close();
      }
      this.websocket = new WebSocket(`ws://localhost:8000/ws/screen/${deviceId}`);
      this.websocket.onmessage = (event) => {
        const device = this.devices.find(d => d.id === deviceId);
        if (device) {
          device.screenStream = event.data;
        }
      };
    },
  }
};
</script>

<style scoped>
.device-management {
  padding: 20px;
}
.device-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.device-details {
  margin-top: 20px;
}
.screen-stream {
  margin-top: 10px;
}
</style> 