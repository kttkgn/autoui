<template>
  <div class="project-management">
    <h1>项目管理</h1>
    <div v-if="loading">加载中...</div>
    <div v-else>
      <div v-for="project in projects" :key="project.id" class="project-item">
        <h3>{{ project.name }}</h3>
        <p>描述: {{ project.description }}</p>
        <p>状态: {{ project.status }}</p>
        <button @click="getProjectDetails(project.id)">查看详情</button>
        <button @click="updateProject(project.id)">更新项目</button>
        <button @click="deleteProject(project.id)">删除项目</button>
        <button @click="addProjectMember(project.id)">添加成员</button>
        <button @click="removeProjectMember(project.id)">移除成员</button>
        <button @click="getProjectMembers(project.id)">获取成员</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      projects: [],
      loading: true,
    };
  },
  methods: {
    async fetchProjects() {
      try {
        const response = await axios.get('/api/v1/projects');
        this.projects = response.data.projects;
      } catch (error) {
        console.error('获取项目列表失败:', error);
      } finally {
        this.loading = false;
      }
    },
    async getProjectDetails(projectId) {
      try {
        const response = await axios.get(`/api/v1/projects/${projectId}`);
        alert('项目详情: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('获取项目详情失败:', error);
      }
    },
    async updateProject(projectId) {
      try {
        const response = await axios.put(`/api/v1/projects/${projectId}`, { name: 'Updated Project', description: 'Updated Description' });
        alert('项目更新成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('更新项目失败:', error);
      }
    },
    async deleteProject(projectId) {
      try {
        await axios.delete(`/api/v1/projects/${projectId}`);
        alert('项目已删除');
        this.fetchProjects();
      } catch (error) {
        console.error('删除项目失败:', error);
      }
    },
    async addProjectMember(projectId) {
      try {
        const response = await axios.post(`/api/v1/projects/${projectId}/members`, { user_id: 'example_user_id', role: 'member' });
        alert('添加成员成功: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('添加成员失败:', error);
      }
    },
    async removeProjectMember(projectId) {
      try {
        await axios.delete(`/api/v1/projects/${projectId}/members/example_user_id`);
        alert('成员已移除');
      } catch (error) {
        console.error('移除成员失败:', error);
      }
    },
    async getProjectMembers(projectId) {
      try {
        const response = await axios.get(`/api/v1/projects/${projectId}/members`);
        alert('项目成员: ' + JSON.stringify(response.data));
      } catch (error) {
        console.error('获取项目成员失败:', error);
      }
    },
  },
  mounted() {
    this.fetchProjects();
  },
};
</script>

<style scoped>
.project-management {
  padding: 20px;
}
.project-item {
  margin-bottom: 20px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}
</style> 