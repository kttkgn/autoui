import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from logging.handlers import RotatingFileHandler
import json

class Logger:
    """日志记录器"""
    
    def __init__(
        self,
        name: str = "uiauto",
        log_dir: str = "logs",
        level: int = logging.INFO,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5
    ):
        """
        初始化日志记录器
        
        Args:
            name: 日志记录器名称
            log_dir: 日志目录
            level: 日志级别
            max_bytes: 单个日志文件最大字节数
            backup_count: 保留的日志文件数量
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # 创建文件处理器
        log_file = self.log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
    def debug(self, message: str, **kwargs) -> None:
        """
        记录调试日志
        
        Args:
            message: 日志消息
            **kwargs: 额外参数
        """
        self._log(logging.DEBUG, message, **kwargs)
        
    def info(self, message: str, **kwargs) -> None:
        """
        记录信息日志
        
        Args:
            message: 日志消息
            **kwargs: 额外参数
        """
        self._log(logging.INFO, message, **kwargs)
        
    def warning(self, message: str, **kwargs) -> None:
        """
        记录警告日志
        
        Args:
            message: 日志消息
            **kwargs: 额外参数
        """
        self._log(logging.WARNING, message, **kwargs)
        
    def error(self, message: str, **kwargs) -> None:
        """
        记录错误日志
        
        Args:
            message: 日志消息
            **kwargs: 额外参数
        """
        self._log(logging.ERROR, message, **kwargs)
        
    def critical(self, message: str, **kwargs) -> None:
        """
        记录严重错误日志
        
        Args:
            message: 日志消息
            **kwargs: 额外参数
        """
        self._log(logging.CRITICAL, message, **kwargs)
        
    def _log(self, level: int, message: str, **kwargs) -> None:
        """
        记录日志
        
        Args:
            level: 日志级别
            message: 日志消息
            **kwargs: 额外参数
        """
        if kwargs:
            # 将额外参数转换为JSON字符串
            extra = json.dumps(kwargs, ensure_ascii=False)
            message = f"{message} - {extra}"
        self.logger.log(level, message)
        
    def get_log_files(self) -> list:
        """
        获取所有日志文件
        
        Returns:
            list: 日志文件列表
        """
        return list(self.log_dir.glob(f"{self.name}_*.log"))
        
    def cleanup_logs(self, days: int = 30) -> None:
        """
        清理旧日志
        
        Args:
            days: 保留天数
        """
        cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
        for log_file in self.get_log_files():
            if log_file.stat().st_mtime < cutoff_time:
                log_file.unlink()
                self.info(f"删除旧日志文件: {log_file}")

# 创建全局日志记录器实例
logger = Logger() 