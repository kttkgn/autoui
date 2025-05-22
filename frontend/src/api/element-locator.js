import request from '@/utils/request'

// 连接设备
export function connectDevice(deviceId) {
  return request({
    url: `/api/v1/element-locator/${deviceId}/connect`,
    method: 'post'
  })
}

// 断开设备连接
export function disconnectDevice(deviceId) {
  return request({
    url: `/api/v1/element-locator/${deviceId}/disconnect`,
    method: 'post'
  })
}

// 获取屏幕尺寸
export function getScreenSize(deviceId) {
  return request({
    url: `/api/v1/element-locator/${deviceId}/screen-size`,
    method: 'get'
  })
}

// 获取屏幕截图
export function takeScreenshot(deviceId) {
  return request({
    url: `/api/v1/element-locator/${deviceId}/screenshot`,
    method: 'get',
    responseType: 'blob'
  })
}

// 获取元素树
export function getElementTree(deviceId) {
  return request({
    url: `/api/v1/element-locator/${deviceId}/element-tree`,
    method: 'get'
  })
}

// 查找元素
export function findElement(deviceId, locator) {
  return request({
    url: `/api/v1/element-locator/${deviceId}/find-element`,
    method: 'post',
    data: locator
  })
}

// 查找多个元素
export function findElements(deviceId, locator) {
  return request({
    url: `/api/v1/element-locator/${deviceId}/find-elements`,
    method: 'post',
    data: locator
  })
}

// 获取元素属性
export function getElementAttributes(deviceId, elementId) {
  return request({
    url: `/api/v1/element-locator/${deviceId}/elements/${elementId}/attributes`,
    method: 'get'
  })
}

// 点击元素
export function clickElement(deviceId, elementId) {
  return request({
    url: `/api/v1/element-locator/${deviceId}/elements/${elementId}/click`,
    method: 'post'
  })
}

// 输入文本
export function inputText(deviceId, elementId, text) {
  return request({
    url: `/api/v1/element-locator/${deviceId}/elements/${elementId}/input`,
    method: 'post',
    data: { text }
  })
} 