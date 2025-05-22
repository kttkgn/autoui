from typing import Dict, Any, List, Optional, Union
import csv
import json
import yaml
import pandas as pd
from pathlib import Path
from app.core.logger import logger
from app.core.exceptions import DataSourceError

class DataSource:
    """数据源基类"""
    
    def __init__(self, file_path: str):
        """
        初始化数据源
        
        Args:
            file_path: 数据文件路径
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise DataSourceError(f"数据文件不存在: {file_path}")
            
    def read(self) -> List[Dict[str, Any]]:
        """
        读取数据
        
        Returns:
            List[Dict[str, Any]]: 数据列表
        """
        raise NotImplementedError("子类必须实现read方法")
        
    def write(self, data: List[Dict[str, Any]]) -> None:
        """
        写入数据
        
        Args:
            data: 数据列表
        """
        raise NotImplementedError("子类必须实现write方法")
        
class CSVDataSource(DataSource):
    """CSV数据源"""
    
    def read(self) -> List[Dict[str, Any]]:
        """
        读取CSV数据
        
        Returns:
            List[Dict[str, Any]]: 数据列表
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except Exception as e:
            raise DataSourceError(f"读取CSV文件失败: {str(e)}")
            
    def write(self, data: List[Dict[str, Any]]) -> None:
        """
        写入CSV数据
        
        Args:
            data: 数据列表
        """
        try:
            if not data:
                return
                
            fieldnames = data[0].keys()
            with open(self.file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except Exception as e:
            raise DataSourceError(f"写入CSV文件失败: {str(e)}")
            
class JSONDataSource(DataSource):
    """JSON数据源"""
    
    def read(self) -> List[Dict[str, Any]]:
        """
        读取JSON数据
        
        Returns:
            List[Dict[str, Any]]: 数据列表
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise DataSourceError(f"读取JSON文件失败: {str(e)}")
            
    def write(self, data: List[Dict[str, Any]]) -> None:
        """
        写入JSON数据
        
        Args:
            data: 数据列表
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise DataSourceError(f"写入JSON文件失败: {str(e)}")
            
class YAMLDataSource(DataSource):
    """YAML数据源"""
    
    def read(self) -> List[Dict[str, Any]]:
        """
        读取YAML数据
        
        Returns:
            List[Dict[str, Any]]: 数据列表
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise DataSourceError(f"读取YAML文件失败: {str(e)}")
            
    def write(self, data: List[Dict[str, Any]]) -> None:
        """
        写入YAML数据
        
        Args:
            data: 数据列表
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True)
        except Exception as e:
            raise DataSourceError(f"写入YAML文件失败: {str(e)}")
            
class ExcelDataSource(DataSource):
    """Excel数据源"""
    
    def read(self) -> List[Dict[str, Any]]:
        """
        读取Excel数据
        
        Returns:
            List[Dict[str, Any]]: 数据列表
        """
        try:
            df = pd.read_excel(self.file_path)
            return df.to_dict('records')
        except Exception as e:
            raise DataSourceError(f"读取Excel文件失败: {str(e)}")
            
    def write(self, data: List[Dict[str, Any]]) -> None:
        """
        写入Excel数据
        
        Args:
            data: 数据列表
        """
        try:
            df = pd.DataFrame(data)
            df.to_excel(self.file_path, index=False)
        except Exception as e:
            raise DataSourceError(f"写入Excel文件失败: {str(e)}")
            
class DataSourceFactory:
    """数据源工厂类"""
    
    @staticmethod
    def create_data_source(file_path: str) -> DataSource:
        """
        创建数据源
        
        Args:
            file_path: 数据文件路径
            
        Returns:
            DataSource: 数据源实例
        """
        file_path = Path(file_path)
        suffix = file_path.suffix.lower()
        
        if suffix == '.csv':
            return CSVDataSource(file_path)
        elif suffix == '.json':
            return JSONDataSource(file_path)
        elif suffix in ['.yaml', '.yml']:
            return YAMLDataSource(file_path)
        elif suffix in ['.xlsx', '.xls']:
            return ExcelDataSource(file_path)
        else:
            raise DataSourceError(f"不支持的文件类型: {suffix}") 