from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.services.data_driven_service import DataDrivenService
from app.services.test_engine_service import TestEngineService
from app.schemas.test_execution import TestExecution
from app.core.exceptions import (
    DataSourceError,
    DataValidationError,
    DataParameterError,
    TestExecutionError
)

router = APIRouter()
test_engine_service = TestEngineService()
data_driven_service = DataDrivenService(test_engine_service.current_engine)

@router.post("/{test_case_id}/execute", response_model=List[TestExecution])
async def execute_data_driven_test(
    test_case_id: int,
    data_source_path: str,
    data_schema: Dict[str, Any]
) -> List[TestExecution]:
    """
    执行数据驱动测试
    
    Args:
        test_case_id: 测试用例ID
        data_source_path: 数据源文件路径
        data_schema: 数据模式
        
    Returns:
        List[TestExecution]: 测试执行记录列表
    """
    try:
        # 获取测试用例
        test_case = await test_case.get(test_case_id)
        if not test_case:
            raise HTTPException(
                status_code=404,
                detail="测试用例不存在"
            )
            
        # 执行数据驱动测试
        return await data_driven_service.execute_data_driven_test(
            test_case,
            data_source_path,
            data_schema
        )
        
    except DataSourceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DataValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except DataParameterError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except TestExecutionError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload")
async def upload_data_source(file: UploadFile = File(...)) -> Dict[str, Any]:
    """
    上传数据源文件
    
    Args:
        file: 数据源文件
        
    Returns:
        Dict[str, Any]: 上传结果
    """
    try:
        # 保存文件
        file_path = f"data/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
            
        return {
            "message": "文件上传成功",
            "file_path": file_path
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data")
async def get_test_data() -> List[Dict[str, Any]]:
    """
    获取测试数据
    
    Returns:
        List[Dict[str, Any]]: 测试数据列表
    """
    try:
        return data_driven_service.get_test_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/data")
async def add_test_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    添加测试数据
    
    Args:
        data: 测试数据
        
    Returns:
        Dict[str, Any]: 添加结果
    """
    try:
        data_driven_service.add_test_data(data)
        return {"message": "测试数据添加成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/data/{index}")
async def remove_test_data(index: int) -> Dict[str, Any]:
    """
    删除测试数据
    
    Args:
        index: 数据索引
        
    Returns:
        Dict[str, Any]: 删除结果
    """
    try:
        data_driven_service.remove_test_data(index)
        return {"message": "测试数据删除成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/data/{index}")
async def update_test_data(
    index: int,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    更新测试数据
    
    Args:
        index: 数据索引
        data: 测试数据
        
    Returns:
        Dict[str, Any]: 更新结果
    """
    try:
        data_driven_service.update_test_data(index, data)
        return {"message": "测试数据更新成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/save")
async def save_data() -> Dict[str, Any]:
    """
    保存测试数据
    
    Returns:
        Dict[str, Any]: 保存结果
    """
    try:
        data_driven_service.save_data()
        return {"message": "测试数据保存成功"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 