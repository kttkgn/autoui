from typing import List, Dict, Any, Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Response, Body
from fastapi.responses import FileResponse
from app.services.report_service import ReportService
from app.core.exceptions import ReportGenerationError
from app.core.enums.project import ReportType
from app.core.exceptions import ReportError

router = APIRouter()
report_service = ReportService()

@router.post("/generate")
async def generate_report(
    *,
    execution_id: str = Body(...),
    report_type: ReportType = Body(...),
    format: str = Body("html")
) -> Dict[str, Any]:
    """
    生成测试报告
    
    Args:
        execution_id: 执行ID
        report_type: 报告类型
        format: 报告格式
        
    Returns:
        Dict[str, Any]: 报告信息
    """
    try:
        report = await report_service.generate_report(
            execution_id,
            report_type,
            format
        )
        return {
            "message": "报告生成成功",
            "report": report.to_dict()
        }
    except ReportError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{report_id}")
async def get_report(
    *,
    report_id: str
) -> Dict[str, Any]:
    """
    获取报告
    
    Args:
        report_id: 报告ID
        
    Returns:
        Dict[str, Any]: 报告信息
    """
    try:
        report = await report_service.get_report(report_id)
        if not report:
            raise HTTPException(status_code=404, detail=f"报告不存在: {report_id}")
        return report.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{report_id}/content")
async def get_report_content(
    *,
    report_id: str
) -> Dict[str, Any]:
    """
    获取报告内容
    
    Args:
        report_id: 报告ID
        
    Returns:
        Dict[str, Any]: 报告内容
    """
    try:
        content = await report_service.get_report_content(report_id)
        if not content:
            raise HTTPException(status_code=404, detail=f"报告不存在: {report_id}")
        return {
            "content": content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def get_all_reports() -> Dict[str, Any]:
    """
    获取所有报告
    
    Returns:
        Dict[str, Any]: 报告列表
    """
    try:
        reports = await report_service.get_all_reports()
        return {
            "reports": [report.to_dict() for report in reports]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/type/{type}")
async def get_reports_by_type(
    *,
    type: ReportType
) -> Dict[str, Any]:
    """
    获取指定类型的报告
    
    Args:
        type: 报告类型
        
    Returns:
        Dict[str, Any]: 报告列表
    """
    try:
        reports = await report_service.get_reports_by_type(type)
        return {
            "reports": [report.to_dict() for report in reports]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/execution/{execution_id}")
async def get_execution_reports(
    *,
    execution_id: str
) -> Dict[str, Any]:
    """
    获取执行的报告
    
    Args:
        execution_id: 执行ID
        
    Returns:
        Dict[str, Any]: 报告列表
    """
    try:
        reports = await report_service.get_execution_reports(execution_id)
        return {
            "reports": [report.to_dict() for report in reports]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{report_id}")
async def delete_report(
    *,
    report_id: str
) -> Dict[str, Any]:
    """
    删除报告
    
    Args:
        report_id: 报告ID
        
    Returns:
        Dict[str, Any]: 删除结果
    """
    try:
        await report_service.delete_report(report_id)
        return {
            "message": "报告删除成功"
        }
    except ReportError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export")
async def export_report(
    *,
    report_id: str = Body(...),
    format: str = Body("html")
) -> Dict[str, Any]:
    """
    导出报告
    
    Args:
        report_id: 报告ID
        format: 导出格式
        
    Returns:
        Dict[str, Any]: 导出结果
    """
    try:
        file_path = await report_service.export_report(report_id, format)
        return {
            "message": "报告导出成功",
            "file_path": file_path
        }
    except ReportError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{execution_id}")
async def generate_report(
    *,
    execution_id: int,
    report_type: str = "html"
) -> Dict[str, Any]:
    """
    生成报告
    
    Args:
        execution_id: 测试执行ID
        report_type: 报告类型
        
    Returns:
        Dict[str, Any]: 生成结果
    """
    try:
        report = await report_service.generate_report(
            str(execution_id),
            ReportType(report_type),
            report_type
        )
        return {
            "message": "报告生成成功",
            "report": report.to_dict()
        }
    except ReportError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/batch")
async def generate_batch_report(
    *,
    execution_ids: List[int] = Body(...),
    report_type: str = Body("html")
) -> Dict[str, Any]:
    """
    批量生成报告
    
    Args:
        execution_ids: 执行ID列表
        report_type: 报告类型
        
    Returns:
        Dict[str, Any]: 生成结果
    """
    try:
        reports = []
        for execution_id in execution_ids:
            report = await report_service.generate_report(
                str(execution_id),
                ReportType(report_type),
                report_type
            )
            reports.append(report.to_dict())
        return {
            "message": "批量报告生成成功",
            "reports": reports
        }
    except ReportError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summary")
async def generate_summary_report(
    *,
    start_date: datetime = Body(...),
    end_date: datetime = Body(...),
    report_type: str = Body("html")
) -> Dict[str, Any]:
    """
    生成汇总报告
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        report_type: 报告类型
        
    Returns:
        Dict[str, Any]: 生成结果
    """
    try:
        report = await report_service.generate_summary_report(
            start_date,
            end_date,
            ReportType(report_type),
            report_type
        )
        return {
            "message": "汇总报告生成成功",
            "report": report.to_dict()
        }
    except ReportError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{execution_id}")
async def get_report(
    *,
    execution_id: int
) -> FileResponse:
    """
    获取报告文件
    
    Args:
        execution_id: 执行ID
        
    Returns:
        FileResponse: 报告文件
    """
    try:
        file_path = await report_service.get_report_file(str(execution_id))
        if not file_path:
            raise HTTPException(status_code=404, detail=f"报告不存在: {execution_id}")
        return FileResponse(
            file_path,
            media_type="application/octet-stream",
            filename=f"report_{execution_id}.html"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/cleanup")
async def cleanup_reports(
    *,
    days: int = 30
) -> Dict[str, Any]:
    """
    清理过期报告
    
    Args:
        days: 保留天数
        
    Returns:
        Dict[str, Any]: 清理结果
    """
    try:
        count = await report_service.cleanup_reports(days)
        return {
            "message": f"成功清理 {count} 个过期报告"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 