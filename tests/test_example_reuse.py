"""
框架复用示例 (Framework Reuse Example)

演示如何使用该测试框架来编写自己的测试套件:

这个文件是一个完整的示例，展示：
  1. 如何继承BaseTest来创建自己的测试类
  2. 如何使用AdapterFactory和ConfigManager
  3. 如何使用自定义断言进行验证
  4. 如何使用DataGenerator生成测试数据
  5. 如何组织和执行测试

关键要点：
  - 继承BaseTest获得公共功能（setup、teardown）
  - 使用AdapterFactory创建协议适配器
  - 使用ConfigManager获取环境配置
  - 使用assert_*系列函数进行清晰的断言
  - 使用DataGenerator生成动态测试数据

快速开始：
  1. 复制此文件为 tests/test_my_api.py
  2. 修改TestExampleAPI类名为你的API名称
  3. 更新endpoint和断言条件
  4. 运行: pytest tests/test_my_api.py -v

最佳实践：
  - 一个测试类对应一个API资源
  - 测试方法名以test_开头
  - 使用有意义的测试方法名
  - 每个测试只验证一个核心功能
  - 使用fixtures管理测试数据生命周期
  - 充分利用断言库简化代码
"""

from core.base_test import BaseTest
from core.adapter_factory import AdapterFactory
from core.config_manager import ConfigManager
from utils.assertions import (
    assert_status_code,
    assert_dict_keys,
    assert_response_contains
)
from utils.data_generator import DataGenerator
import pytest


class TestExampleAPI(BaseTest):
    """
    Example test suite showing how to reuse the framework.
    
    CUSTOMIZATION STEPS:
    1. Update config/environments.yaml with your API endpoint
    2. Replace "example" with your API name
    3. Replace endpoint paths with your actual API paths
    4. Replace assertions with your business logic
    """
    
    @pytest.fixture(autouse=True)
    def setup_adapter(self):
        """Setup HTTP adapter with your API endpoint."""
        config = ConfigManager()
        api_config = config.get_api_config("http")
        
        self.adapter = AdapterFactory.get_protocol_adapter(
            "http",
            base_url=api_config.get("base_url", "http://localhost:8080")
        )
        
        yield
    
    def test_get_resource_list(self):
        """
        Example: Test GET endpoint that returns a list.
        
        CUSTOMIZE:
        - Change endpoint path: "/your-resource"
        - Change expected keys based on your response
        """
        response = self.adapter.send_request("GET", "/users")
        
        # Verify response status
        assert_status_code(response, 200)
        
        # Verify response structure
        body = response.get("body", {})
        assert isinstance(body.get("data"), list)
        
        # Verify first item structure (if list not empty)
        if body.get("data"):
            first_item = body["data"][0]
            expected_keys = ["id", "name", "email"]
            assert_dict_keys(first_item, expected_keys)
    
    def test_get_single_resource(self):
        """
        Example: Test GET endpoint for single resource.
        
        CUSTOMIZE:
        - Change resource ID
        - Change endpoint path
        - Change expected response structure
        """
        resource_id = 1
        response = self.adapter.send_request("GET", f"/users/{resource_id}")
        
        assert_status_code(response, 200)
        
        body = response.get("body", {})
        assert_dict_keys(body, ["id", "name", "email", "created_at"])
    
    def test_create_resource(self):
        """
        Example: Test POST endpoint that creates a resource.
        
        CUSTOMIZE:
        - Generate test data appropriate for your API
        - Change endpoint path
        - Update assertions for your response format
        """
        # Generate test data
        user_data = {
            "name": DataGenerator.random_string(10),
            "email": DataGenerator.random_email(),
            "age": DataGenerator.random_number(18, 80)
        }
        
        # Send request
        response = self.adapter.send_request(
            "POST",
            "/users",
            data=user_data
        )
        
        # Verify response
        assert_status_code(response, 201)  # Or your expected status
        
        body = response.get("body", {})
        assert "id" in body  # Verify resource was created
        assert body.get("name") == user_data["name"]
    
    def test_update_resource(self):
        """
        Example: Test PUT endpoint that updates a resource.
        
        CUSTOMIZE:
        - Change resource ID
        - Change update data
        - Update assertions
        """
        resource_id = 1
        update_data = {
            "name": DataGenerator.random_string(10),
            "email": DataGenerator.random_email()
        }
        
        response = self.adapter.send_request(
            "PUT",
            f"/users/{resource_id}",
            data=update_data
        )
        
        assert_status_code(response, 200)
        
        # Verify update
        body = response.get("body", {})
        assert body.get("name") == update_data["name"]
    
    def test_delete_resource(self):
        """
        Example: Test DELETE endpoint.
        
        CUSTOMIZE:
        - Change resource ID
        - Update expected status code (204 is common)
        """
        resource_id = 999  # Use a test/dummy ID
        
        response = self.adapter.send_request(
            "DELETE",
            f"/users/{resource_id}"
        )
        
        # Most APIs return 200, 204, or 202 for successful deletion
        assert response.get("status") in [200, 204, 202]
    
    def test_error_handling_invalid_id(self):
        """
        Example: Test error handling for invalid input.
        
        CUSTOMIZE:
        - Change endpoint and invalid input
        - Update expected status code
        """
        response = self.adapter.send_request(
            "GET",
            "/users/invalid-id"
        )
        
        # Expecting 400 Bad Request or 404 Not Found
        assert response.get("status") in [400, 404]
        
        body = response.get("body", {})
        assert "error" in body or "message" in body
    
    @pytest.mark.integration
    def test_workflow_create_and_read(self):
        """
        Example: Test workflow spanning multiple endpoints.
        
        CUSTOMIZE:
        - Implement your actual workflow
        - Test multiple related operations
        """
        # Step 1: Create a resource
        user_data = DataGenerator.generate_user_data()
        create_response = self.adapter.send_request(
            "POST",
            "/users",
            data=user_data
        )
        assert_status_code(create_response, 201)
        
        created_user = create_response.get("body", {})
        user_id = created_user.get("id")
        
        # Step 2: Read the created resource
        read_response = self.adapter.send_request(
            "GET",
            f"/users/{user_id}"
        )
        assert_status_code(read_response, 200)
        
        # Step 3: Verify data matches
        read_user = read_response.get("body", {})
        assert read_user.get("name") == created_user.get("name")
        assert read_user.get("email") == created_user.get("email")


