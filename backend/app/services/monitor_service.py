from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from pathlib import Path
from app.core.monitor import monitor
from app.core.logger import logger

class MonitorService:
    """性能监控服务"""
    
    def __init__(self, data_dir: str = "data/monitor"):
        """
        初始化性能监控服务
        
        Args:
            data_dir: 数据目录
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def start_monitoring(self) -> None:
        """启动性能监控"""
        monitor.start()
        
    def stop_monitoring(self) -> None:
        """停止性能监控"""
        monitor.stop()
        
    def get_metrics(
        self,
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
        return monitor.get_performance_metrics(start_time, end_time)
        
    def save_metrics(
        self,
        metrics: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> str:
        """
        保存性能指标
        
        Args:
            metrics: 性能指标
            output_path: 输出路径
            
        Returns:
            str: 保存路径
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = self.data_dir / f"metrics_{timestamp}.json"
        else:
            output_path = Path(output_path)
            
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, ensure_ascii=False, indent=2, default=str)
            
        return str(output_path)
        
    def load_metrics(self, file_path: str) -> Dict[str, Any]:
        """
        加载性能指标
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 性能指标
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    def get_metrics_files(self) -> List[str]:
        """
        获取性能指标文件列表
        
        Returns:
            List[str]: 文件路径列表
        """
        return [str(f) for f in self.data_dir.glob("metrics_*.json")]
        
    def cleanup_metrics(self, days: int = 30) -> None:
        """
        清理旧性能指标
        
        Args:
            days: 保留天数
        """
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        for file_path in self.data_dir.glob("metrics_*.json"):
            if file_path.stat().st_mtime < cutoff_time:
                file_path.unlink()
                logger.info(f"删除旧性能指标文件: {file_path}")
                
    def get_performance_report(
        self,
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
        metrics = self.get_metrics(start_time, end_time)
        stats = metrics["statistics"]
        
        report = {
            "summary": {
                "cpu_usage": {
                    "average": f"{stats['cpu_usage']['avg']:.2f}%",
                    "maximum": f"{stats['cpu_usage']['max']:.2f}%",
                    "minimum": f"{stats['cpu_usage']['min']:.2f}%"
                },
                "memory_usage": {
                    "average": f"{stats['memory_usage']['avg']:.2f}%",
                    "maximum": f"{stats['memory_usage']['max']:.2f}%",
                    "minimum": f"{stats['memory_usage']['min']:.2f}%"
                },
                "disk_io": {
                    "total_read": f"{stats['disk_io']['total_read'] / 1024 / 1024:.2f} MB",
                    "total_write": f"{stats['disk_io']['total_write'] / 1024 / 1024:.2f} MB"
                },
                "network_io": {
                    "total_sent": f"{stats['network_io']['total_sent'] / 1024 / 1024:.2f} MB",
                    "total_recv": f"{stats['network_io']['total_recv'] / 1024 / 1024:.2f} MB"
                }
            },
            "execution_times": {
                name: f"{data['duration']:.2f}s"
                for name, data in metrics["execution_times"].items()
                if data["duration"] is not None
            }
        }
        
        return report 