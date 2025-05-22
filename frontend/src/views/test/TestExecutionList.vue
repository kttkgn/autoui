<template>
  <div class="test-execution-list">
    <div class="header">
      <h2>测试执行记录</h2>
      <div class="actions">
        <el-button type="primary" @click="handleCreate">
          新建执行
        </el-button>
      </div>
    </div>

    <el-card class="filter-card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="测试用例">
          <el-select
            v-model="filterForm.testCaseId"
            placeholder="选择测试用例"
            clearable
            @change="handleFilter"
          >
            <el-option
              v-for="item in testCases"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="设备">
          <el-select
            v-model="filterForm.deviceId"
            placeholder="选择设备"
            clearable
            @change="handleFilter"
          >
            <el-option
              v-for="item in devices"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select
            v-model="filterForm.status"
            placeholder="选择状态"
            clearable
            @change="handleFilter"
          >
            <el-option label="已创建" value="created" />
            <el-option label="执行中" value="running" />
            <el-option label="已完成" value="completed" />
            <el-option label="失败" value="failed" />
            <el-option label="已停止" value="stopped" />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleFilter">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-table
      v-loading="loading"
      :data="executions"
      style="width: 100%"
    >
      <el-table-column prop="test_case.name" label="测试用例" />
      <el-table-column prop="device.name" label="设备" />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="开始时间" width="180">
        <template #default="{ row }">
          {{ formatDateTime(row.start_time) }}
        </template>
      </el-table-column>
      <el-table-column label="结束时间" width="180">
        <template #default="{ row }">
          {{ formatDateTime(row.end_time) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button
            link
            type="primary"
            @click="handleView(row)"
          >
            查看
          </el-button>
          <el-button
            v-if="row.status === 'created'"
            link
            type="primary"
            @click="handleStart(row)"
          >
            开始
          </el-button>
          <el-button
            v-if="row.status === 'running'"
            link
            type="danger"
            @click="handleStop(row)"
          >
            停止
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="page"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <!-- 新建执行对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="新建测试执行"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="测试用例" prop="testCaseId">
          <el-select
            v-model="form.testCaseId"
            placeholder="选择测试用例"
          >
            <el-option
              v-for="item in testCases"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="设备" prop="deviceId">
          <el-select
            v-model="form.deviceId"
            placeholder="选择设备"
          >
            <el-option
              v-for="item in devices"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  createExecution,
  startExecution,
  stopExecution
} from '@/api/test-execution'
import { getTestCases } from '@/api/test-case'
import { getDevices } from '@/api/device'
import { formatDateTime } from '@/utils/format'

const router = useRouter()

// 数据列表
const loading = ref(false)
const executions = ref([])
const testCases = ref([])
const devices = ref([])

// 分页
const page = ref(1)
const pageSize = ref(10)
const total = ref(0)

// 筛选表单
const filterForm = ref({
  testCaseId: '',
  deviceId: '',
  status: ''
})

// 新建表单
const dialogVisible = ref(false)
const formRef = ref(null)
const form = ref({
  testCaseId: '',
  deviceId: ''
})

// 表单验证规则
const rules = {
  testCaseId: [
    { required: true, message: '请选择测试用例', trigger: 'change' }
  ],
  deviceId: [
    { required: true, message: '请选择设备', trigger: 'change' }
  ]
}

// 获取测试用例列表
const fetchTestCases = async () => {
  try {
    const data = await getTestCases()
    testCases.value = data
  } catch (error) {
    ElMessage.error('获取测试用例列表失败')
  }
}

// 获取设备列表
const fetchDevices = async () => {
  try {
    const data = await getDevices()
    devices.value = data
  } catch (error) {
    ElMessage.error('获取设备列表失败')
  }
}

// 获取执行记录列表
const fetchExecutions = async () => {
  try {
    loading.value = true
    const params = {
      page: page.value,
      page_size: pageSize.value,
      ...filterForm.value
    }
    const { items, total: totalCount } = await getExecutions(params)
    executions.value = items
    total.value = totalCount
  } catch (error) {
    ElMessage.error('获取执行记录列表失败')
  } finally {
    loading.value = false
  }
}

// 处理筛选
const handleFilter = () => {
  page.value = 1
  fetchExecutions()
}

// 重置筛选
const resetFilter = () => {
  filterForm.value = {
    testCaseId: '',
    deviceId: '',
    status: ''
  }
  handleFilter()
}

// 处理分页
const handleSizeChange = (val) => {
  pageSize.value = val
  fetchExecutions()
}

const handleCurrentChange = (val) => {
  page.value = val
  fetchExecutions()
}

// 查看详情
const handleView = (row) => {
  router.push(`/test/executions/${row.id}`)
}

// 开始执行
const handleStart = async (row) => {
  try {
    await startExecution(row.id)
    ElMessage.success('测试执行已开始')
    fetchExecutions()
  } catch (error) {
    ElMessage.error('开始执行失败')
  }
}

// 停止执行
const handleStop = async (row) => {
  try {
    await stopExecution(row.id)
    ElMessage.success('测试执行已停止')
    fetchExecutions()
  } catch (error) {
    ElMessage.error('停止执行失败')
  }
}

// 新建执行
const handleCreate = () => {
  form.value = {
    testCaseId: '',
    deviceId: ''
  }
  dialogVisible.value = true
}

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    await createExecution(form.value)
    ElMessage.success('创建成功')
    dialogVisible.value = false
    fetchExecutions()
  } catch (error) {
    if (error.message) {
      ElMessage.error(error.message)
    }
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

onMounted(() => {
  fetchTestCases()
  fetchDevices()
  fetchExecutions()
})
</script>

<style scoped>
.test-execution-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style> 