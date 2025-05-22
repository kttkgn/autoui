<template>
  <div class="test-case-list">
    <h1>测试用例列表</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div v-for="testCase in testCases" :key="testCase.id" class="test-case-card">
        <h2>{{ testCase.name }}</h2>
        <p>步骤数: {{ testCase.steps.length }}</p>
        <button @click="executeTestCase(testCase.id)">执行</button>
        <button @click="executeKeywordTestCase(testCase.id, 'click')">关键字执行</button>
        <button @click="executeDataDrivenTestCase(testCase.id, [{ value: 'test' }])">数据驱动执行</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      testCases: [],
      loading: true
    };
  },
  async created() {
    await this.fetchTestCases();
  },
  methods: {
    async fetchTestCases() {
      try {
        const response = await axios.get('/api/v1/test-cases');
        this.testCases = response.data;
        this.loading = false;
      } catch (error) {
        console.error('获取测试用例列表失败:', error);
        this.loading = false;
      }
    },
    async executeTestCase(testCaseId) {
      try {
        const response = await axios.post(`/api/v1/test-cases/${testCaseId}/execute`);
        console.log('执行结果:', response.data);
      } catch (error) {
        console.error('执行测试用例失败:', error);
      }
    },
    async executeKeywordTestCase(testCaseId, keyword) {
      try {
        const response = await axios.post(`/api/v1/test-cases/${testCaseId}/execute/keyword`, { keyword });
        console.log('关键字执行结果:', response.data);
      } catch (error) {
        console.error('关键字执行失败:', error);
      }
    },
    async executeDataDrivenTestCase(testCaseId, data) {
      try {
        const response = await axios.post(`/api/v1/test-cases/${testCaseId}/execute/data`, { data });
        console.log('数据驱动执行结果:', response.data);
      } catch (error) {
        console.error('数据驱动执行失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.test-case-list {
  padding: 20px;
}
.test-case-card {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}
button {
  margin-right: 10px;
}
</style> 