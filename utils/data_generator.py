"""
测试数据生成器 (Data Generator)

自动生成随机测试数据，避免硬编码测试数据：

1. DataGenerator类
   - random_string(): 生成随机字符串
   - random_email(): 生成随机邮箱
   - random_phone(): 生成随机电话号码
   - random_number(): 生成范围内的随机数
   - random_date(): 生成随机日期
   - random_datetime(): 生成随机日期时间
   - generate_user_data(): 生成完整的用户测试数据
   - generate_product_data(): 生成完整的产品测试数据

2. MockDataProvider类
   - get_http_response(): 生成模拟的HTTP响应
   - get_database_rows(): 生成模拟的数据库行数据

使用示例：
    from utils.data_generator import DataGenerator, MockDataProvider
    
    # 生成随机数据
    user = DataGenerator.generate_user_data()
    # {'name': 'abc123', 'email': 'xyz@example.com', 'phone': '1234567890', 'age': 35}
    
    product = DataGenerator.generate_product_data()
    # {'name': 'Product_xyz', 'price': 456, 'quantity': 23, 'sku': 'ABC123'}
    
    # 生成模拟数据
    response = MockDataProvider.get_http_response(200, {"success": True})
    rows = MockDataProvider.get_database_rows(count=5)
"""
import random
import string
from datetime import datetime, timedelta
from typing import Any, Dict, List


class DataGenerator:
    """Generate test data."""
    
    @staticmethod
    def random_string(length: int = 10) -> str:
        """Generate random string."""
        return ''.join(random.choices(string.ascii_letters, k=length))
    
    @staticmethod
    def random_email() -> str:
        """Generate random email."""
        username = DataGenerator.random_string(8)
        return f"{username}@example.com"
    
    @staticmethod
    def random_number(min_val: int = 1, max_val: int = 1000) -> int:
        """Generate random number."""
        return random.randint(min_val, max_val)
    
    @staticmethod
    def random_phone() -> str:
        """Generate random phone number."""
        return ''.join(random.choices(string.digits, k=10))
    
    @staticmethod
    def random_date(days_offset: int = 0) -> str:
        """Generate random date."""
        date = datetime.now() + timedelta(days=days_offset)
        return date.strftime("%Y-%m-%d")
    
    @staticmethod
    def random_datetime(days_offset: int = 0) -> str:
        """Generate random datetime."""
        dt = datetime.now() + timedelta(days=days_offset)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def generate_user_data() -> Dict[str, Any]:
        """Generate user test data."""
        return {
            "name": DataGenerator.random_string(8),
            "email": DataGenerator.random_email(),
            "phone": DataGenerator.random_phone(),
            "age": DataGenerator.random_number(18, 80)
        }
    
    @staticmethod
    def generate_product_data() -> Dict[str, Any]:
        """Generate product test data."""
        return {
            "name": f"Product_{DataGenerator.random_string(5)}",
            "price": DataGenerator.random_number(10, 1000),
            "quantity": DataGenerator.random_number(1, 100),
            "sku": DataGenerator.random_string(6).upper()
        }


class MockDataProvider:
    """Provide mock data for testing."""
    
    @staticmethod
    def get_http_response(status: int = 200, data: Dict = None) -> Dict[str, Any]:
        """Get mock HTTP response."""
        return {
            "status": status,
            "body": data or {"message": "success"},
            "headers": {"Content-Type": "application/json"}
        }
    
    @staticmethod
    def get_database_rows(count: int = 5) -> List[Dict[str, Any]]:
        """Generate mock database rows."""
        return [
            {
                "id": i,
                "name": f"Item_{i}",
                "value": DataGenerator.random_number()
            }
            for i in range(1, count + 1)
        ]
