from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import jinja2
import pdfkit
import os
from pathlib import Path
from app.core.logger import logger
from app.models.project import TestExecution, TestStepResult
from app.core.exceptions import ReportGenerationError

class ReportGenerator:
    """报告生成器基类"""
    
    def __init__(self, template_dir: str = "templates/reports"):
        """
        初始化报告生成器
        
        Args:
            template_dir: 模板目录
        """
        self.template_dir = Path(template_dir)
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(self.template_dir)),
            autoescape=True
        )
        
    def generate_report(
        self,
        execution: TestExecution,
        step_results: List[TestStepResult],
        output_path: str
    ) -> str:
        """
        生成报告
        
        Args:
            execution: 测试执行记录
            step_results: 步骤执行结果列表
            output_path: 输出路径
            
        Returns:
            str: 报告文件路径
        """
        raise NotImplementedError("子类必须实现generate_report方法")
        
class HTMLReportGenerator(ReportGenerator):
    """HTML报告生成器"""
    
    def generate_report(
        self,
        execution: TestExecution,
        step_results: List[TestStepResult],
        output_path: str
    ) -> str:
        """
        生成HTML报告
        
        Args:
            execution: 测试执行记录
            step_results: 步骤执行结果列表
            output_path: 输出路径
            
        Returns:
            str: 报告文件路径
        """
        try:
            # 加载模板
            template = self.env.get_template("report.html")
            
            # 准备数据
            data = {
                "execution": execution,
                "step_results": step_results,
                "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "summary": self._generate_summary(execution, step_results)
            }
            
            # 渲染模板
            html_content = template.render(**data)
            
            # 保存报告
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
                
            return str(output_path)
            
        except Exception as e:
            raise ReportGenerationError(f"生成HTML报告失败: {str(e)}")
            
    def _generate_summary(self, execution: TestExecution, step_results: List[TestStepResult]) -> Dict[str, Any]:
        """
        生成报告摘要
        
        Args:
            execution: 测试执行记录
            step_results: 步骤执行结果列表
            
        Returns:
            Dict[str, Any]: 报告摘要
        """
        total_steps = len(step_results)
        passed_steps = len([r for r in step_results if r.status == "passed"])
        failed_steps = len([r for r in step_results if r.status == "failed"])
        skipped_steps = len([r for r in step_results if r.status == "skipped"])
        
        start_time = execution.start_time
        end_time = execution.end_time
        duration = (end_time - start_time).total_seconds() if end_time else 0
        
        return {
            "total_steps": total_steps,
            "passed_steps": passed_steps,
            "failed_steps": failed_steps,
            "skipped_steps": skipped_steps,
            "pass_rate": (passed_steps / total_steps * 100) if total_steps > 0 else 0,
            "duration": duration,
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S") if start_time else None,
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S") if end_time else None
        }
        
class PDFReportGenerator(ReportGenerator):
    """PDF报告生成器"""
    
    def generate_report(
        self,
        execution: TestExecution,
        step_results: List[TestStepResult],
        output_path: str
    ) -> str:
        """
        生成PDF报告
        
        Args:
            execution: 测试执行记录
            step_results: 步骤执行结果列表
            output_path: 输出路径
            
        Returns:
            str: 报告文件路径
        """
        try:
            # 先生成HTML报告
            html_generator = HTMLReportGenerator(self.template_dir)
            html_path = html_generator.generate_report(
                execution,
                step_results,
                output_path.replace(".pdf", ".html")
            )
            
            # 转换为PDF
            pdf_path = output_path
            pdfkit.from_file(html_path, pdf_path)
            
            # 删除临时HTML文件
            os.remove(html_path)
            
            return pdf_path
            
        except Exception as e:
            raise ReportGenerationError(f"生成PDF报告失败: {str(e)}")
            
class ReportGeneratorFactory:
    """报告生成器工厂类"""
    
    @staticmethod
    def create_generator(report_type: str) -> ReportGenerator:
        """
        创建报告生成器
        
        Args:
            report_type: 报告类型
            
        Returns:
            ReportGenerator: 报告生成器实例
        """
        if report_type == "html":
            return HTMLReportGenerator()
        elif report_type == "pdf":
            return PDFReportGenerator()
        else:
            raise ReportGenerationError(f"不支持的报告类型: {report_type}") 