export interface Project {
  id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface TestSuite {
  id: number
  project_id: number
  name: string
  description?: string
  created_at: string
  updated_at: string
}

export interface TestStep {
  id: number
  test_case_id: number
  step_number: number
  action: string
  element: string
  value?: string
  created_at: string
  updated_at: string
}

export interface TestCase {
  id: number
  test_suite_id: number
  name: string
  description?: string
  steps: TestStep[]
  data_driven?: {
    enabled: boolean
    data_source: string
    parameters: string[]
  }
  created_at: string
  updated_at: string
}

export interface DataDrivenConfig {
  enabled: boolean
  data_source: string
  parameters: string[]
} 