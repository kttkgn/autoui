import request from '@/utils/request'
import type { TestCase } from '@/types/project'

export function getTestCases(testSuiteId: number) {
  return request.get<TestCase[]>(`/test-suites/${testSuiteId}/test-cases`)
}

export function getTestCaseDetail(id: number) {
  return request.get<TestCase>(`/test-cases/${id}`)
}

export function createTestCase(testSuiteId: number, data: Partial<TestCase>) {
  return request.post<TestCase>(`/test-suites/${testSuiteId}/test-cases`, data)
}

export function updateTestCase(id: number, data: Partial<TestCase>) {
  return request.put<TestCase>(`/test-cases/${id}`, data)
}

export function deleteTestCase(id: number) {
  return request.delete(`/test-cases/${id}`)
} 