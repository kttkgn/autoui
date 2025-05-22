from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from pathlib import Path
from app.core.report_generator import ReportGeneratorFactory
from app.core.logger import logger
from app.models.project import TestExecution, TestStepResult
from app.crud.test_execution import test_execution_crud
from app.core.exceptions import ReportGenerationError

class ReportService:
    """报告生成服务"""
    
    def __init__(self, output_dir: str = "reports"):
        """
        初始化报告生成服务
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    async def generate_report(
        self,
        execution_id: int,
        report_type: str = "html"
    ) -> str:
        """
        生成报告
        
        Args:
            execution_id: 测试执行ID
            report_type: 报告类型
            
        Returns:
            str: 报告文件路径
        """
        try:
            # 获取执行记录
            execution = await test_execution_crud.get(execution_id)
            if not execution:
                raise ReportGenerationError(f"执行记录不存在: {execution_id}")
                
            # 获取步骤结果
            step_results = await test_execution_crud.get_step_results(execution_id)
            
            # 创建报告生成器
            generator = ReportGeneratorFactory.create_generator(report_type)
            
            # 生成报告文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{execution_id}_{timestamp}.{report_type}"
            output_path = self.output_dir / filename
            
            # 生成报告
            report_path = generator.generate_report(
                execution,
                step_results,
                str(output_path)
            )
            
            logger.info(f"报告生成成功: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"生成报告失败: {str(e)}")
            raise ReportGenerationError(f"生成报告失败: {str(e)}")
            
    async def generate_batch_report(
        self,
        execution_ids: List[int],
        report_type: str = "html"
    ) -> str:
        """
        生成批量报告
        
        Args:
            execution_ids: 测试执行ID列表
            report_type: 报告类型
            
        Returns:
            str: 报告文件路径
        """
        try:
            # 获取执行记录
            executions = []
            all_step_results = []
            
            for execution_id in execution_ids:
                execution = await test_execution_crud.get(execution_id)
                if not execution:
                    raise ReportGenerationError(f"执行记录不存在: {execution_id}")
                    
                step_results = await test_execution_crud.get_step_results(execution_id)
                
                executions.append(execution)
                all_step_results.extend(step_results)
                
            # 创建报告生成器
            generator = ReportGeneratorFactory.create_generator(report_type)
            
            # 生成报告文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batch_report_{timestamp}.{report_type}"
            output_path = self.output_dir / filename
            
            # 生成报告
            report_path = generator.generate_report(
                executions[0],  # 使用第一个执行记录作为主记录
                all_step_results,
                str(output_path)
            )
            
            logger.info(f"批量报告生成成功: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"生成批量报告失败: {str(e)}")
            raise ReportGenerationError(f"生成批量报告失败: {str(e)}")
            
    async def generate_summary_report(
        self,
        start_date: datetime,
        end_date: datetime,
        report_type: str = "html"
    ) -> str:
        """
        生成汇总报告
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            report_type: 报告类型
            
        Returns:
            str: 报告文件路径
        """
        try:
            # 获取执行记录
            executions = await test_execution_crud.get_multi_by_date_range(
                start_date,
                end_date
            )
            
            if not executions:
                raise ReportGenerationError("指定日期范围内没有执行记录")
                
            # 获取所有步骤结果
            all_step_results = []
            for execution in executions:
                step_results = await test_execution_crud.get_step_results(execution.id)
                all_step_results.extend(step_results)
                
            # 创建报告生成器
            generator = ReportGeneratorFactory.create_generator(report_type)
            
            # 生成报告文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summary_report_{timestamp}.{report_type}"
            output_path = self.output_dir / filename
            
            # 生成报告
            report_path = generator.generate_report(
                executions[0],  # 使用第一个执行记录作为主记录
                all_step_results,
                str(output_path)
            )
            
            logger.info(f"汇总报告生成成功: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"生成汇总报告失败: {str(e)}")
            raise ReportGenerationError(f"生成汇总报告失败: {str(e)}")
            
    def get_report_path(self, execution_id: int) -> Optional[str]:
        """
        获取报告路径
        
        Args:
            execution_id: 测试执行ID
            
        Returns:
            Optional[str]: 报告文件路径
        """
        try:
            # 查找最新的报告文件
            pattern = f"report_{execution_id}_*.html"
            report_files = list(self.output_dir.glob(pattern))
            
            if not report_files:
                return None
                
            # 按修改时间排序
            latest_report = max(report_files, key=lambda x: x.stat().st_mtime)
            return str(latest_report)
            
        except Exception as e:
            logger.error(f"获取报告路径失败: {str(e)}")
            return None
            
    def cleanup_reports(self, days: int = 30) -> None:
        """
        清理旧报告
        
        Args:
            days: 保留天数
        """
        try:
            # 计算截止时间
            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
            
            # 遍历报告文件
            for report_file in self.output_dir.glob("report_*.*"):
                if report_file.stat().st_mtime < cutoff_time:
                    report_file.unlink()
                    logger.info(f"删除旧报告: {report_file}")
                    
        except Exception as e:
            logger.error(f"清理旧报告失败: {str(e)}") 