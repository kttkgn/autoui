<template>
  <div class="project-detail">
    <div class="header">
      <h2>项目详情</h2>
      <el-button-group>
        <el-button type="primary" @click="editProject">编辑</el-button>
        <el-button type="danger" @click="deleteProject">删除</el-button>
      </el-button-group>
    </div>

    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>{{ project?.name }}</span>
        </div>
      </template>
      <div class="info">
        <p><strong>描述：</strong>{{ project?.description || '暂无描述' }}</p>
        <p><strong>创建时间：</strong>{{ formatDate(project?.created_at) }}</p>
        <p><strong>更新时间：</strong>{{ formatDate(project?.updated_at) }}</p>
      </div>
    </el-card>

    <!-- 编辑项目对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="编辑项目"
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
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { useProjectStore } from '@/stores/project'
import type { Project } from '@/types/project'
import { formatDate } from '@/utils/date'

const route = useRoute()
const router = useRouter()
const projectStore = useProjectStore()
const loading = ref(false)
const dialogVisible = ref(false)
const project = ref<Project | null>(null)

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

onMounted(async () => {
  const projectId = Number(route.params.projectId)
  if (isNaN(projectId)) {
    ElMessage.error('无效的项目ID')
    router.push('/projects')
    return
  }
  await fetchProjectDetail(projectId)
})

async function fetchProjectDetail(id: number) {
  loading.value = true
  try {
    project.value = await projectStore.fetchProjectDetail(id)
  } catch (error) {
    ElMessage.error('获取项目详情失败')
    router.push('/projects')
  } finally {
    loading.value = false
  }
}

function editProject() {
  if (!project.value) return
  form.value = {
    name: project.value.name,
    description: project.value.description
  }
  dialogVisible.value = true
}

async function submitForm() {
  if (!formRef.value || !project.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await projectStore.updateProject(project.value.id, form.value)
        ElMessage.success('更新成功')
        dialogVisible.value = false
        await fetchProjectDetail(project.value.id)
      } catch (error) {
        ElMessage.error('更新失败')
      }
    }
  })
}

async function deleteProject() {
  if (!project.value) return
  
  try {
    await ElMessageBox.confirm('确定要删除该项目吗？', '提示', {
      type: 'warning'
    })
    await projectStore.deleteProject(project.value.id)
    ElMessage.success('删除成功')
    router.push('/projects')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}
</script>

<style scoped>
.project-detail {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.info {
  line-height: 2;
}

.info p {
  margin: 10px 0;
}
</style> 