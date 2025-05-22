from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from pathlib import Path
from app.core.logger import logger

class LogService:
    """日志服务"""
    
    def __init__(self, log_dir: str = "logs"):
        """
        初始化日志服务
        
        Args:
            log_dir: 日志目录
        """
        self.log_dir = Path(log_dir)
        
    def get_logs(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        level: Optional[str] = None,
        keyword: Optional[str] = None,
        limit: int = 1000
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
        logs = []
        count = 0
        
        for log_file in self.log_dir.glob("*.log"):
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    if count >= limit:
                        break
                        
                    try:
                        # 解析日志行
                        log_entry = self._parse_log_line(line)
                        if not log_entry:
                            continue
                            
                        # 应用过滤条件
                        if not self._apply_filters(log_entry, start_time, end_time, level, keyword):
                            continue
                            
                        logs.append(log_entry)
                        count += 1
                        
                    except Exception as e:
                        logger.error(f"解析日志行失败: {str(e)}")
                        continue
                        
        return logs
        
    def get_log_statistics(
        self,
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
        stats = {
            "total": 0,
            "by_level": {},
            "by_hour": {},
            "by_day": {}
        }
        
        for log_file in self.log_dir.glob("*.log"):
            with open(log_file, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        log_entry = self._parse_log_line(line)
                        if not log_entry:
                            continue
                            
                        # 应用时间过滤
                        if not self._apply_time_filter(log_entry, start_time, end_time):
                            continue
                            
                        # 更新统计信息
                        stats["total"] += 1
                        
                        # 按级别统计
                        level = log_entry["level"]
                        stats["by_level"][level] = stats["by_level"].get(level, 0) + 1
                        
                        # 按小时统计
                        hour = log_entry["timestamp"].hour
                        stats["by_hour"][hour] = stats["by_hour"].get(hour, 0) + 1
                        
                        # 按天统计
                        day = log_entry["timestamp"].strftime("%Y-%m-%d")
                        stats["by_day"][day] = stats["by_day"].get(day, 0) + 1
                        
                    except Exception as e:
                        logger.error(f"统计日志失败: {str(e)}")
                        continue
                        
        return stats
        
    def export_logs(
        self,
        output_path: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        level: Optional[str] = None,
        keyword: Optional[str] = None
    ) -> str:
        """
        导出日志
        
        Args:
            output_path: 输出路径
            start_time: 开始时间
            end_time: 结束时间
            level: 日志级别
            keyword: 关键字
            
        Returns:
            str: 导出文件路径
        """
        logs = self.get_logs(start_time, end_time, level, keyword)
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2, default=str)
            
        return str(output_path)
        
    def _parse_log_line(self, line: str) -> Optional[Dict[str, Any]]:
        """
        解析日志行
        
        Args:
            line: 日志行
            
        Returns:
            Optional[Dict[str, Any]]: 解析结果
        """
        try:
            # 解析日志格式
            parts = line.strip().split(" - ", 3)
            if len(parts) != 4:
                return None
                
            timestamp_str, name, level, message = parts
            
            # 解析时间戳
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
            
            # 解析额外参数
            extra = {}
            if " - " in message:
                message, extra_str = message.rsplit(" - ", 1)
                try:
                    extra = json.loads(extra_str)
                except json.JSONDecodeError:
                    pass
                    
            return {
                "timestamp": timestamp,
                "name": name,
                "level": level,
                "message": message,
                "extra": extra
            }
            
        except Exception:
            return None
            
    def _apply_filters(
        self,
        log_entry: Dict[str, Any],
        start_time: Optional[datetime],
        end_time: Optional[datetime],
        level: Optional[str],
        keyword: Optional[str]
    ) -> bool:
        """
        应用过滤条件
        
        Args:
            log_entry: 日志条目
            start_time: 开始时间
            end_time: 结束时间
            level: 日志级别
            keyword: 关键字
            
        Returns:
            bool: 是否通过过滤
        """
        # 时间过滤
        if not self._apply_time_filter(log_entry, start_time, end_time):
            return False
            
        # 级别过滤
        if level and log_entry["level"] != level:
            return False
            
        # 关键字过滤
        if keyword:
            message = log_entry["message"].lower()
            if keyword.lower() not in message:
                return False
                
        return True
        
    def _apply_time_filter(
        self,
        log_entry: Dict[str, Any],
        start_time: Optional[datetime],
        end_time: Optional[datetime]
    ) -> bool:
        """
        应用时间过滤
        
        Args:
            log_entry: 日志条目
            start_time: 开始时间
            end_time: 结束时间
            
        Returns:
            bool: 是否通过过滤
        """
        timestamp = log_entry["timestamp"]
        
        if start_time and timestamp < start_time:
            return False
            
        if end_time and timestamp > end_time:
            return False
            
        return True 