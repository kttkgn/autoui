<template>
  <div class="device-list">
    <div class="header">
      <h2>设备管理</h2>
      <div class="actions">
        <el-button type="primary" @click="handleDetectDevices" :loading="detecting">
          检测设备
        </el-button>
      </div>
    </div>

    <el-table
      v-loading="loading"
      :data="devices"
      style="width: 100%"
    >
      <el-table-column prop="name" label="设备名称" />
      <el-table-column prop="type" label="设备类型">
        <template #default="{ row }">
          <el-tag :type="getDeviceTypeTag(row.type)">
            {{ getDeviceTypeLabel(row.type) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="getStatusTag(row.status)">
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="属性">
        <template #default="{ row }">
          <el-popover
            placement="right"
            :width="300"
            trigger="hover"
          >
            <template #reference>
              <el-button link>查看属性</el-button>
            </template>
            <div class="device-properties">
              <div
                v-for="prop in row.properties"
                :key="prop.key"
                class="property-item"
              >
                <span class="property-key">{{ prop.key }}:</span>
                <span class="property-value">{{ prop.value }}</span>
              </div>
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button
            link
            type="primary"
            @click="handleStartMonitor(row)"
            v-if="!row.monitoring"
          >
            启动监控
          </el-button>
          <el-button
            link
            type="danger"
            @click="handleStopMonitor(row)"
            v-else
          >
            停止监控
          </el-button>
          <el-button
            link
            type="primary"
            @click="handleEdit(row)"
          >
            编辑
          </el-button>
          <el-button
            link
            type="danger"
            @click="handleDelete(row)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑设备对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="编辑设备"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="设备名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="设备类型" prop="type">
          <el-select v-model="form.type" style="width: 100%">
            <el-option label="Android" value="android" />
            <el-option label="iOS" value="ios" />
            <el-option label="Web" value="web" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSave">
            保存
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getDevices, detectDevices, updateDevice, deleteDevice } from '@/api/device'
import { startMonitor, stopMonitor } from '@/api/device-monitor'

const loading = ref(false)
const detecting = ref(false)
const devices = ref([])
const dialogVisible = ref(false)
const formRef = ref(null)
const form = ref({
  id: null,
  name: '',
  type: ''
})

const rules = {
  name: [
    { required: true, message: '请输入设备名称', trigger: 'blur' }
  ],
  type: [
    { required: true, message: '请选择设备类型', trigger: 'change' }
  ]
}

// 获取设备列表
const fetchDevices = async () => {
  loading.value = true
  try {
    const response = await getDevices()
    devices.value = response.items
  } catch (error) {
    ElMessage.error('获取设备列表失败')
  } finally {
    loading.value = false
  }
}

// 检测设备
const handleDetectDevices = async () => {
  detecting.value = true
  try {
    const detectedDevices = await detectDevices()
    ElMessage.success(`检测到 ${detectedDevices.length} 个设备`)
    await fetchDevices()
  } catch (error) {
    ElMessage.error('检测设备失败')
  } finally {
    detecting.value = false
  }
}

// 启动监控
const handleStartMonitor = async (row) => {
  try {
    await startMonitor(row.id)
    ElMessage.success('设备监控已启动')
    row.monitoring = true
  } catch (error) {
    ElMessage.error('启动设备监控失败')
  }
}

// 停止监控
const handleStopMonitor = async (row) => {
  try {
    await stopMonitor(row.id)
    ElMessage.success('设备监控已停止')
    row.monitoring = false
  } catch (error) {
    ElMessage.error('停止设备监控失败')
  }
}

// 编辑设备
const handleEdit = (row) => {
  form.value = {
    id: row.id,
    name: row.name,
    type: row.type
  }
  dialogVisible.value = true
}

// 保存设备
const handleSave = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await updateDevice(form.value.id, form.value)
        ElMessage.success('保存成功')
        dialogVisible.value = false
        await fetchDevices()
      } catch (error) {
        ElMessage.error('保存失败')
      }
    }
  })
}

// 删除设备
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除该设备吗？',
      '警告',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    
    await deleteDevice(row.id)
    ElMessage.success('删除成功')
    await fetchDevices()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 获取设备类型标签
const getDeviceTypeTag = (type) => {
  const tags = {
    android: 'success',
    ios: 'warning',
    web: 'info'
  }
  return tags[type] || 'info'
}

// 获取设备类型标签文本
const getDeviceTypeLabel = (type) => {
  const labels = {
    android: 'Android',
    ios: 'iOS',
    web: 'Web'
  }
  return labels[type] || type
}

// 获取状态标签
const getStatusTag = (status) => {
  const tags = {
    online: 'success',
    offline: 'danger',
    busy: 'warning'
  }
  return tags[status] || 'info'
}

// 获取状态标签文本
const getStatusLabel = (status) => {
  const labels = {
    online: '在线',
    offline: '离线',
    busy: '忙碌'
  }
  return labels[status] || status
}

onMounted(() => {
  fetchDevices()
})
</script>

<style scoped>
.device-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.device-properties {
  padding: 10px;
}

.property-item {
  margin-bottom: 8px;
}

.property-key {
  font-weight: bold;
  margin-right: 8px;
}

.property-value {
  color: #666;
}
</style> 