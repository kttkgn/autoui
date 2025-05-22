<template>
  <div class="element-locator">
    <div class="screen-container">
      <canvas ref="screenCanvas" @click="handleScreenClick"></canvas>
      <div class="element-info" v-if="selectedElement">
        <h3>元素信息</h3>
        <div class="info-item" v-for="(value, key) in selectedElement.attributes" :key="key">
          <span class="label">{{ key }}:</span>
          <span class="value">{{ value }}</span>
        </div>
        <div class="actions">
          <el-button type="primary" @click="handleCopyLocator">复制定位器</el-button>
          <el-button @click="handleClickElement">点击元素</el-button>
          <el-button @click="handleInputText">输入文本</el-button>
        </div>
      </div>
    </div>
    
    <div class="element-tree">
      <h3>元素树</h3>
      <el-tree
        :data="elementTree"
        :props="defaultProps"
        @node-click="handleNodeClick"
      >
        <template #default="{ node, data }">
          <span class="custom-tree-node">
            <span>{{ node.label }}</span>
            <span class="node-type">{{ data.type }}</span>
          </span>
        </template>
      </el-tree>
    </div>
    
    <!-- 输入文本对话框 -->
    <el-dialog
      v-model="inputDialogVisible"
      title="输入文本"
      width="400px"
    >
      <el-form>
        <el-form-item label="文本内容">
          <el-input v-model="inputText" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="inputDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleConfirmInput">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRoute } from 'vue-router'
import {
  connectDevice,
  disconnectDevice,
  getElementTree,
  clickElement,
  inputText
} from '@/api/element-locator'

const props = defineProps({
  deviceId: {
    type: Number,
    required: true
  }
})

const route = useRoute()
const screenCanvas = ref(null)
const elementTree = ref([])
const selectedElement = ref(null)
const inputDialogVisible = ref(false)
const inputText = ref('')
const ws = ref(null)

const defaultProps = {
  children: 'children',
  label: 'name'
}

// 连接设备
const connect = async () => {
  try {
    await connectDevice(props.deviceId)
    startScreenStream()
    fetchElementTree()
  } catch (error) {
    ElMessage.error('设备连接失败')
  }
}

// 断开连接
const disconnect = async () => {
  try {
    await disconnectDevice(props.deviceId)
    stopScreenStream()
  } catch (error) {
    ElMessage.error('设备断开连接失败')
  }
}

// 启动屏幕流
const startScreenStream = () => {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const wsUrl = `${protocol}//${window.location.host}/api/v1/element-locator/${props.deviceId}/screen-stream`
  
  ws.value = new WebSocket(wsUrl)
  ws.value.binaryType = 'arraybuffer'
  
  ws.value.onmessage = (event) => {
    const blob = new Blob([event.data], { type: 'image/png' })
    const url = URL.createObjectURL(blob)
    const img = new Image()
    
    img.onload = () => {
      const canvas = screenCanvas.value
      const ctx = canvas.getContext('2d')
      
      canvas.width = img.width
      canvas.height = img.height
      ctx.drawImage(img, 0, 0)
      
      URL.revokeObjectURL(url)
    }
    
    img.src = url
  }
  
  ws.value.onerror = (error) => {
    console.error('WebSocket错误:', error)
    ElMessage.error('屏幕流连接失败')
  }
  
  ws.value.onclose = () => {
    console.log('WebSocket连接已关闭')
  }
}

// 停止屏幕流
const stopScreenStream = () => {
  if (ws.value) {
    ws.value.close()
    ws.value = null
  }
}

// 获取元素树
const fetchElementTree = async () => {
  try {
    const tree = await getElementTree(props.deviceId)
    elementTree.value = tree
  } catch (error) {
    ElMessage.error('获取元素树失败')
  }
}

// 处理屏幕点击
const handleScreenClick = async (event) => {
  const canvas = screenCanvas.value
  const rect = canvas.getBoundingClientRect()
  const x = event.clientX - rect.left
  const y = event.clientY - rect.top
  
  // TODO: 实现点击坐标转换为元素
}

// 处理节点点击
const handleNodeClick = (data) => {
  selectedElement.value = data
}

// 复制定位器
const handleCopyLocator = () => {
  if (!selectedElement.value) return
  
  const locator = {
    type: selectedElement.value.type,
    attributes: selectedElement.value.attributes
  }
  
  navigator.clipboard.writeText(JSON.stringify(locator))
    .then(() => {
      ElMessage.success('定位器已复制到剪贴板')
    })
    .catch(() => {
      ElMessage.error('复制失败')
    })
}

// 点击元素
const handleClickElement = async () => {
  if (!selectedElement.value) return
  
  try {
    await clickElement(props.deviceId, selectedElement.value.id)
    ElMessage.success('点击成功')
  } catch (error) {
    ElMessage.error('点击失败')
  }
}

// 显示输入文本对话框
const handleInputText = () => {
  if (!selectedElement.value) return
  inputDialogVisible.value = true
}

// 确认输入文本
const handleConfirmInput = async () => {
  if (!selectedElement.value || !inputText.value) return
  
  try {
    await inputText(props.deviceId, selectedElement.value.id, inputText.value)
    ElMessage.success('输入成功')
    inputDialogVisible.value = false
    inputText.value = ''
  } catch (error) {
    ElMessage.error('输入失败')
  }
}

onMounted(() => {
  connect()
})

onUnmounted(() => {
  disconnect()
})
</script>

<style scoped>
.element-locator {
  display: flex;
  height: 100%;
  padding: 20px;
  gap: 20px;
}

.screen-container {
  flex: 1;
  position: relative;
  background: #000;
  border-radius: 4px;
  overflow: hidden;
}

.screen-container canvas {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.element-info {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(255, 255, 255, 0.9);
  padding: 15px;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  max-width: 300px;
}

.info-item {
  margin-bottom: 8px;
}

.info-item .label {
  font-weight: bold;
  margin-right: 8px;
}

.info-item .value {
  color: #666;
}

.actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
}

.element-tree {
  width: 300px;
  background: #fff;
  border-radius: 4px;
  padding: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.custom-tree-node {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.node-type {
  color: #999;
  font-size: 12px;
}
</style> 