# ============================================================================
# ADVANCED EXAMPLES
# ============================================================================

class TestAPIWithDatabase(BaseTest):
    """
    Example: Test API with database verification.
    
    Verifies that API correctly updates the database.
    """
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup both API adapter and database adapter."""
        self.http = AdapterFactory.get_protocol_adapter(
            "http",
            base_url="http://localhost:8080"
        )
        
        config = ConfigManager()
        db_config = config.get_db_config("mysql")
        
        self.db = AdapterFactory.get_database_adapter(
            "mysql",
            **db_config
        )
        
        self.db.connect()
        yield
        self.db.disconnect()
    
    def test_api_updates_database(self):
        """Test that API call updates database correctly."""
        # Call API to create resource
        user_data = DataGenerator.generate_user_data()
        response = self.http.send_request("POST", "/users", data=user_data)
        assert_status_code(response, 201)
        
        # Verify in database
        user_id = response.get("body", {}).get("id")
        results = self.db.execute_query(
            f"SELECT * FROM users WHERE id = {user_id}"
        )
        
        assert len(results) == 1
        assert results[0]["email"] == user_data["email"]


@pytest.mark.smoke
def test_api_is_healthy():
    """
    Quick smoke test - verify API is running.
    
    CUSTOMIZE:
    - Change endpoint to your health check endpoint
    - Update status code if different
    """
    adapter = AdapterFactory.get_protocol_adapter(
        "http",
        base_url="http://localhost:8080"
    )
    
    response = adapter.send_request("GET", "/health")
    assert_status_code(response, 200)


# ============================================================================
# NOTES
# ============================================================================

"""
CUSTOMIZATION CHECKLIST:

Before running these tests:

1. ✅ Update config/environments.yaml with your API endpoint
2. ✅ Change test class names to match your API (TestUserAPI, TestProductAPI)
3. ✅ Replace endpoint paths with your actual API paths
4. ✅ Update test data generation to match your API schema
5. ✅ Review and update assertions for your response format
6. ✅ Add/remove test methods based on your endpoints

RUNNING TESTS:

# Run all tests
pytest tests/test_example_reuse.py

# Run only smoke tests
pytest -m smoke tests/

# Run with detailed output
pytest -v tests/test_example_reuse.py

# Run in parallel
pytest -n auto tests/

NEXT STEPS:

1. Copy this file: cp tests/test_example_reuse.py tests/test_my_api.py
2. Customize for your API
3. Run: pytest tests/test_my_api.py
4. Delete this file when done

Good luck! 🚀
"""
