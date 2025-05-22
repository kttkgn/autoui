<template>
  <div class="element-management">
    <h1>元素管理</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div v-for="device in devices" :key="device.id" class="device-item">
        <h3>{{ device.name }}</h3>
        <p>状态: {{ device.status }}</p>
        <button @click="connectDevice(device.id)">连接设备</button>
        <button @click="disconnectDevice(device.id)">断开设备</button>
        <button @click="locateElement(device.id)">定位元素</button>
        <button @click="getElementTree(device.id)">获取元素树</button>
        <button @click="highlightElement(device.id)">高亮显示元素</button>
        <button @click="takeScreenshot(device.id)">获取截图</button>
        <button @click="performAction(device.id)">执行元素操作</button>
        <button @click="getScreenSize(device.id)">获取屏幕尺寸</button>
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
      loading: true,
    };
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
    async connectDevice(deviceId) {
      try {
        await axios.post(`/api/v1/elements/${deviceId}/connect`);
        alert('设备连接成功');
      } catch (error) {
        console.error('连接设备失败:', error);
      }
    },
    async disconnectDevice(deviceId) {
      try {
        await axios.post(`/api/v1/elements/${deviceId}/disconnect`);
        alert('设备已断开连接');
      } catch (error) {
        console.error('断开设备连接失败:', error);
      }
    },
    async locateElement(deviceId) {
      try {
        const response = await axios.post('/api/v1/elements/locate', { device_id: deviceId });
        alert('元素定位成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('定位元素失败:', error);
      }
    },
    async getElementTree(deviceId) {
      try {
        const response = await axios.get(`/api/v1/elements/tree?device_id=${deviceId}`);
        alert('获取元素树成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('获取元素树失败:', error);
      }
    },
    async highlightElement(deviceId) {
      try {
        await axios.post(`/api/v1/elements/${deviceId}/highlight`, { element_id: 'example_element_id' });
        alert('元素已高亮');
      } catch (error) {
        console.error('高亮显示元素失败:', error);
      }
    },
    async takeScreenshot(deviceId) {
      try {
        const response = await axios.get(`/api/v1/elements/${deviceId}/screenshot`);
        alert('获取截图成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('获取截图失败:', error);
      }
    },
    async performAction(deviceId) {
      try {
        const response = await axios.post(`/api/v1/elements/${deviceId}/action`, { element_id: 'example_element_id', action: 'click' });
        alert('执行元素操作成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('执行元素操作失败:', error);
      }
    },
    async getScreenSize(deviceId) {
      try {
        const response = await axios.get(`/api/v1/elements/${deviceId}/screen-size`);
        alert('获取屏幕尺寸成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('获取屏幕尺寸失败:', error);
      }
    },
  },
  mounted() {
    this.fetchDevices();
  },
};
</script>

<style scoped>
.element-management {
  padding: 20px;
}
.device-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style> 