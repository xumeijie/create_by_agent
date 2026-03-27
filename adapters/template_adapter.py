"""
适配器模板 (Adapter Template)

为开发者提供创建自定义适配器的模板和示例：

模板类型：
1. CustomProtocolTemplate
   - 创建自定义协议适配器的模板
   - 包含基本的初始化、请求、响应处理等方法
   - 可以扩展支持WebSocket、MQ、gRPC等协议

2. CustomDatabaseTemplate
   - 创建自定义数据库适配器的模板
   - 包含连接、断开、查询、更新等方法
   - 可以扩展支持MongoDB、Redis等数据库

使用方法：
  1. 复制此文件到适配器目录
  2. 重命名为具体的适配器名称（如my_custom_adapter.py）
  3. 修改类名和实现方法
  4. 在AdapterFactory中注册新的适配器
  5. 在测试中使用新的适配器

创建WebSocket适配器示例：
    from adapters.template_adapter import CustomProtocolTemplate
    
    class WebSocketAdapter(CustomProtocolTemplate):
        def __init__(self, endpoint):
            super().__init__(endpoint)
            self.ws = None
        
        def request(self, data):
            # 实现WebSocket连接和发送消息
            pass

注意：
  - 遵循现有适配器的设计模式
  - 实现共同的接口方法
  - 添加适当的错误处理
  - 编写对应的单元测试
"""

from typing import Any, Dict, Optional


# ============================================================================
# PROTOCOL ADAPTER TEMPLATE
# ============================================================================

class CustomProtocolTemplate:
    """Template for implementing custom protocol adapters."""
    
    def __init__(self, endpoint: str, timeout: int = 30):
        """
        Initialize custom protocol adapter.
        
        Args:
            endpoint: Service endpoint URL
            timeout: Request timeout in seconds
        """
        self.endpoint = endpoint
        self.timeout = timeout
    
    def send_request(self, **kwargs) -> Dict[str, Any]:
        """
        Send a request using your custom protocol.
        
        Args:
            **kwargs: Protocol-specific parameters
        
        Returns:
            Response dict with 'status', 'body', and 'headers'
        """
        try:
            # TODO: Implement your protocol logic here
            # Example:
            # 1. Format request according to your protocol
            # 2. Send request
            # 3. Parse response
            
            response = {
                "status": 200,
                "body": {"message": "success"},
                "headers": {}
            }
            return response
        
        except Exception as e:
            raise Exception(f"Custom protocol request failed: {str(e)}")


# Example: Custom Protocol Implementation
class CustomProtocolAdapter(CustomProtocolTemplate):
    """Example custom protocol adapter."""
    
    def send_request(self, method: str = "GET", 
                    path: str = "/", 
                    data: Optional[Dict] = None) -> Dict[str, Any]:
        """Send request using custom protocol."""
        
        # Your implementation here
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Custom {method} request to {self.endpoint}{path}")
        
        return {
            "status": 200,
            "body": data or {},
            "headers": {"X-Custom-Protocol": "v1"}
        }


# ============================================================================
# DATABASE ADAPTER TEMPLATE
# ============================================================================

class CustomDatabaseTemplate:
    """Template for implementing custom database adapters."""
    
    def __init__(self, host: str, port: int, user: str, 
                 password: str, database: str):
        """
        Initialize custom database adapter.
        
        Args:
            host: Database host
            port: Database port
            user: Database user
            password: Database password
            database: Database name
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def connect(self) -> None:
        """Establish database connection."""
        # TODO: Implement connection logic
        # Example:
        # import your_db_client
        # self.connection = your_db_client.connect(...)
        pass
    
    def disconnect(self) -> None:
        """Close database connection."""
        # TODO: Implement disconnection logic
        if self.connection:
            # self.connection.close()
            pass
    
    def execute_query(self, query: str) -> list:
        """Execute SELECT query and return results."""
        # TODO: Execute query and return results
        return []
    
    def execute_update(self, query: str) -> int:
        """Execute INSERT/UPDATE/DELETE and return affected rows."""
        # TODO: Execute update and return row count
        return 0


# Example: Custom Database Implementation
class MongoDBAdapter(CustomDatabaseTemplate):
    """Example MongoDB adapter."""
    
    def connect(self) -> None:
        """Connect to MongoDB."""
        try:
            from pymongo import MongoClient
            uri = f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}"
            self.connection = MongoClient(uri)
            self.db = self.connection[self.database]
            print(f"Connected to MongoDB: {self.host}:{self.port}")
        except Exception as e:
            raise Exception(f"Failed to connect to MongoDB: {str(e)}")
    
    def disconnect(self) -> None:
        """Disconnect from MongoDB."""
        if self.connection:
            self.connection.close()
            print("Disconnected from MongoDB")
    
    def execute_query(self, query: str) -> list:
        """Execute query (collection.find())."""
        try:
            # Placeholder: use MongoDB aggregation pipeline
            collection_name = query.split('.')[0]
            collection = self.db[collection_name]
            return list(collection.find())
        except Exception as e:
            raise Exception(f"MongoDB query failed: {str(e)}")
    
    def execute_update(self, query: str) -> int:
        """Execute update operation."""
        return 1


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

"""
To use your custom adapter:

1. Create your adapter (copy this template)
2. Save to adapters/your_adapter.py

3. Register in conftest.py:
   
   from adapters.your_adapter import YourCustomAdapter
   from core.adapter_factory import AdapterFactory
   
   AdapterFactory.register_protocol_adapter("custom", YourCustomAdapter)
   # or
   AdapterFactory.register_database_adapter("mongodb", MongoDBAdapter)

4. Use in tests:
   
   from core.adapter_factory import AdapterFactory
   
   adapter = AdapterFactory.get_protocol_adapter("custom", endpoint="...")
   response = adapter.send_request(method="GET", path="/data")
"""
