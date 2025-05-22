from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse
from app.services.log_service import LogService

router = APIRouter()
log_service = LogService()

@router.get("/")
async def get_logs(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    level: Optional[str] = None,
    keyword: Optional[str] = None,
    limit: int = Query(1000, ge=1, le=10000)
) -> List[Dict[str, Any]]:
    """
    获取日志记录
    
    Args:
        start_time: 开始时间
        end_time: 结束时间
        level: 日志级别
        keyword: 关键字
        limit: 限制数量
        
    Returns:
        List[Dict[str, Any]]: 日志记录列表
    """
    try:
        return log_service.get_logs(
            start_time=start_time,
            end_time=end_time,
            level=level,
            keyword=keyword,
            limit=limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/statistics")
async def get_log_statistics(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    获取日志统计信息
    
    Args:
        start_time: 开始时间
        end_time: 结束时间
        
    Returns:
        Dict[str, Any]: 统计信息
    """
    try:
        return log_service.get_log_statistics(
            start_time=start_time,
            end_time=end_time
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/export")
async def export_logs(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    level: Optional[str] = None,
    keyword: Optional[str] = None
) -> FileResponse:
    """
    导出日志
    
    Args:
        start_time: 开始时间
        end_time: 结束时间
        level: 日志级别
        keyword: 关键字
        
    Returns:
        FileResponse: 导出文件
    """
    try:
        # 生成导出文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"exports/logs_{timestamp}.json"
        
        # 导出日志
        file_path = log_service.export_logs(
            output_path=output_path,
            start_time=start_time,
            end_time=end_time,
            level=level,
            keyword=keyword
        )
        
        return FileResponse(
            file_path,
            filename=f"logs_{timestamp}.json",
            media_type="application/json"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 