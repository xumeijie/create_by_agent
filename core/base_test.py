"""
基础测试类 (BaseTest)

所有测试类的父类，提供以下功能：
- 自动setup/teardown: 每个测试前后自动初始化和清理
- 日志记录: 测试开始和结束时自动记录日志
- 响应断言: 提供assert_response方法验证API响应

使用示例：
    from core.base_test import BaseTest
    
    class TestUserAPI(BaseTest):
        def test_get_user(self):
            response = {"status": 200, "data": {"id": 1}}
            self.assert_response(response, 200, ["data"])
"""
import pytest
import logging
from typing import Any, Dict, Optional


logger = logging.getLogger(__name__)


class BaseTest:
    """Base test class with common setup and teardown."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup before each test."""
        logger.info(f"Starting test: {self.__class__.__name__}")
        self.test_data = {}
        yield
        logger.info(f"Completed test: {self.__class__.__name__}")
    
    def assert_response(self, response: Dict[str, Any], expected_status: int, 
                       expected_keys: Optional[list] = None) -> None:
        """Common assertion helper for API responses."""
        assert response.get("status") == expected_status, \
            f"Expected status {expected_status}, got {response.get('status')}"
        
        if expected_keys:
            for key in expected_keys:
                assert key in response, f"Expected key '{key}' not found in response"
        
        logger.info(f"Response assertion passed - Status: {expected_status}")
