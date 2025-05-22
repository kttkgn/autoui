<template>
  <div class="test-report">
    <h1>测试报告</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div class="report-list">
        <h2>报告列表</h2>
        <div v-for="report in reports" :key="report.id" class="report-item">
          <p>报告ID: {{ report.id }}</p>
          <p>执行ID: {{ report.execution_id }}</p>
          <p>生成时间: {{ report.generated_at }}</p>
          <button @click="downloadReport(report.id)">下载报告</button>
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
      reports: [],
      loading: true
    };
  },
  async created() {
    await this.fetchReports();
  },
  methods: {
    async fetchReports() {
      try {
        const response = await axios.get('/api/v1/reports');
        this.reports = response.data;
        this.loading = false;
      } catch (error) {
        console.error('获取报告列表失败:', error);
        this.loading = false;
      }
    },
    async downloadReport(reportId) {
      try {
        const response = await axios.get(`/api/v1/reports/${reportId}/download`, { responseType: 'blob' });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `report-${reportId}.pdf`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (error) {
        console.error('下载报告失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.test-report {
  padding: 20px;
}
.report-list {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
}
.report-item {
  margin-bottom: 10px;
}
</style> 