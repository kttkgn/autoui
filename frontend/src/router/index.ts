import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/projects'
  },
  {
    path: '/projects',
    name: 'ProjectList',
    component: () => import('@/views/project/ProjectList.vue')
  },
  {
    path: '/projects/:projectId',
    name: 'ProjectDetail',
    component: () => import('@/views/project/ProjectDetail.vue')
  },
  {
    path: '/projects/:projectId/test-suites',
    name: 'TestSuiteList',
    component: () => import('@/views/project/TestSuiteList.vue')
  },
  {
    path: '/test-suites/:testSuiteId/test-cases',
    name: 'TestCaseList',
    component: () => import('@/views/project/TestCaseList.vue')
  },
  {
    path: '/test-cases/:testCaseId',
    name: 'TestCaseDetail',
    component: () => import('@/views/project/TestCaseDetail.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 