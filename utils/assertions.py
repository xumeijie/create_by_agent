"""
自定义断言函数 (Custom Assertions)

提供可读性更强的断言函数，用于测试中的验证：

提供的函数：
- assert_dict_keys(): 检查字典中是否包含所有期望的键
- assert_dict_values(): 检查字典中特定键的值是否匹配
- assert_response_contains(): 检查API响应体中是否包含期望内容
- assert_status_code(): 检查HTTP响应状态码
- assert_json_valid(): 验证字符串是否为有效JSON
- assert_list_contains_item(): 检查列表中是否包含指定项

使用示例：
    from utils.assertions import assert_status_code, assert_dict_keys
    
    response = {"status": 200, "body": {"id": 1, "name": "John"}}
    assert_status_code(response, 200)  # 检查状态码
    assert_dict_keys(response["body"], ["id", "name"])  # 检查必要字段
    
    users = [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]
    assert_list_contains_item(users, {"id": 1}, key="id")  # 检查列表中是否包含
"""
import json
from typing import Any, Dict, List, Optional


def assert_dict_keys(data: Dict, expected_keys: List[str]) -> None:
    """Assert that dictionary contains all expected keys."""
    missing_keys = set(expected_keys) - set(data.keys())
    assert not missing_keys, f"Missing keys: {missing_keys}"


def assert_dict_values(data: Dict, expected_values: Dict) -> None:
    """Assert that dictionary values match expected values."""
    for key, expected_value in expected_values.items():
        actual_value = data.get(key)
        assert actual_value == expected_value, \
            f"Key '{key}': expected {expected_value}, got {actual_value}"


def assert_response_contains(response: Dict[str, Any], expected_content: Dict) -> None:
    """Assert that response contains expected content."""
    body = response.get("body", {})
    assert_dict_keys(body, list(expected_content.keys()))
    assert_dict_values(body, expected_content)


def assert_status_code(response: Dict[str, Any], expected_status: int) -> None:
    """Assert that response status matches expected."""
    actual_status = response.get("status")
    assert actual_status == expected_status, \
        f"Expected status {expected_status}, got {actual_status}"


def assert_json_valid(json_str: str) -> Dict:
    """Assert that string is valid JSON and return parsed data."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON: {str(e)}")


def assert_list_contains_item(items: List[Any], expected_item: Any, 
                             key: Optional[str] = None) -> None:
    """Assert that list contains an item."""
    if key:
        item_found = any(item.get(key) == expected_item.get(key) for item in items)
        assert item_found, f"Item with {key}={expected_item.get(key)} not found in list"
    else:
        assert expected_item in items, f"Item {expected_item} not found in list"
