import request from '@/utils/request'
import type { TestExecution, TestExecutionResult, TestExecutionSummary } from '@/types/project'

export const testExecutionApi = {
  executeTestCase(testCaseId: number) {
    return request.post<TestExecution>(`/test-executions/${testCaseId}`)
  },

  getExecutionResult(executionId: number) {
    return request.get<TestExecutionResult>(`/test-executions/${executionId}/result`)
  },

  getExecutionHistory(testCaseId: number) {
    return request.get<TestExecution[]>(`/test-executions/${testCaseId}/history`)
  },

  getProjectExecutionSummary(projectId: number) {
    return request<TestExecutionSummary>({
      url: `/test-executions/project/${projectId}/summary`,
      method: 'get'
    })
  }
} 