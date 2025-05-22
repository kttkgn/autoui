<template>
  <div class="test-case-detail">
    <div class="header">
      <h2>测试用例详情</h2>
      <el-button-group>
        <el-button @click="goBack">返回</el-button>
        <el-button type="primary" @click="showEditDialog">编辑</el-button>
        <el-button type="success" :loading="executing" @click="executeTestCase">执行测试</el-button>
      </el-button-group>
    </div>

    <el-descriptions
      v-loading="loading"
      :column="2"
      border
    >
      <el-descriptions-item label="用例名称">{{ testCase?.name }}</el-descriptions-item>
      <el-descriptions-item label="创建时间">{{ formatDate(testCase?.created_at) }}</el-descriptions-item>
      <el-descriptions-item label="描述" :span="2">{{ testCase?.description }}</el-descriptions-item>
      <el-descriptions-item label="数据驱动">
        <el-tag v-if="testCase?.data_driven?.enabled" type="success">启用</el-tag>
        <el-tag v-else type="info">禁用</el-tag>
      </el-descriptions-item>
      <el-descriptions-item v-if="testCase?.data_driven?.enabled" label="数据源">
        {{ testCase?.data_driven?.data_source }}
      </el-descriptions-item>
    </el-descriptions>

    <div class="steps-section">
      <div class="steps-header">
        <h3>测试步骤</h3>
        <el-button type="primary" @click="showAddStepDialog">添加步骤</el-button>
      </div>

      <el-table
        v-loading="stepsLoading"
        :data="testSteps"
        row-key="step_number"
        border
        @row-drop="handleRowDrop"
      >
        <el-table-column label="步骤" width="80">
          <template #default="{ row }">
            <el-icon class="drag-handle"><Rank /></el-icon>
            {{ row.step_number }}
          </template>
        </el-table-column>
        <el-table-column prop="action" label="操作" />
        <el-table-column prop="element" label="元素" />
        <el-table-column prop="value" label="值" />
        <el-table-column label="操作" width="150">
          <template #default="{ row }">
            <el-button-group>
              <el-button size="small" @click="editStep(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleteStep(row)">删除</el-button>
            </el-button-group>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 编辑测试用例对话框 -->
    <el-dialog
      v-model="editDialogVisible"
      title="编辑测试用例"
      width="600px"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-width="100px"
      >
        <el-form-item label="用例名称" prop="name">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="editForm.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="数据驱动">
          <el-switch v-model="editForm.data_driven.enabled" />
        </el-form-item>
        <template v-if="editForm.data_driven.enabled">
          <el-form-item label="数据源" prop="data_driven.data_source">
            <el-input v-model="editForm.data_driven.data_source" placeholder="请输入数据源路径" />
          </el-form-item>
          <el-form-item label="参数" prop="data_driven.parameters">
            <el-select
              v-model="editForm.data_driven.parameters"
              multiple
              filterable
              allow-create
              default-first-option
              placeholder="请选择或输入参数"
            >
              <el-option
                v-for="param in availableParameters"
                :key="param"
                :label="param"
                :value="param"
              />
            </el-select>
          </el-form-item>
        </template>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEditForm">确定</el-button>
      </template>
    </el-dialog>

    <!-- 添加/编辑测试步骤对话框 -->
    <el-dialog
      v-model="stepDialogVisible"
      :title="stepDialogType === 'add' ? '添加测试步骤' : '编辑测试步骤'"
      width="500px"
    >
      <el-form
        ref="stepFormRef"
        :model="stepForm"
        :rules="stepRules"
        label-width="80px"
      >
        <el-form-item label="操作" prop="action">
          <el-select v-model="stepForm.action" placeholder="请选择操作">
            <el-option label="点击" value="click" />
            <el-option label="输入" value="input" />
            <el-option label="等待" value="wait" />
            <el-option label="断言" value="assert" />
          </el-select>
        </el-form-item>
        <el-form-item label="元素" prop="element">
          <el-input v-model="stepForm.element" placeholder="请输入元素定位表达式" />
        </el-form-item>
        <el-form-item label="值" prop="value">
          <el-input v-model="stepForm.value" placeholder="请输入操作值" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="stepDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitStepForm">确定</el-button>
      </template>
    </el-dialog>

    <div class="execution-section" v-if="currentExecution">
      <div class="execution-header">
        <h3>执行结果</h3>
        <el-tag :type="getExecutionStatusType(currentExecution.status)">
          {{ getExecutionStatusText(currentExecution.status) }}
        </el-tag>
      </div>
      
      <el-descriptions :column="2" border>
        <el-descriptions-item label="开始时间">
          {{ formatDate(currentExecution.start_time) }}
        </el-descriptions-item>
        <el-descriptions-item label="结束时间">
          {{ formatDate(currentExecution.end_time) }}
        </el-descriptions-item>
        <el-descriptions-item label="执行时长">
          {{ formatDuration(currentExecution.duration) }}
        </el-descriptions-item>
        <el-descriptions-item label="执行设备">
          {{ currentExecution.device_name }}
        </el-descriptions-item>
      </el-descriptions>

      <div v-if="executionResult" class="step-results">
        <h4>步骤执行结果</h4>
        <el-table :data="executionResult.step_results" border>
          <el-table-column prop="step_number" label="步骤" width="80" />
          <el-table-column prop="action" label="操作" />
          <el-table-column prop="element" label="元素" />
          <el-table-column prop="value" label="值" />
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 'success' ? 'success' : 'danger'">
                {{ row.status === 'success' ? '成功' : '失败' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="message" label="消息" />
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { Rank } from '@element-plus/icons-vue'
import { useTestCaseStore } from '@/stores/testCase'
import { useTestStepStore } from '@/stores/testStep'
import { useTestExecutionStore } from '@/stores/testExecution'
import type { TestCase, TestStep, TestExecution, TestExecutionResult } from '@/types/project'
import { formatDate } from '@/utils/date'
import Sortable from 'sortablejs'

const route = useRoute()
const router = useRouter()
const testCaseStore = useTestCaseStore()
const testStepStore = useTestStepStore()
const testExecutionStore = useTestExecutionStore()

const loading = ref(false)
const stepsLoading = ref(false)
const testCase = ref<TestCase | null>(null)
const testSteps = ref<TestStep[]>([])

// 编辑测试用例相关
const editDialogVisible = ref(false)
const editFormRef = ref<FormInstance>()
const editForm = ref({
  name: '',
  description: '',
  data_driven: {
    enabled: false,
    data_source: '',
    parameters: [] as string[]
  }
})

const editRules = {
  name: [
    { required: true, message: '请输入用例名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ],
  'data_driven.data_source': [
    { required: true, message: '请输入数据源路径', trigger: 'blur' }
  ],
  'data_driven.parameters': [
    { required: true, message: '请选择或输入参数', trigger: 'change' }
  ]
}

// 测试步骤相关
const stepDialogVisible = ref(false)
const stepDialogType = ref<'add' | 'edit'>('add')
const currentStep = ref<TestStep | null>(null)
const stepFormRef = ref<FormInstance>()
const stepForm = ref({
  action: '',
  element: '',
  value: ''
})

const stepRules = {
  action: [
    { required: true, message: '请选择操作', trigger: 'change' }
  ],
  element: [
    { required: true, message: '请输入元素定位表达式', trigger: 'blur' }
  ]
}

const availableParameters = ref<string[]>(['username', 'password', 'email', 'phone'])

const executing = ref(false)
const currentExecution = ref<TestExecution | null>(null)
const executionResult = ref<TestExecutionResult | null>(null)

onMounted(async () => {
  const testCaseId = Number(route.params.testCaseId)
  if (testCaseId) {
    await fetchTestCase(testCaseId)
    await fetchTestSteps(testCaseId)
    initSortable()
  }
})

async function fetchTestCase(testCaseId: number) {
  loading.value = true
  try {
    testCase.value = await testCaseStore.fetchTestCaseDetail(testCaseId)
  } catch (error) {
    ElMessage.error('获取测试用例详情失败')
  } finally {
    loading.value = false
  }
}

async function fetchTestSteps(testCaseId: number) {
  stepsLoading.value = true
  try {
    testSteps.value = await testStepStore.fetchTestSteps(testCaseId)
  } catch (error) {
    ElMessage.error('获取测试步骤列表失败')
  } finally {
    stepsLoading.value = false
  }
}

function goBack() {
  router.back()
}

function showEditDialog() {
  if (!testCase.value) return
  editForm.value = {
    name: testCase.value.name,
    description: testCase.value.description,
    data_driven: testCase.value.data_driven || {
      enabled: false,
      data_source: '',
      parameters: []
    }
  }
  editDialogVisible.value = true
}

async function submitEditForm() {
  if (!editFormRef.value || !testCase.value) return
  
  await editFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await testCaseStore.updateTestCase(testCase.value.id, editForm.value)
        ElMessage.success('更新成功')
        editDialogVisible.value = false
        await fetchTestCase(testCase.value.id)
      } catch (error) {
        ElMessage.error('更新失败')
      }
    }
  })
}

