import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Project } from '@/types/project'
import * as projectApi from '@/api/project'

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const loading = ref(false)

  async function fetchProjects() {
    loading.value = true
    try {
      const data = await projectApi.getProjects()
      projects.value = data
      return data
    } finally {
      loading.value = false
    }
  }

  async function fetchProjectDetail(id: number) {
    loading.value = true
    try {
      const data = await projectApi.getProject(id)
      currentProject.value = data
      return data
    } finally {
      loading.value = false
    }
  }

  async function createProject(project: Partial<Project>) {
    const data = await projectApi.createProject(project)
    projects.value.push(data)
    return data
  }

  async function updateProject(id: number, project: Partial<Project>) {
    const data = await projectApi.updateProject(id, project)
    const index = projects.value.findIndex(p => p.id === id)
    if (index !== -1) {
      projects.value[index] = data
    }
    if (currentProject.value?.id === id) {
      currentProject.value = data
    }
    return data
  }

  async function deleteProject(id: number) {
    await projectApi.deleteProject(id)
    const index = projects.value.findIndex(p => p.id === id)
    if (index !== -1) {
      projects.value.splice(index, 1)
    }
    if (currentProject.value?.id === id) {
      currentProject.value = null
    }
  }

  return {
    projects,
    currentProject,
    loading,
    fetchProjects,
    fetchProjectDetail,
    createProject,
    updateProject,
    deleteProject
  }
}) 