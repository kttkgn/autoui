import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TestStep } from '@/types/project'
import { testStepApi } from '@/api/testStep'

export const useTestStepStore = defineStore('testStep', () => {
  const testSteps = ref<TestStep[]>([])
  const loading = ref(false)

  async function fetchTestSteps(testCaseId: number) {
    loading.value = true
    try {
      const response = await testStepApi.getTestSteps(testCaseId)
      testSteps.value = response
      return response
    } finally {
      loading.value = false
    }
  }

  async function createTestStep(testCaseId: number, testStep: Partial<TestStep>) {
    const response = await testStepApi.createTestStep(testCaseId, testStep)
    testSteps.value.push(response)
    return response
  }

  async function updateTestStep(testCaseId: number, stepNumber: number, testStep: Partial<TestStep>) {
    const response = await testStepApi.updateTestStep(testCaseId, stepNumber, testStep)
    const index = testSteps.value.findIndex(step => step.step_number === stepNumber)
    if (index !== -1) {
      testSteps.value[index] = response
    }
    return response
  }

  async function deleteTestStep(testCaseId: number, stepNumber: number) {
    await testStepApi.deleteTestStep(testCaseId, stepNumber)
    testSteps.value = testSteps.value.filter(step => step.step_number !== stepNumber)
  }

  async function reorderTestSteps(testCaseId: number, stepNumbers: number[]) {
    await testStepApi.reorderTestSteps(testCaseId, stepNumbers)
    await fetchTestSteps(testCaseId)
  }

  return {
    testSteps,
    loading,
    fetchTestSteps,
    createTestStep,
    updateTestStep,
    deleteTestStep,
    reorderTestSteps
  }
}) 