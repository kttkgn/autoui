<template>
  <div class="report-management">
    <h1>报告管理</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div v-for="report in reports" :key="report.id" class="report-item">
        <h3>{{ report.name }}</h3>
        <p>类型: {{ report.type }}</p>
        <p>执行ID: {{ report.execution_id }}</p>
        <button @click="getReportDetails(report.id)">查看详情</button>
        <button @click="getReportContent(report.id)">获取内容</button>
        <button @click="deleteReport(report.id)">删除报告</button>
        <button @click="exportReport(report.id)">导出报告</button>
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
      loading: true,
    };
  },
  methods: {
    async fetchReports() {
      try {
        const response = await axios.get('/api/v1/reports');
        this.reports = response.data.reports;
      } catch (error) {
        console.error('获取报告列表失败:', error);
      } finally {
        this.loading = false;
      }
    },
    async getReportDetails(reportId) {
      try {
        const response = await axios.get(`/api/v1/reports/${reportId}`);
        alert('报告详情: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('获取报告详情失败:', error);
      }
    },
    async getReportContent(reportId) {
      try {
        const response = await axios.get(`/api/v1/reports/${reportId}/content`);
        alert('报告内容: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('获取报告内容失败:', error);
      }
    },
    async deleteReport(reportId) {
      try {
        await axios.delete(`/api/v1/reports/${reportId}`);
        alert('报告已删除');
        this.fetchReports();
      } catch (error) {
        console.error('删除报告失败:', error);
      }
    },
    async exportReport(reportId) {
      try {
        const response = await axios.post(`/api/v1/reports/export`, { report_id: reportId });
        alert('报告导出成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('导出报告失败:', error);
      }
    },
  },
  mounted() {
    this.fetchReports();
  },
};
</script>

<style scoped>
.report-management {
  padding: 20px;
}
.report-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style> 