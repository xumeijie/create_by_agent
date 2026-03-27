"""
适配器工厂 (AdapterFactory)

使用工厂模式创建和管理协议和数据库适配器：
- 支持动态注册新的适配器
- 支持创建多个类型的协议适配器 (HTTP、SOAP、GraphQL)
- 支持创建多个类型的数据库适配器 (MySQL、Oracle、PostgreSQL)
- 维护所有已注册的适配器列表

适配器注册流程：
1. 创建适配器类，继承相应的基类
2. 在工厂中注册: AdapterFactory.register_protocol_adapter("name", AdapterClass)
3. 在代码中使用: adapter = AdapterFactory.get_protocol_adapter("name", **kwargs)

使用示例：
    from core.adapter_factory import AdapterFactory
    
    # 获取HTTP适配器
    http = AdapterFactory.get_protocol_adapter("http", base_url="http://api.test")
    
    # 获取MySQL适配器
    mysql = AdapterFactory.get_database_adapter("mysql", host="localhost", ...)
"""
from typing import Dict, Type, Any


class AdapterFactory:
    """Factory for creating protocol and database adapters."""
    
    _protocol_adapters: Dict[str, Type] = {}
    _database_adapters: Dict[str, Type] = {}
    
    @classmethod
    def register_protocol_adapter(cls, name: str, adapter_class: Type) -> None:
        """Register a protocol adapter."""
        cls._protocol_adapters[name.lower()] = adapter_class
    
    @classmethod
    def register_database_adapter(cls, name: str, adapter_class: Type) -> None:
        """Register a database adapter."""
        cls._database_adapters[name.lower()] = adapter_class
    
    @classmethod
    def get_protocol_adapter(cls, name: str, **kwargs: Any) -> Any:
        """Get a protocol adapter instance."""
        adapter_class = cls._protocol_adapters.get(name.lower())
        if not adapter_class:
            raise ValueError(f"Protocol adapter '{name}' not registered")
        return adapter_class(**kwargs)
    
    @classmethod
    def get_database_adapter(cls, name: str, **kwargs: Any) -> Any:
        """Get a database adapter instance."""
        adapter_class = cls._database_adapters.get(name.lower())
        if not adapter_class:
            raise ValueError(f"Database adapter '{name}' not registered")
        return adapter_class(**kwargs)
    
    @classmethod
    def list_protocol_adapters(cls) -> list:
        """List all registered protocol adapters."""
        return list(cls._protocol_adapters.keys())
    
    @classmethod
    def list_database_adapters(cls) -> list:
        """List all registered database adapters."""
        return list(cls._database_adapters.keys())
