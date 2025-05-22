<template>
  <div class="project-list">
    <div class="header">
      <h2>项目列表</h2>
      <el-button type="primary" @click="showCreateDialog">创建项目</el-button>
    </div>

    <el-table
      v-loading="loading"
      :data="projects"
      style="width: 100%"
    >
      <el-table-column prop="name" label="项目名称" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="created_at" label="创建时间">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button-group>
            <el-button size="small" @click="viewProject(row)">查看</el-button>
            <el-button size="small" type="primary" @click="editProject(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteProject(row)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <!-- 创建/编辑项目对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogType === 'create' ? '创建项目' : '编辑项目'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="项目名称" prop="name">
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
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { useProjectStore } from '@/stores/project'
import type { Project } from '@/types/project'
import { formatDate } from '@/utils/date'

const router = useRouter()
const projectStore = useProjectStore()
const loading = ref(false)
const dialogVisible = ref(false)
const dialogType = ref<'create' | 'edit'>('create')
const currentProject = ref<Project | null>(null)

const formRef = ref<FormInstance>()
const form = ref({
  name: '',
  description: ''
})

const rules = {
  name: [
    { required: true, message: '请输入项目名称', trigger: 'blur' },
    { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
  ]
}

const projects = ref<Project[]>([])

onMounted(async () => {
  await fetchProjects()
})

async function fetchProjects() {
  loading.value = true
  try {
    projects.value = await projectStore.fetchProjects()
  } catch (error) {
    ElMessage.error('获取项目列表失败')
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

function editProject(project: Project) {
  dialogType.value = 'edit'
  currentProject.value = project
  form.value = {
    name: project.name,
    description: project.description
  }
  dialogVisible.value = true
}

async function submitForm() {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (dialogType.value === 'create') {
          await projectStore.createProject(form.value)
          ElMessage.success('创建成功')
        } else {
          if (!currentProject.value) return
          await projectStore.updateProject(currentProject.value.id, form.value)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        await fetchProjects()
      } catch (error) {
        ElMessage.error(dialogType.value === 'create' ? '创建失败' : '更新失败')
      }
    }
  })
}

async function deleteProject(project: Project) {
  try {
    await ElMessageBox.confirm('确定要删除该项目吗？', '提示', {
      type: 'warning'
    })
    await projectStore.deleteProject(project.id)
    ElMessage.success('删除成功')
    await fetchProjects()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

function viewProject(project: Project) {
  router.push(`/projects/${project.id}`)
}
</script>

<style scoped>
.project-list {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
</style> 