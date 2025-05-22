import request from '@/utils/request'

// 获取设备列表
export function getDevices(params) {
  return request({
    url: '/api/v1/devices',
    method: 'get',
    params
  })
}

// 检测设备
export function detectDevices() {
  return request({
    url: '/api/v1/devices/detect',
    method: 'post'
  })
}

// 创建设备
export function createDevice(data) {
  return request({
    url: '/api/v1/devices',
    method: 'post',
    data
  })
}

// 更新设备
export function updateDevice(id, data) {
  return request({
    url: `/api/v1/devices/${id}`,
    method: 'put',
    data
  })
}

// 删除设备
export function deleteDevice(id) {
  return request({
    url: `/api/v1/devices/${id}`,
    method: 'delete'
  })
}

// 添加设备属性
export function addDeviceProperty(deviceId, data) {
  return request({
    url: `/api/v1/devices/${deviceId}/properties`,
    method: 'post',
    data
  })
}

// 更新设备属性
export function updateDeviceProperty(propertyId, data) {
  return request({
    url: `/api/v1/devices/properties/${propertyId}`,
    method: 'put',
    data
  })
}

// 删除设备属性
export function deleteDeviceProperty(propertyId) {
  return request({
    url: `/api/v1/devices/properties/${propertyId}`,
    method: 'delete'
  })
} 