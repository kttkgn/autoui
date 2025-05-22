<template>
  <div class="test-case-management">
    <h1>测试用例管理</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div v-for="testCase in testCases" :key="testCase.id" class="test-case-item">
        <h3>{{ testCase.name }}</h3>
        <p>描述: {{ testCase.description }}</p>
        <button @click="getTestCaseDetails(testCase.id)">查看详情</button>
        <button @click="updateTestCase(testCase.id)">更新测试用例</button>
        <button @click="deleteTestCase(testCase.id)">删除测试用例</button>
        <button @click="executeTestCase(testCase.id)">执行测试用例</button>
        <button @click="executeKeywordTestCase(testCase.id)">执行关键字驱动测试用例</button>
        <button @click="executeDataTestCase(testCase.id)">执行数据驱动测试用例</button>
        <button @click="executeBatchTestCase(testCase.id)">批量执行测试用例</button>
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
      loading: true,
    };
  },
  methods: {
    async fetchTestCases() {
      try {
        const response = await axios.get('/api/v1/test-suites/1/test-cases');
        this.testCases = response.data;
      } catch (error) {
        console.error('获取测试用例列表失败:', error);
      } finally {
        this.loading = false;
      }
    },
    async getTestCaseDetails(testCaseId) {
      try {
        const response = await axios.get(`/api/v1/test-cases/${testCaseId}`);
        alert('测试用例详情: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('获取测试用例详情失败:', error);
      }
    },
    async updateTestCase(testCaseId) {
      try {
        const response = await axios.put(`/api/v1/test-cases/${testCaseId}`, { name: 'Updated Test Case', description: 'Updated Description' });
        alert('测试用例更新成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('更新测试用例失败:', error);
      }
    },
    async deleteTestCase(testCaseId) {
      try {
        await axios.delete(`/api/v1/test-cases/${testCaseId}`);
        alert('测试用例已删除');
        this.fetchTestCases();
      } catch (error) {
        console.error('删除测试用例失败:', error);
      }
    },
    async executeTestCase(testCaseId) {
      try {
        const response = await axios.post(`/api/v1/test-cases/${testCaseId}/execute`);
        alert('执行测试用例成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('执行测试用例失败:', error);
      }
    },
    async executeKeywordTestCase(testCaseId) {
      try {
        const response = await axios.post(`/api/v1/test-cases/${testCaseId}/execute/keyword`, { keyword: 'example_keyword', params: {} });
        alert('执行关键字驱动测试用例成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('执行关键字驱动测试用例失败:', error);
      }
    },
    async executeDataTestCase(testCaseId) {
      try {
        const response = await axios.post(`/api/v1/test-cases/${testCaseId}/execute/data`, [{ param1: 'value1' }]);
        alert('执行数据驱动测试用例成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('执行数据驱动测试用例失败:', error);
      }
    },
    async executeBatchTestCase(testCaseId) {
      try {
        const response = await axios.post(`/api/v1/test-cases/${testCaseId}/execute/batch`, { data_list: [{ param1: 'value1' }] });
        alert('批量执行测试用例成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('批量执行测试用例失败:', error);
      }
    },
  },
  mounted() {
    this.fetchTestCases();
  },
};
</script>

<style scoped>
.test-case-management {
  padding: 20px;
}
.test-case-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style> 