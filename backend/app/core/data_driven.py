from typing import Any, Dict, List, Optional, Callable
from pathlib import Path
from pydantic import BaseModel, ValidationError
from app.core.data_source import DataSourceFactory, DataSourceError

class DataDrivenTest:
    """数据驱动测试核心类"""
    
    def __init__(self, data_source_path: str):
        self.data_source_path = data_source_path
        self.test_data: List[Dict[str, Any]] = []
        self.current_index = 0
        self.data_schema: Optional[Dict[str, Any]] = None
        self.data_source = DataSourceFactory.create_data_source(data_source_path)
    
    def load_data(self) -> None:
        """加载测试数据"""
        try:
            self.test_data = self.data_source.read()
        except DataSourceError as e:
            raise ValueError(f"加载测试数据失败: {str(e)}")
    
    def validate_data(self, schema: Dict[str, Any]) -> None:
        """验证测试数据"""
        self.data_schema = schema
        for index, data in enumerate(self.test_data):
            try:
                # 使用 Pydantic 进行数据验证
                class DataSchema(BaseModel):
                    __root__: Dict[str, Any]
                
                DataSchema(__root__=data)
            except ValidationError as e:
                raise ValueError(f"数据验证失败 (索引 {index}): {str(e)}")
    
    def iterate_data(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """迭代执行测试数据"""
        for data in self.test_data:
            self.current_index = self.test_data.index(data)
            callback(data)
    
    def parameterize(self, template: str) -> str:
        """参数化字符串"""
        if not template:
            return template
        
        result = template
        for key, value in self.get_current_data().items():
            result = result.replace(f"${{{key}}}", str(value))
        return result
    
    def parameterize_dict(self, template_dict: Dict[str, Any]) -> Dict[str, Any]:
        """参数化字典"""
        if not template_dict:
            return template_dict
        
        result = {}
        for key, value in template_dict.items():
            if isinstance(value, str):
                result[key] = self.parameterize(value)
            elif isinstance(value, dict):
                result[key] = self.parameterize_dict(value)
            elif isinstance(value, list):
                result[key] = [self.parameterize_dict(item) if isinstance(item, dict) 
                             else self.parameterize(item) if isinstance(item, str)
                             else item for item in value]
            else:
                result[key] = value
        return result
    
    def get_current_data(self) -> Dict[str, Any]:
        """获取当前测试数据"""
        if not self.test_data:
            return {}
        return self.test_data[self.current_index]
    
    def get_test_data(self) -> List[Dict[str, Any]]:
        """获取所有测试数据"""
        return self.test_data
    
    def add_test_data(self, data: Dict[str, Any]) -> None:
        """添加测试数据"""
        if self.data_schema:
            # 验证新数据
            class DataSchema(BaseModel):
                __root__: Dict[str, Any]
            DataSchema(__root__=data)
        self.test_data.append(data)
    
    def remove_test_data(self, index: int) -> None:
        """删除测试数据"""
        if 0 <= index < len(self.test_data):
            self.test_data.pop(index)
    
    def update_test_data(self, index: int, data: Dict[str, Any]) -> None:
        """更新测试数据"""
        if 0 <= index < len(self.test_data):
            if self.data_schema:
                # 验证更新后的数据
                class DataSchema(BaseModel):
                    __root__: Dict[str, Any]
                DataSchema(__root__=data)
            self.test_data[index] = data
    
    def save_data(self) -> None:
        """保存测试数据"""
        try:
            self.data_source.write(self.test_data)
        except DataSourceError as e:
            raise ValueError(f"保存测试数据失败: {str(e)}")
    
    def cleanup_data(self) -> None:
        """清理测试数据"""
        self.test_data = []
        self.current_index = 0
        self.data_schema = None


class DataDriver:
    """数据驱动工具类"""
    
    @staticmethod
    async def load_test_data(config: Dict[str, Any]) -> Optional[DataDrivenTest]:
        """加载测试数据"""
        if not config.get('enabled'):
            return None
        
        data_source = config.get('data_source')
        if not data_source:
            return None
        
        driver = DataDrivenTest(data_source)
        driver.load_data()
        
        # 如果有数据模式定义，进行验证
        if config.get('schema'):
            driver.validate_data(config['schema'])
        
        return driver 