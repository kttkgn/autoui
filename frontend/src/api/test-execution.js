import request from '@/utils/request'

// 获取测试执行记录
export function getExecution(id) {
  return request({
    url: `/api/v1/test-executions/${id}`,
    method: 'get'
  })
}

// 获取测试步骤结果
export function getStepResults(executionId) {
  return request({
    url: `/api/v1/test-executions/${executionId}/step-results`,
    method: 'get'
  })
}

// 开始执行测试
export function startExecution(id) {
  return request({
    url: `/api/v1/test-executions/${id}/start`,
    method: 'post'
  })
}

// 停止执行测试
export function stopExecution(id) {
  return request({
    url: `/api/v1/test-executions/${id}/stop`,
    method: 'post'
  })
}

// 创建测试执行记录
export function createExecution(data) {
  return request({
    url: '/api/v1/test-executions',
    method: 'post',
    data
  })
}

// 获取测试用例的执行历史
export function getTestCaseExecutions(testCaseId, params) {
  return request({
    url: `/api/v1/test-cases/${testCaseId}/executions`,
    method: 'get',
    params
  })
}

// 获取设备的执行历史
export function getDeviceExecutions(deviceId, params) {
  return request({
    url: `/api/v1/devices/${deviceId}/executions`,
    method: 'get',
    params
  })
} 