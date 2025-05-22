import request from '@/utils/request'
import type { TestStep } from '@/types/project'

export const testStepApi = {
  getTestSteps(testCaseId: number) {
    return request.get<TestStep[]>(`/test-steps/${testCaseId}`)
  },

  createTestStep(testCaseId: number, data: Partial<TestStep>) {
    return request.post<TestStep>(`/test-steps/${testCaseId}`, data)
  },

  updateTestStep(testCaseId: number, stepNumber: number, data: Partial<TestStep>) {
    return request.put<TestStep>(`/test-steps/${testCaseId}/${stepNumber}`, data)
  },

  deleteTestStep(testCaseId: number, stepNumber: number) {
    return request.delete(`/test-steps/${testCaseId}/${stepNumber}`)
  },

  reorderTestSteps(testCaseId: number, stepNumbers: number[]) {
    return request.put(`/test-steps/${testCaseId}/reorder`, { step_numbers: stepNumbers })
  }
} 