function showAddStepDialog() {
  stepDialogType.value = 'add'
  stepForm.value = {
    action: '',
    element: '',
    value: ''
  }
  stepDialogVisible.value = true
}

function editStep(step: TestStep) {
  stepDialogType.value = 'edit'
  currentStep.value = step
  stepForm.value = {
    action: step.action,
    element: step.element,
    value: step.value
  }
  stepDialogVisible.value = true
}

async function submitStepForm() {
  if (!stepFormRef.value || !testCase.value) return
  
  await stepFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (stepDialogType.value === 'add') {
          await testStepStore.createTestStep(testCase.value.id, stepForm.value)
          ElMessage.success('添加成功')
        } else {
          if (!currentStep.value) return
          await testStepStore.updateTestStep(
            testCase.value.id,
            currentStep.value.step_number,
            stepForm.value
          )
          ElMessage.success('更新成功')
        }
        stepDialogVisible.value = false
        await fetchTestSteps(testCase.value.id)
      } catch (error) {
        ElMessage.error(stepDialogType.value === 'add' ? '添加失败' : '更新失败')
      }
    }
  })
}

async function deleteStep(step: TestStep) {
  if (!testCase.value) return
  
  try {
    await ElMessageBox.confirm('确定要删除该测试步骤吗？', '提示', {
      type: 'warning'
    })
    await testStepStore.deleteTestStep(testCase.value.id, step.step_number)
    ElMessage.success('删除成功')
    await fetchTestSteps(testCase.value.id)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

function initSortable() {
  const tbody = document.querySelector('.el-table__body-wrapper tbody')
  if (tbody) {
    Sortable.create(tbody, {
      handle: '.drag-handle',
      animation: 150,
      onEnd({ newIndex, oldIndex }) {
        if (newIndex !== oldIndex) {
          const newSteps = [...testSteps.value]
          const [removed] = newSteps.splice(oldIndex, 1)
          newSteps.splice(newIndex, 0, removed)
          // 更新步骤顺序
          const stepNumbers = newSteps.map(step => step.step_number)
          reorderSteps(stepNumbers)
        }
      }
    })
  }
}

async function executeTestCase() {
  if (!testCase.value) return
  
  executing.value = true
  try {
    currentExecution.value = await testExecutionStore.executeTestCase(testCase.value.id)
    await pollExecutionResult()
  } catch (error) {
    ElMessage.error('执行测试失败')
  } finally {
    executing.value = false
  }
}

async function pollExecutionResult() {
  if (!currentExecution.value) return
  
  const maxAttempts = 60 // 最多等待60秒
  let attempts = 0
  
  while (attempts < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 1000))
    const result = await testExecutionStore.fetchExecutionResult(currentExecution.value.id)
    
    if (result.status !== 'running') {
      executionResult.value = result
      break
    }
    
    attempts++
  }
  
  if (attempts >= maxAttempts) {
    ElMessage.warning('执行超时，请稍后查看结果')
  }
}

function getExecutionStatusType(status: string) {
  switch (status) {
    case 'success':
      return 'success'
    case 'failed':
      return 'danger'
    case 'running':
      return 'warning'
    default:
      return 'info'
  }
}

function getExecutionStatusText(status: string) {
  switch (status) {
    case 'success':
      return '执行成功'
    case 'failed':
      return '执行失败'
    case 'running':
      return '执行中'
    default:
      return '未知状态'
  }
}

function formatDuration(seconds: number) {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}分${remainingSeconds}秒`
}
</script>

<style scoped>
.test-case-detail {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.steps-section {
  margin-top: 30px;
}

.steps-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.drag-handle {
  cursor: move;
  margin-right: 8px;
  color: #909399;
}

.drag-handle:hover {
  color: #409EFF;
}

.execution-section {
  margin-top: 30px;
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.execution-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.step-results {
  margin-top: 20px;
}

.step-results h4 {
  margin-bottom: 15px;
}
</style> 