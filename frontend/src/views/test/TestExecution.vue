<template>
  <div class="test-execution">
    <div class="header">
      <h2>测试执行</h2>
      <div class="actions">
        <el-button type="primary" @click="handleStart" :loading="loading">
          开始执行
        </el-button>
        <el-button @click="handleStop" :disabled="!isRunning">
          停止执行
        </el-button>
      </div>
    </div>
    
    <el-tabs v-model="activeTab">
      <el-tab-pane label="执行详情" name="details">
        <div class="execution-details">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="测试用例">
              {{ execution?.test_case?.name }}
            </el-descriptions-item>
            <el-descriptions-item label="设备">
              {{ execution?.device?.name }}
            </el-descriptions-item>
            <el-descriptions-item label="状态">
              <el-tag :type="getStatusType(execution?.status)">
                {{ getStatusText(execution?.status) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="开始时间">
              {{ formatDateTime(execution?.start_time) }}
            </el-descriptions-item>
            <el-descriptions-item label="结束时间">
              {{ formatDateTime(execution?.end_time) }}
            </el-descriptions-item>
            <el-descriptions-item label="错误信息" v-if="execution?.error_message">
              {{ execution.error_message }}
            </el-descriptions-item>
          </el-descriptions>
        </div>
      </el-tab-pane>
      
      <el-tab-pane label="步骤结果" name="steps">
        <div class="step-results">
          <el-timeline>
            <el-timeline-item
              v-for="step in stepResults"
              :key="step.id"
              :type="getStepStatusType(step.status)"
              :timestamp="formatDateTime(step.start_time)"
            >
              <div class="step-item">
                <div class="step-header">
                  <span class="step-name">{{ step.test_step?.name }}</span>
                  <el-tag :type="getStepStatusType(step.status)" size="small">
                    {{ getStepStatusText(step.status) }}
                  </el-tag>
                </div>
                
                <div class="step-content">
                  <div class="step-info">
                    <p class="step-description">{{ step.test_step?.description }}</p>
                    <p class="step-message" v-if="step.message">{{ step.message }}</p>
                  </div>
                  
                  <div class="step-screenshot" v-if="step.screenshot">
                    <img :src="step.screenshot" alt="步骤截图" />
                  </div>
                </div>
              </div>
            </el-timeline-item>
          </el-timeline>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  getExecution,
  getStepResults,
  startExecution,
  stopExecution
} from '@/api/test-execution'
import { formatDateTime } from '@/utils/format'

const route = useRoute()
const executionId = route.params.id

const loading = ref(false)
const isRunning = ref(false)
const activeTab = ref('details')
const execution = ref(null)
const stepResults = ref([])
const timer = ref(null)

// 获取执行记录
const fetchExecution = async () => {
  try {
    const data = await getExecution(executionId)
    execution.value = data
    isRunning.value = data.status === 'running'
  } catch (error) {
    ElMessage.error('获取执行记录失败')
  }
}

// 获取步骤结果
const fetchStepResults = async () => {
  try {
    const data = await getStepResults(executionId)
    stepResults.value = data
  } catch (error) {
    ElMessage.error('获取步骤结果失败')
  }
}

// 开始执行
const handleStart = async () => {
  try {
    loading.value = true
    await startExecution(executionId)
    ElMessage.success('测试执行已开始')
    isRunning.value = true
    startPolling()
  } catch (error) {
    ElMessage.error('开始执行失败')
  } finally {
    loading.value = false
  }
}

// 停止执行
const handleStop = async () => {
  try {
    await stopExecution(executionId)
    ElMessage.success('测试执行已停止')
    isRunning.value = false
    stopPolling()
  } catch (error) {
    ElMessage.error('停止执行失败')
  }
}

// 开始轮询
const startPolling = () => {
  timer.value = setInterval(() => {
    fetchExecution()
    fetchStepResults()
  }, 2000)
}

// 停止轮询
const stopPolling = () => {
  if (timer.value) {
    clearInterval(timer.value)
    timer.value = null
  }
}

// 获取状态类型
const getStatusType = (status) => {
  const types = {
    created: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger',
    stopped: 'info'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status) => {
  const texts = {
    created: '已创建',
    running: '执行中',
    completed: '已完成',
    failed: '失败',
    stopped: '已停止'
  }
  return texts[status] || status
}

// 获取步骤状态类型
const getStepStatusType = (status) => {
  const types = {
    passed: 'success',
    failed: 'danger'
  }
  return types[status] || 'info'
}

// 获取步骤状态文本
const getStepStatusText = (status) => {
  const texts = {
    passed: '通过',
    failed: '失败'
  }
  return texts[status] || status
}

onMounted(() => {
  fetchExecution()
  fetchStepResults()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.test-execution {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.execution-details {
  margin-top: 20px;
}

.step-results {
  margin-top: 20px;
}

.step-item {
  padding: 10px;
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.step-name {
  font-weight: bold;
}

.step-content {
  display: flex;
  gap: 20px;
}

.step-info {
  flex: 1;
}

.step-description {
  color: #666;
  margin-bottom: 10px;
}

.step-message {
  color: #f56c6c;
}

.step-screenshot {
  width: 200px;
  height: 150px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
}

.step-screenshot img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
</style> 