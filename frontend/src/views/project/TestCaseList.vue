<template>
  <div class="test-case-list">
    <div class="header">
      <h2>测试用例列表</h2>
      <el-button type="primary" @click="showCreateDialog">创建测试用例</el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="testCases"
      style="width: 100%"
    >
      <el-table-column prop="name" label="用例名称" />
      <el-table-column prop="description" label="描述" />
      <el-table-column label="数据驱动">
        <template #default="{ row }">
          <el-tag v-if="row.data_driven?.enabled" type="success">启用</el-tag>
          <el-tag v-else type="info">禁用</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button-group>
            <el-button size="small" @click="viewTestCase(row)">查看</el-button>
            <el-button size="small" type="primary" @click="editTestCase(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteTestCase(row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑测试用例对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '创建测试用例' : '编辑测试用例'"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="用例名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
        <el-form-item label="数据驱动">
          <el-switch v-model="form.data_driven.enabled" />
        </el-form-item>
        <template v-if="form.data_driven.enabled">
          <el-form-item label="数据源" prop="data_driven.data_source">
            <el-input v-model="form.data_driven.data_source" placeholder="请输入数据源路径" />
          </el-form-item>
          <el-form-item label="参数" prop="data_driven.parameters">
            <el-select
              v-model="form.data_driven.parameters"
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
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { useTestCaseStore } from '@/stores/testCase'
import type { TestCase } from '@/types/project'
import { formatDate } from '@/utils/date'

const route = useRoute()
const router = useRouter()
const testCaseStore = useTestCaseStore()
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const currentTestCase = ref<TestCase | null>(null)

const formRef = ref<FormInstance>()
const form = ref({
  name: '',
  description: '',
  data_driven: {
    enabled: false,
    data_source: '',
    parameters: [] as string[]
  }
})

const rules = {
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

const testCases = ref<TestCase[]>([])
const availableParameters = ref<string[]>(['username', 'password', 'email', 'phone'])

onMounted(async () => {
  const testSuiteId = Number(route.params.testSuiteId)
  if (testSuiteId) {
    await fetchTestCases(testSuiteId)
  }
})

async function fetchTestCases(testSuiteId: number) {
  loading.value = true
  try {
    testCases.value = await testCaseStore.fetchTestCases(testSuiteId)
  } catch (error) {
    ElMessage.error('获取测试用例列表失败')
  } finally {
    loading.value = false
  }
}

function showCreateDialog() {
  dialogType.value = 'create'
  form.value = {
    name: '',
    description: '',
    data_driven: {
      enabled: false,
      data_source: '',
      parameters: []
    }
  }
  dialogVisible.value = true
}

function editTestCase(testCase: TestCase) {
  dialogType.value = 'edit'
  currentTestCase.value = testCase
  form.value = {
    name: testCase.name,
    description: testCase.description,
    data_driven: testCase.data_driven || {
      enabled: false,
      data_source: '',
      parameters: []
    }
  }
  dialogVisible.value = true
}

async function submitForm() {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const testSuiteId = Number(route.params.testSuiteId)
        if (dialogType.value === 'create') {
          await testCaseStore.createTestCase(testSuiteId, form.value)
          ElMessage.success('创建成功')
        } else {
          if (!currentTestCase.value) return
          await testCaseStore.updateTestCase(currentTestCase.value.id, form.value)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        await fetchTestCases(testSuiteId)
      } catch (error) {
        ElMessage.error(dialogType.value === 'create' ? '创建失败' : '更新失败')
      }
    }
  })
}

async function deleteTestCase(testCase: TestCase) {
  try {
    await ElMessageBox.confirm('确定要删除该测试用例吗？', '提示', {
      type: 'warning'
    })
    await testCaseStore.deleteTestCase(testCase.id)
    ElMessage.success('删除成功')
    const testSuiteId = Number(route.params.testSuiteId)
    await fetchTestCases(testSuiteId)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

function viewTestCase(testCase: TestCase) {
  router.push(`/test-cases/${testCase.id}`)
}
</script>

<style scoped>
.test-case-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 