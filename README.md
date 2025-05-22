# 自动化测试平台

## 项目概述
本项目是一个自动化测试平台，旨在提供全面的测试管理、执行和报告功能。通过该平台，用户可以管理测试用例、执行测试任务、生成测试报告，并进行环境配置和资源管理。

## 功能特点
- **项目管理**: 创建和管理项目，支持项目成员管理。
- **测试用例管理**: 支持测试用例的创建、更新和删除。
- **测试执行管理**: 执行测试用例，查看执行结果和步骤。
- **报告管理**: 生成和导出测试报告，支持多种报告类型。
- **环境管理**: 配置和管理测试环境，支持环境切换。
- **资源管理**: 管理测试资源，包括设备和元素定位。
- **任务管理**: 创建和管理测试任务，支持批量执行。

## 技术栈
- **前端**: Vue.js, Axios
- **后端**: FastAPI
- **数据库**: Mysql 

## 安装说明
1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **安装后端依赖**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **安装前端依赖**
   ```bash
   cd frontend
   npm install
   ```

4. **启动后端服务**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

5. **启动前端服务**
   ```bash
   cd frontend
   npm run dev
   ```

## 使用说明
- 访问 `http://localhost:8080` 进入前端应用。
- 通过API接口进行测试用例、任务、报告等的管理。

## 贡献
欢迎贡献代码或提出建议，请提交Pull Request或Issue。

## 许可证
本项目采用MIT许可证。 