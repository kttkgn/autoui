from enum import Enum

class ProjectStatus(str, Enum):
    """项目状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

class TestExecutionStatus(str, Enum):
    """测试执行状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"
    BLOCKED = "blocked"

class TestStepStatus(str, Enum):
    """测试步骤状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    ERROR = "error"
    SKIPPED = "skipped"

class TestCaseStatus(str, Enum):
    """测试用例状态枚举"""
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"

class TestSuiteStatus(str, Enum):
    """测试套件状态枚举"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"

class TestPriority(str, Enum):
    """测试优先级枚举"""
    P0 = "p0"
    P1 = "p1"
    P2 = "p2"
    P3 = "p3"
    P4 = "p4"

class TestType(str, Enum):
    """测试类型枚举"""
    FUNCTIONAL = "functional"
    PERFORMANCE = "performance"
    SECURITY = "security"
    USABILITY = "usability"
    COMPATIBILITY = "compatibility"
    REGRESSION = "regression"

class TestEnvironment(str, Enum):
    """测试环境枚举"""
    DEV = "dev"
    TEST = "test"
    STAGING = "staging"
    PROD = "prod"

class TestPlatform(str, Enum):
    """测试平台枚举"""
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"
    DESKTOP = "desktop"

class ExecutionStatus(str, Enum):
    """执行状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ReportType(str, Enum):
    """报告类型枚举"""
    HTML = "html"
    PDF = "pdf"
    EXCEL = "excel"
    JSON = "json" 