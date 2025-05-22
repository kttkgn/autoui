class ExecutionError(Exception):
    """测试执行错误"""
    pass

class TestExecutionError(Exception):
    """测试执行错误"""
    pass

class TestStepError(Exception):
    """测试步骤错误"""
    pass

class ElementNotFoundError(Exception):
    """元素未找到错误"""
    pass

class ElementNotVisibleError(Exception):
    """元素不可见错误"""
    pass

class ElementNotEnabledError(Exception):
    """元素不可用错误"""
    pass

class ElementNotSelectedError(Exception):
    """元素未选中错误"""
    pass

class AssertionError(Exception):
    """断言错误"""
    pass

class TimeoutError(Exception):
    """超时错误"""
    pass

class InvalidLocatorError(Exception):
    """无效的定位器错误"""
    pass

class InvalidActionError(Exception):
    """无效的操作错误"""
    pass

class InvalidAssertionError(Exception):
    """无效的断言错误"""
    pass

class DataSourceError(Exception):
    """数据源错误"""
    pass

class DataValidationError(Exception):
    """数据验证错误"""
    pass

class DataParameterError(Exception):
    """数据参数错误"""
    pass

class DataCleanupError(Exception):
    """数据清理错误"""
    pass

class ReportGenerationError(Exception):
    """报告生成错误"""
    pass

class ReportTemplateError(Exception):
    """报告模板错误"""
    pass

class ReportExportError(Exception):
    """报告导出错误"""
    pass

class ResourceConfigError(Exception):
    """资源配置错误"""
    pass

class ResourceValidationError(Exception):
    """资源验证错误"""
    pass

class ResourceNotFoundError(Exception):
    """资源未找到错误"""
    pass

class ResourceOperationError(Exception):
    """资源操作错误"""
    pass

class ResourceHealthCheckError(Exception):
    """资源健康检查错误"""
    pass

class DeviceError(Exception):
    """设备相关错误"""
    pass

class ReportError(Exception):
    """报告错误"""
    pass

class ProjectError(Exception):
    """项目错误"""
    pass 