import json
import csv
import yaml
from typing import List, Dict, Any, Optional
from pathlib import Path

class DataDriver:
    @staticmethod
    async def load_test_data(data_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """加载测试数据
        
        Args:
            data_config: 数据配置，包含以下字段：
                - type: 数据类型，支持 json/csv/yaml
                - path: 数据文件路径
                - variables: 变量映射，用于替换数据中的变量
        """
        data_type = data_config.get("type", "json")
        data_path = data_config.get("path")
        variables = data_config.get("variables", {})

        if not data_path:
            raise Exception("未指定数据文件路径")

        try:
            # 读取数据文件
            if data_type == "json":
                data = await DataDriver._load_json(data_path)
            elif data_type == "csv":
                data = await DataDriver._load_csv(data_path)
            elif data_type == "yaml":
                data = await DataDriver._load_yaml(data_path)
            else:
                raise Exception(f"不支持的数据类型: {data_type}")

            # 替换变量
            return await DataDriver._replace_variables(data, variables)
        except Exception as e:
            raise Exception(f"加载测试数据失败: {str(e)}")

    @staticmethod
    async def _load_json(file_path: str) -> List[Dict[str, Any]]:
        """加载JSON数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data if isinstance(data, list) else [data]
        except Exception as e:
            raise Exception(f"加载JSON数据失败: {str(e)}")

    @staticmethod
    async def _load_csv(file_path: str) -> List[Dict[str, Any]]:
        """加载CSV数据"""
        try:
            data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(dict(row))
            return data
        except Exception as e:
            raise Exception(f"加载CSV数据失败: {str(e)}")

    @staticmethod
    async def _load_yaml(file_path: str) -> List[Dict[str, Any]]:
        """加载YAML数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            return data if isinstance(data, list) else [data]
        except Exception as e:
            raise Exception(f"加载YAML数据失败: {str(e)}")

    @staticmethod
    async def _replace_variables(data: List[Dict[str, Any]], variables: Dict[str, Any]) -> List[Dict[str, Any]]:
        """替换数据中的变量"""
        result = []
        for item in data:
            new_item = {}
            for key, value in item.items():
                if isinstance(value, str):
                    # 替换字符串中的变量
                    for var_name, var_value in variables.items():
                        value = value.replace(f"${{{var_name}}}", str(var_value))
                new_item[key] = value
            result.append(new_item)
        return result 