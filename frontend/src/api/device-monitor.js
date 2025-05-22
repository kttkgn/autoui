import request from '@/utils/request'

// 启动设备监控
export function startMonitor(deviceId) {
  return request({
    url: `/api/v1/devices/${deviceId}/monitor/start`,
    method: 'post'
  })
}

// 停止设备监控
export function stopMonitor(deviceId) {
  return request({
    url: `/api/v1/devices/${deviceId}/monitor/stop`,
    method: 'post'
  })
} 