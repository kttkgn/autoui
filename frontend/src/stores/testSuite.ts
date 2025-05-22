import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TestSuite } from '@/types/project'
import * as testSuiteApi from '@/api/testSuite'

export const useTestSuiteStore = defineStore('testSuite', () => {
  const testSuites = ref<TestSuite[]>([])
  const currentTestSuite = ref<TestSuite | null>(null)
  const loading = ref(false)

  async function fetchTestSuites(projectId: number) {
    loading.value = true
    try {
      const data = await testSuiteApi.getTestSuites(projectId)
      testSuites.value = data
      return data
    } finally {
      loading.value = false
    }
  }

  async function fetchTestSuiteDetail(id: number) {
    loading.value = true
    try {
      const data = await testSuiteApi.getTestSuiteDetail(id)
      currentTestSuite.value = data
      return data
    } finally {
      loading.value = false
    }
  }

  async function createTestSuite(projectId: number, testSuite: Partial<TestSuite>) {
    const data = await testSuiteApi.createTestSuite(projectId, testSuite)
    testSuites.value.push(data)
    return data
  }

  async function updateTestSuite(id: number, testSuite: Partial<TestSuite>) {
    const data = await testSuiteApi.updateTestSuite(id, testSuite)
    const index = testSuites.value.findIndex(ts => ts.id === id)
    if (index !== -1) {
      testSuites.value[index] = data
    }
    if (currentTestSuite.value?.id === id) {
      currentTestSuite.value = data
    }
    return data
  }

  async function deleteTestSuite(id: number) {
    await testSuiteApi.deleteTestSuite(id)
    const index = testSuites.value.findIndex(ts => ts.id === id)
    if (index !== -1) {
      testSuites.value.splice(index, 1)
    }
    if (currentTestSuite.value?.id === id) {
      currentTestSuite.value = null
    }
  }

  return {
    testSuites,
    currentTestSuite,
    loading,
    fetchTestSuites,
    fetchTestSuiteDetail,
    createTestSuite,
    updateTestSuite,
    deleteTestSuite
  }
}) 