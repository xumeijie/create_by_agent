"""
配置管理器 (ConfigManager)

单例模式的配置管理器，用于管理不同环境的配置文件：
- 支持dev、staging、prod三个环境
- 使用YAML格式存储配置
- 支持数据库、API、超时等配置
- 提供便捷的配置获取方法

支持的配置类型：
- 数据库配置: MySQL、Oracle、PostgreSQL
- API配置: HTTP、SOAP、GraphQL
- 超时配置: 请求超时、数据库超时等
- 日志配置: 日志级别、格式等

使用示例：
    config = ConfigManager()
    config.load_config("dev")
    mysql_config = config.get_db_config("mysql")
    api_url = config.get_api_config("http")["base_url"]
"""
import yaml
import os
import re
from typing import Any, Dict, Optional
from pathlib import Path


class ConfigManager:
    """Manages configuration for different environments."""
    
    _instance = None
    _config = {}
    _current_env = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize config manager."""
        if not self._config:
            self.load_config()
    
    def load_config(self, env: str = None) -> None:
        """Load configuration from YAML file."""
        # Auto-detect environment if not specified
        if env is None:
            env = os.getenv("TEST_ENV", "dev")
        
        self._current_env = env
        
        # Try unified environments.yaml first
        config_path = Path(__file__).parent.parent / "config" / "environments.yaml"
        
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                all_envs = yaml.safe_load(f) or {}
            
            # Extract the specific environment
            env_configs = all_envs.get("environments", {})
            self._config = env_configs.get(env, {})
            
            # Add global settings if available
            if "global" in all_envs:
                self._config["global"] = all_envs["global"]
        else:
            # Fallback to individual environment files
            env_config_path = Path(__file__).parent.parent / "config" / f"{env}.yaml"
            if env_config_path.exists():
                with open(env_config_path, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f) or {}
            else:
                self._config = self._get_default_config()
        
        # Resolve environment variables
        self._resolve_env_vars()
    
    def _resolve_env_vars(self) -> None:
        """Resolve environment variables in configuration."""
        self._config = self._substitute_env_vars(self._config)
    
    def _substitute_env_vars(self, obj: Any) -> Any:
        """Recursively substitute environment variables in config."""
        if isinstance(obj, str):
            # Replace ${VAR_NAME} with environment variable value
            pattern = r'\$\{([^}]+)\}'
            def replace_func(match):
                var_name = match.group(1)
                return os.getenv(var_name, match.group(0))
            return re.sub(pattern, replace_func, obj)
        elif isinstance(obj, dict):
            return {k: self._substitute_env_vars(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._substitute_env_vars(item) for item in obj]
        return obj
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key."""
        return self._config.get(key, default)
    
    def get_environment(self) -> str:
        """Get current environment."""
        return self._current_env or "dev"
    
    def get_db_config(self, db_type: str) -> Dict[str, Any]:
        """Get database configuration."""
        return self._config.get("databases", {}).get(db_type, {})
    
    def get_api_config(self, api_type: str) -> Dict[str, Any]:
        """Get API configuration."""
        return self._config.get("apis", {}).get(api_type, {})
    
    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """Return default configuration."""
        return {
            "databases": {
                "mysql": {"host": "localhost", "port": 3306},
                "oracle": {"host": "localhost", "port": 1521},
                "postgresql": {"host": "localhost", "port": 5432}
            },
            "apis": {
                "http": {"base_url": "http://localhost:8080"},
                "soap": {"endpoint": "http://localhost:8080/soap"},
                "graphql": {"endpoint": "http://localhost:8080/graphql"}
            },
            "timeout": 30
        }
