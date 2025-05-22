from fastapi import APIRouter
from app.api.v1.endpoints import (
    environments,
    resources,
    test_cases,
    tasks,
    devices,
    elements,
    execution,
    reports,
    users,
    projects
)

api_router = APIRouter()

# 环境管理
api_router.include_router(
    environments.router,
    prefix="/environments",
    tags=["环境管理"]
)

# 资源池管理
api_router.include_router(
    resources.router,
    prefix="/resources",
    tags=["资源池管理"]
)

# 测试用例管理
api_router.include_router(
    test_cases.router,
    prefix="/testcases",
    tags=["测试用例管理"]
)

# 测试任务管理
api_router.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["测试任务管理"]
)

# 设备管理
api_router.include_router(
    devices.router,
    prefix="/devices",
    tags=["设备管理"]
)

# 元素定位
api_router.include_router(
    elements.router,
    prefix="/elements",
    tags=["元素定位"]
)

# 测试执行
api_router.include_router(
    execution.router,
    prefix="/execution",
    tags=["测试执行"]
)

# 测试报告
api_router.include_router(
    reports.router,
    prefix="/reports",
    tags=["测试报告"]
)

# 用户管理
# api_router.include_router(
#     users.router,
#     prefix="/users",
#     tags=["用户管理"]
# )

# 项目管理
api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["项目管理"]
) 