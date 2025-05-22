from typing import Dict, Any, List, Optional
from app.core.environment import Environment, environment_manager
from app.core.logger import logger

class EnvironmentService:
    """环境管理服务"""
    
    def create_environment(
        self,
        name: str,
        config: Dict[str, Any],
        description: Optional[str] = None
    ) -> Environment:
        """
        创建环境配置
        
        Args:
            name: 环境名称
            config: 环境配置
            description: 环境描述
            
        Returns:
            Environment: 环境配置
        """
        # 检查环境是否已存在
        if environment_manager.get_environment(name):
            raise ValueError(f"环境已存在: {name}")
            
        # 创建环境配置
        env = Environment(name, config, description)
        
        # 验证环境配置
        if not environment_manager.validate_environment(name):
            raise ValueError(f"环境配置无效: {name}")
            
        # 保存环境配置
        environment_manager.save_environment(env)
        
        return env
        
    def update_environment(
        self,
        name: str,
        config: Dict[str, Any],
        description: Optional[str] = None
    ) -> Environment:
        """
        更新环境配置
        
        Args:
            name: 环境名称
            config: 环境配置
            description: 环境描述
            
        Returns:
            Environment: 环境配置
        """
        # 检查环境是否存在
        env = environment_manager.get_environment(name)
        if not env:
            raise ValueError(f"环境不存在: {name}")
            
        # 更新环境配置
        env.config.update(config)
        if description is not None:
            env.description = description
            
        # 验证环境配置
        if not environment_manager.validate_environment(name):
            raise ValueError(f"环境配置无效: {name}")
            
        # 保存环境配置
        environment_manager.save_environment(env)
        
        return env
        
    def delete_environment(self, name: str) -> None:
        """
        删除环境配置
        
        Args:
            name: 环境名称
        """
        # 检查环境是否存在
        if not environment_manager.get_environment(name):
            raise ValueError(f"环境不存在: {name}")
            
        # 检查是否为当前环境
        if environment_manager.current_environment == name:
            raise ValueError(f"无法删除当前环境: {name}")
            
        # 删除环境配置
        environment_manager.delete_environment(name)
        
    def switch_environment(self, name: str) -> None:
        """
        切换环境
        
        Args:
            name: 环境名称
        """
        # 检查环境是否存在
        if not environment_manager.get_environment(name):
            raise ValueError(f"环境不存在: {name}")
            
        # 验证环境配置
        if not environment_manager.validate_environment(name):
            raise ValueError(f"环境配置无效: {name}")
            
        # 切换环境
        environment_manager.switch_environment(name)
        
    def get_environment(self, name: str) -> Optional[Environment]:
        """
        获取环境配置
        
        Args:
            name: 环境名称
            
        Returns:
            Optional[Environment]: 环境配置
        """
        return environment_manager.get_environment(name)
        
    def get_current_environment(self) -> Optional[Environment]:
        """
        获取当前环境
        
        Returns:
            Optional[Environment]: 当前环境配置
        """
        return environment_manager.get_current_environment()
        
    def get_all_environments(self) -> Dict[str, Environment]:
        """
        获取所有环境
        
        Returns:
            Dict[str, Environment]: 环境配置字典
        """
        return environment_manager.get_all_environments()
        
    def get_environment_names(self) -> List[str]:
        """
        获取所有环境名称
        
        Returns:
            List[str]: 环境名称列表
        """
        return environment_manager.get_environment_names()
        
    def validate_environment(self, name: str) -> bool:
        """
        验证环境配置
        
        Args:
            name: 环境名称
            
        Returns:
            bool: 是否有效
        """
        return environment_manager.validate_environment(name)
        
    def get_environment_config(self, name: str) -> Dict[str, Any]:
        """
        获取环境配置
        
        Args:
            name: 环境名称
            
        Returns:
            Dict[str, Any]: 环境配置
        """
        env = environment_manager.get_environment(name)
        if not env:
            raise ValueError(f"环境不存在: {name}")
            
        return env.config
        
    def get_environment_value(self, name: str, key: str, default: Any = None) -> Any:
        """
        获取环境配置值
        
        Args:
            name: 环境名称
            key: 配置键
            default: 默认值
            
        Returns:
            Any: 配置值
        """
        env = environment_manager.get_environment(name)
        if not env:
            raise ValueError(f"环境不存在: {name}")
            
        return env.get_value(key, default)
        
    def set_environment_value(self, name: str, key: str, value: Any) -> None:
        """
        设置环境配置值
        
        Args:
            name: 环境名称
            key: 配置键
            value: 配置值
        """
        env = environment_manager.get_environment(name)
        if not env:
            raise ValueError(f"环境不存在: {name}")
            
        env.set_value(key, value)
        environment_manager.save_environment(env) 