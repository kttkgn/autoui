import request from '@/utils/request'
import type { TestSuite } from '@/types/project'

export function getTestSuites(projectId: number) {
  return request.get<TestSuite[]>(`/projects/${projectId}/test-suites`)
}

export function getTestSuiteDetail(id: number) {
  return request.get<TestSuite>(`/test-suites/${id}`)
}

export function createTestSuite(projectId: number, data: Partial<TestSuite>) {
  return request.post<TestSuite>(`/projects/${projectId}/test-suites`, data)
}

export function updateTestSuite(id: number, data: Partial<TestSuite>) {
  return request.put<TestSuite>(`/test-suites/${id}`, data)
}

export function deleteTestSuite(id: number) {
  return request.delete(`/test-suites/${id}`)
} 