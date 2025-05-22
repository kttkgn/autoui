import request from '@/utils/request'
import type { Project, TestSuite, TestCase } from '@/types/project'

export const projectApi = {
  getProjects() {
    return request.get<{ projects: Project[] }>('/projects').then(response => response.projects)
  },

  getProject(id: number) {
    return request.get<Project>(`/projects/${id}`)
  },

  createProject(data: Partial<Project>) {
    return request.post<Project>('/projects', data)
  },

  updateProject(id: number, data: Partial<Project>) {
    return request.put<Project>(`/projects/${id}`, data)
  },

  deleteProject(id: number) {
    return request.delete(`/projects/${id}`)
  },

  addProjectMember(id: number, userId: number) {
    return request.post(`/projects/${id}/members`, { user_id: userId })
  },

  removeProjectMember(id: number, userId: number) {
    return request.delete(`/projects/${id}/members/${userId}`)
  },

  getProjectMembers(id: number) {
    return request.get(`/projects/${id}/members`)
  },

  getTestSuites(projectId: number) {
    return request.get<TestSuite[]>(`/projects/${projectId}/test-suites`)
  },

  getTestCases(suiteId: number) {
    return request.get<TestCase[]>(`/test-suites/${suiteId}/test-cases`)
  }
} 