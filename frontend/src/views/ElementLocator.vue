<template>
  <div class="element-locator">
    <h1>元素定位</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div class="device-connection">
        <h2>设备连接</h2>
        <button @click="connectDevice(deviceId)">连接设备</button>
        <button @click="disconnectDevice(deviceId)">断开连接</button>
      </div>
      <div class="element-location">
        <h2>元素定位</h2>
        <button @click="locateElement">定位元素</button>
        <button @click="getElementTree">获取元素树</button>
        <button @click="highlightElement">高亮元素</button>
        <button @click="takeScreenshot">获取截图</button>
        <button @click="performAction">执行操作</button>
        <button @click="getScreenSize">获取屏幕尺寸</button>
      </div>
      <div class="screen-stream">
        <h2>屏幕流</h2>
        <img :src="screenStreamUrl" alt="屏幕流" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      deviceId: 'example_device_id',
      screenStreamUrl: '',
      loading: true
    };
  },
  async created() {
    await this.fetchScreenStream();
  },
  methods: {
    async connectDevice(deviceId) {
      try {
        await axios.post(`/api/v1/elements/${deviceId}/connect`);
        console.log('设备连接成功');
      } catch (error) {
        console.error('设备连接失败:', error);
      }
    },
    async disconnectDevice(deviceId) {
      try {
        await axios.post(`/api/v1/elements/${deviceId}/disconnect`);
        console.log('设备已断开连接');
      } catch (error) {
        console.error('断开设备连接失败:', error);
      }
    },
    async locateElement() {
      try {
        const response = await axios.post('/api/v1/elements/locate', { device_id: this.deviceId, strategy: 'id', selector: 'example' });
        console.log('元素定位结果:', response.data);
      } catch (error) {
        console.error('元素定位失败:', error);
      }
    },
    async getElementTree() {
      try {
        const response = await axios.get(`/api/v1/elements/tree?device_id=${this.deviceId}`);
        console.log('元素树:', response.data);
      } catch (error) {
        console.error('获取元素树失败:', error);
      }
    },
    async highlightElement() {
      try {
        await axios.post(`/api/v1/elements/${this.deviceId}/highlight`, { element_id: 'example_element_id' });
        console.log('元素已高亮');
      } catch (error) {
        console.error('高亮元素失败:', error);
      }
    },
    async takeScreenshot() {
      try {
        const response = await axios.get(`/api/v1/elements/${this.deviceId}/screenshot`);
        console.log('截图:', response.data);
      } catch (error) {
        console.error('获取截图失败:', error);
      }
    },
    async performAction() {
      try {
        const response = await axios.post(`/api/v1/elements/${this.deviceId}/action`, { element_id: 'example_element_id', action: 'click', params: {} });
        console.log('操作执行结果:', response.data);
      } catch (error) {
        console.error('执行操作失败:', error);
      }
    },
    async getScreenSize() {
      try {
        const response = await axios.get(`/api/v1/elements/${this.deviceId}/screen-size`);
        console.log('屏幕尺寸:', response.data);
      } catch (error) {
        console.error('获取屏幕尺寸失败:', error);
      }
    },
    async fetchScreenStream() {
      try {
        const response = await axios.get(`/api/v1/elements/${this.deviceId}/screen`);
        this.screenStreamUrl = response.data.url;
        this.loading = false;
      } catch (error) {
        console.error('获取屏幕流失败:', error);
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
.element-locator {
  padding: 20px;
}
.device-connection, .element-location, .screen-stream {
  margin-bottom: 20px;
}
</style> 