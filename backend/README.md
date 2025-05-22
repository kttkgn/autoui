# UI自动化测试平台后端

## 项目简介
本项目是一个基于 FastAPI 和 SQLAlchemy 的 UI 自动化测试平台后端，提供设备管理、测试用例管理、测试执行、报告生成等功能。

## 技术栈
- FastAPI
- SQLAlchemy (异步)
- Alembic (数据库迁移)
- Pydantic
- MySQL (数据库)
- Redis (缓存)
- RabbitMQ (消息队列)
- MinIO (对象存储)

## 安装步骤

1. 克隆项目
   ```bash
   git clone <项目地址>
   cd <项目目录>/backend
   ```

2. 创建虚拟环境（推荐使用 conda 或 venv）
   ```bash
   conda create -n backend python=3.12
   conda activate backend
   ```

3. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

4. 配置环境变量
   - 复制 `.env.example` 文件为 `.env`
   - 根据实际情况修改数据库、Redis、RabbitMQ、MinIO 等配置

5. 初始化数据库
   ```bash
   alembic upgrade head
   ```

## 运行项目

启动开发服务器：
```bash
uvicorn app.main:app --reload
```

## API 文档
启动服务后，访问以下地址查看 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构
```
backend/
├── alembic/            # 数据库迁移文件
├── app/
│   ├── api/            # API 路由
│   ├── core/           # 核心配置、异常、依赖等
│   ├── crud/           # 数据库 CRUD 操作
│   ├── db/             # 数据库配置
│   ├── models/         # SQLAlchemy 模型
│   ├── schemas/        # Pydantic 模型
│   ├── services/       # 业务逻辑
│   └── main.py         # 应用入口
├── tests/              # 测试文件
├── .env                # 环境变量
├── .env.example        # 环境变量示例
├── requirements.txt    # 项目依赖
└── README.md           # 项目说明
```

## 开发指南
- 遵循 PEP 8 编码规范
- 使用 Black 进行代码格式化
- 使用 isort 进行导入排序
- 使用 mypy 进行类型检查

## 测试
运行测试：
```bash
pytest
```

## 部署
1. 构建 Docker 镜像
   ```bash
   docker build -t uiauto-backend .
   ```

2. 运行容器
   ```bash
   docker run -d -p 8000:8000 uiauto-backend
   ```

## 贡献指南
1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证
MIT 