"""
模拟工具库 (Mocking Utilities)

创建和管理测试中的模拟对象，隔离外部依赖：

1. ResponseMocker类
   - create_http_response(): 创建模拟HTTP响应对象
   - 模拟状态码、headers、body内容
   - 支持JSON和文本响应

2. RequestMocker类
   - create_mock_request(): 创建模拟请求对象
   - create_database_connection(): 模拟数据库连接
   - create_database_cursor(): 模拟数据库游标

使用示例：
    from utils.mocking import ResponseMocker, RequestMocker
    
    # 模拟HTTP响应
    response = ResponseMocker.create_http_response(
        status_code=200,
        json_data={"user_id": 123, "name": "John"}
    )
    
    # 模拟数据库连接
    mock_conn = RequestMocker.create_database_connection()
    mock_cursor = RequestMocker.create_database_cursor()
    mock_cursor.fetchone.return_value = (1, 'test_data')
    
    # 在测试中使用patch
    with patch('requests.get', return_value=response):
        # 测试代码
        pass
"""
from unittest.mock import Mock, MagicMock, patch
from typing import Any, Dict, Optional


class ResponseMocker:
    """Mock response data for testing."""
    
    @staticmethod
    def create_http_response(status_code: int = 200, data: Dict = None) -> Mock:
        """Create mock HTTP response."""
        response = Mock()
        response.status_code = status_code
        response.json.return_value = data or {"success": True}
        response.text = str(data or {})
        response.headers = {"Content-Type": "application/json"}
        return response
    
    @staticmethod
    def create_database_cursor(rows: list) -> Mock:
        """Create mock database cursor."""
        cursor = Mock()
        cursor.fetchall.return_value = rows
        cursor.rowcount = len(rows)
        return cursor
    
    @staticmethod
    def create_database_connection(rows_result: list = None) -> Mock:
        """Create mock database connection."""
        connection = Mock()
        cursor = ResponseMocker.create_database_cursor(rows_result or [])
        connection.cursor.return_value = cursor
        return connection


class RequestMocker:
    """Mock request data."""
    
    @staticmethod
    def create_http_request(method: str = "GET", 
                           headers: Dict = None, 
                           data: Dict = None) -> Mock:
        """Create mock HTTP request."""
        request = Mock()
        request.method = method
        request.headers = headers or {}
        request.data = data or {}
        return request
    
    @staticmethod
    def create_soap_request(service: str = "", method: str = "", 
                           data: Dict = None) -> Mock:
        """Create mock SOAP request."""
        request = Mock()
        request.service = service
        request.method = method
        request.data = data or {}
        return request


def mock_http_adapter(status: int = 200, response_data: Dict = None):
    """Context manager to mock HTTP adapter."""
    class MockHTTPAdapter:
        def __init__(self):
            self.status = status
            self.response_data = response_data or {}
        
        def send_request(self, method, endpoint, data=None, headers=None):
            return {
                "status": self.status,
                "body": self.response_data,
                "headers": {}
            }
    
    return MockHTTPAdapter()


def mock_database_adapter(rows: list = None):
    """Context manager to mock database adapter."""
    class MockDatabaseAdapter:
        def __init__(self):
            self.rows = rows or []
        
        def connect(self):
            pass
        
        def disconnect(self):
            pass
        
        def execute_query(self, query):
            return self.rows
        
        def execute_update(self, query):
            return len(self.rows)
    
    return MockDatabaseAdapter()
