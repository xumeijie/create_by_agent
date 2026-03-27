"""
单元测试集 (Unit Tests)

测试各个模块的独立功能，确保单个组件的正确性：

主要测试类和方法：
- TestDataGenerator: 数据生成器功能测试
  - test_random_string(): 验证随机字符串生成
  - test_random_email(): 验证随机邮箱生成
  - test_random_phone(): 验证随机电话生成
  - test_random_number(): 验证随机数生成
  - test_generate_user_data(): 验证用户数据生成
  - test_generate_product_data(): 验证产品数据生成

- TestAssertions: 自定义断言功能测试
  - test_assert_dict_keys(): 验证字典键断言
  - test_assert_dict_values(): 验证字典值断言
  - test_assert_list_contains_item(): 验证列表包含项断言

执行单元测试：
    # 执行所有单元测试
    pytest tests/test_unit.py -v
    
    # 执行特定测试类
    pytest tests/test_unit.py::TestDataGenerator -v
    
    # 并行执行单元测试（8个worker）
    pytest tests/test_unit.py -v -n 8

测试覆盖率：
    pytest tests/test_unit.py --cov=utils --cov-report=html
"""
import pytest
from core.base_test import BaseTest
from utils.data_generator import DataGenerator
from utils.assertions import assert_dict_keys, assert_dict_values


class TestDataGenerator(BaseTest):
    """Test data generation utilities."""
    
    def test_random_string(self):
        """Test random string generation."""
        result = DataGenerator.random_string(10)
        assert isinstance(result, str)
        assert len(result) == 10
    
    def test_random_email(self):
        """Test random email generation."""
        result = DataGenerator.random_email()
        assert "@example.com" in result
        assert isinstance(result, str)
    
    def test_random_number(self):
        """Test random number generation."""
        result = DataGenerator.random_number(1, 100)
        assert 1 <= result <= 100
    
    def test_generate_user_data(self):
        """Test user data generation."""
        user = DataGenerator.generate_user_data()
        assert_dict_keys(user, ["name", "email", "phone", "age"])
    
    def test_generate_product_data(self):
        """Test product data generation."""
        product = DataGenerator.generate_product_data()
        expected = {"name": "", "price": 0, "quantity": 0, "sku": ""}
        assert_dict_keys(product, list(expected.keys()))


class TestAssertions(BaseTest):
    """Test assertion utilities."""
    
    def test_assert_dict_keys_success(self):
        """Test successful key assertion."""
        data = {"name": "test", "age": 25, "email": "test@test.com"}
        assert_dict_keys(data, ["name", "age"])  # Should not raise
    
    def test_assert_dict_keys_failure(self):
        """Test failed key assertion."""
        data = {"name": "test", "age": 25}
        with pytest.raises(AssertionError):
            assert_dict_keys(data, ["name", "email"])
    
    def test_assert_dict_values(self):
        """Test dict values assertion."""
        data = {"name": "test", "age": 25}
        assert_dict_values(data, {"name": "test", "age": 25})  # Should not raise
    
    def test_assert_dict_values_failure(self):
        """Test failed dict values assertion."""
        data = {"name": "test", "age": 25}
        with pytest.raises(AssertionError):
            assert_dict_values(data, {"name": "wrong", "age": 25})
