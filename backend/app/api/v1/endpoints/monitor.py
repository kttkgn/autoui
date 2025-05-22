from typing import Dict, Any, List, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from app.services.monitor_service import MonitorService

router = APIRouter()
monitor_service = MonitorService()

@router.post("/start")
async def start_monitoring() -> Dict[str, Any]:
    """
    启动性能监控
    
    Returns:
        Dict[str, Any]: 操作结果
    """
    try:
        monitor_service.start_monitoring()
        return {
            "message": "性能监控已启动"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
async def stop_monitoring() -> Dict[str, Any]:
    """
    停止性能监控
    
    Returns:
        Dict[str, Any]: 操作结果
    """
    try:
        monitor_service.stop_monitoring()
        return {
            "message": "性能监控已停止"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
async def get_metrics(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    获取性能指标
    
    Args:
        start_time: 开始时间
        end_time: 结束时间
        
    Returns:
        Dict[str, Any]: 性能指标
    """
    try:
        return monitor_service.get_metrics(
            start_time=start_time,
            end_time=end_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/report")
async def get_performance_report(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    获取性能报告
    
    Args:
        start_time: 开始时间
        end_time: 结束时间
        
    Returns:
        Dict[str, Any]: 性能报告
    """
    try:
        return monitor_service.get_performance_report(
            start_time=start_time,
            end_time=end_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export")
async def export_metrics(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> FileResponse:
    """
    导出性能指标
    
    Args:
        start_time: 开始时间
        end_time: 结束时间
        
    Returns:
        FileResponse: 导出文件
    """
    try:
        # 获取性能指标
        metrics = monitor_service.get_metrics(
            start_time=start_time,
            end_time=end_time
        )
        
        # 保存性能指标
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = monitor_service.save_metrics(
            metrics,
            f"exports/metrics_{timestamp}.json"
        )
        
        return FileResponse(
            file_path,
            filename=f"metrics_{timestamp}.json",
            media_type="application/json"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/files")
async def get_metrics_files() -> List[str]:
    """
    获取性能指标文件列表
    
    Returns:
        List[str]: 文件路径列表
    """
    try:
        return monitor_service.get_metrics_files()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cleanup")
async def cleanup_metrics(days: int = Query(30, ge=1)) -> Dict[str, Any]:
    """
    清理旧性能指标
    
    Args:
        days: 保留天数
        
    Returns:
        Dict[str, Any]: 操作结果
    """
    try:
        monitor_service.cleanup_metrics(days)
        return {
            "message": "旧性能指标已清理"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 