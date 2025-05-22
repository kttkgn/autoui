<template>
  <div class="test-suite-list">
    <div class="header">
      <h2>测试套件列表</h2>
      <el-button type="primary" @click="showCreateDialog">创建测试套件</el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="testSuites"
      style="width: 100%"
    >
      <el-table-column prop="name" label="套件名称" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="created_at" label="创建时间">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button-group>
            <el-button size="small" @click="viewTestSuite(row)">查看</el-button>
            <el-button size="small" type="primary" @click="editTestSuite(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteTestSuite(row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑测试套件对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '创建测试套件' : '编辑测试套件'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="套件名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
          />
        </el-form-item>
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
import { useTestSuiteStore } from '@/stores/testSuite'
import type { TestSuite } from '@/types/project'
import { formatDate } from '@/utils/date'

const route = useRoute()
const router = useRouter()
const testSuiteStore = useTestSuiteStore()
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const currentTestSuite = ref<TestSuite | null>(null)

const formRef = ref<FormInstance>()
const form = ref({
  name: '',
  description: ''
})

const rules = {
  name: [
    { required: true, message: '请输入套件名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ]
}

const testSuites = ref<TestSuite[]>([])

onMounted(async () => {
  const projectId = Number(route.params.projectId)
  if (projectId) {
    await fetchTestSuites(projectId)
  }
})

async function fetchTestSuites(projectId: number) {
  loading.value = true
  try {
    testSuites.value = await testSuiteStore.fetchTestSuites(projectId)
  } catch (error) {
    ElMessage.error('获取测试套件列表失败')
  } finally {
    loading.value = false
  }
}

function showCreateDialog() {
  dialogType.value = 'create'
  form.value = {
    name: '',
    description: ''
  }
  dialogVisible.value = true
}

function editTestSuite(testSuite: TestSuite) {
  dialogType.value = 'edit'
  currentTestSuite.value = testSuite
  form.value = {
    name: testSuite.name,
    description: testSuite.description
  }
  dialogVisible.value = true
}

async function submitForm() {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        const projectId = Number(route.params.projectId)
        if (dialogType.value === 'create') {
          await testSuiteStore.createTestSuite(projectId, form.value)
          ElMessage.success('创建成功')
        } else {
          if (!currentTestSuite.value) return
          await testSuiteStore.updateTestSuite(currentTestSuite.value.id, form.value)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        await fetchTestSuites(projectId)
      } catch (error) {
        ElMessage.error(dialogType.value === 'create' ? '创建失败' : '更新失败')
      }
    }
  })
}

async function deleteTestSuite(testSuite: TestSuite) {
  try {
    await ElMessageBox.confirm('确定要删除该测试套件吗？', '提示', {
      type: 'warning'
    })
    await testSuiteStore.deleteTestSuite(testSuite.id)
    ElMessage.success('删除成功')
    const projectId = Number(route.params.projectId)
    await fetchTestSuites(projectId)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

function viewTestSuite(testSuite: TestSuite) {
  router.push(`/projects/${route.params.projectId}/test-suites/${testSuite.id}`)
}
</script>

<style scoped>
.test-suite-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 