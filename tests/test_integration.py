"""
集成测试集 (Integration Tests)

测试多个模块间的协作和实际系统的集成功能：

主要测试类和方法：
- TestHTTPAdapterIntegration: HTTP网络适配器集成测试
  - test_adapter_registration(): 验证适配器注册机制
  - test_get_request_success(): 验证HTTP GET请求成功
  - test_api_error_handling(): 验证错误处理机制

测试特点：
  - 使用真实的外部API (jsonplaceholder.typicode.com)
  - 验证适配器工厂的创建和管理能力
  - 测试HTTP协议的实际通信能力
  - 演示错误处理流程

执行集成测试：
    # 执行所有集成测试
    pytest tests/test_integration.py -v
    
    # 执行特定测试类
    pytest tests/test_integration.py::TestHTTPAdapterIntegration -v
    
    # 显示详细输出（包括print语句）
    pytest tests/test_integration.py -v -s

注意：
    - 集成测试需要网络连接
    - 外部API响应时间较长，执行速度会变慢
    - 建议分离集成测试和单元测试分别执行
"""
import pytest
from core.base_test import BaseTest
from adapters.protocol_adapter import HTTPAdapter
from utils.assertions import assert_status_code, assert_dict_keys


class TestHTTPAdapterIntegration(BaseTest):
    """Test HTTP adapter integration."""
    
    @pytest.fixture(autouse=True)
    def setup_http_adapter(self):
        """Setup HTTP adapter."""
        self.adapter = HTTPAdapter(base_url="https://jsonplaceholder.typicode.com")
        yield
        # Cleanup if needed
    
    def test_get_request(self):
        """Test GET request."""
        response = self.adapter.send_request("GET", "/posts/1")
        assert_status_code(response, 200)
        body = response.get("body", {})
        assert_dict_keys(body, ["id", "userId", "title"])
    
    def test_api_error_handling(self):
        """Test API error handling."""
        with pytest.raises(Exception):
            # This should fail or return error
            self.adapter.send_request("GET", "/invalid-endpoint")


class TestAdapterFactory(BaseTest):
    """Test adapter factory pattern."""
    
    def test_register_and_retrieve_adapter(self):
        """Test registering and retrieving adapters."""
        from core.adapter_factory import AdapterFactory
        from adapters.protocol_adapter import HTTPAdapter
        
        # Register adapter
        AdapterFactory.register_protocol_adapter("http", HTTPAdapter)
        
        # Verify registration
        adapters = AdapterFactory.list_protocol_adapters()
        assert "http" in adapters
        
        # Retrieve and verify instance
        adapter = AdapterFactory.get_protocol_adapter("http", 
                                                      base_url="http://localhost:8080")
        assert isinstance(adapter, HTTPAdapter)
