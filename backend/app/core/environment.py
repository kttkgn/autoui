from typing import Dict, Optional
from pydantic import BaseModel
from app.core.config import settings

class Environment(BaseModel):
    """环境配置类"""
    id: str
    name: str
    description: Optional[str] = None
    config: Dict = {}
    is_active: bool = True

class EnvironmentManager:
    """环境管理器"""
    def __init__(self):
        self._environments: Dict[str, Environment] = {}
        
    def add_environment(self, env: Environment) -> None:
        """添加环境"""
        self._environments[env.id] = env
        
    def remove_environment(self, env_id: str) -> None:
        """移除环境"""
        if env_id in self._environments:
            del self._environments[env_id]
            
    def get_environment(self, env_id: str) -> Optional[Environment]:
        """获取环境"""
        return self._environments.get(env_id)
    
    def get_all_environments(self) -> Dict[str, Environment]:
        """获取所有环境"""
        return self._environments.copy()
    
    def update_environment(self, env_id: str, env: Environment) -> None:
        """更新环境"""
        if env_id in self._environments:
            self._environments[env_id] = env

# 创建全局环境管理器实例
environment_manager = EnvironmentManager()

# 初始化默认环境
default_env = Environment(
    id="default",
    name="Default Environment",
    description="Default environment for testing",
    config={
        "base_url": settings.API_V1_STR,
        "timeout": 30,
        "retry_count": 3
    }
)
environment_manager.add_environment(default_env) 