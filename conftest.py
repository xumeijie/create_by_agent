"""
Pytest配置文件 (Pytest Configuration)

配置pytest测试框架和定义全局fixture：

主要fixture：
1. setup_test_environment: 会话级别fixture
   - 初始化配置管理器
   - 注册所有适配器
   - 一次性执行，在所有测试前运行

2. config_manager: 函数级别fixture
   - 提供ConfigManager实例给测试函数
   - 用于访问配置信息

3. adapter_factory: 函数级别fixture
   - 提供AdapterFactory实例给测试函数
   - 用于创建协议和数据库适配器

4. cleanup_test_data: 函数级别fixture
   - 测试后清理临时数据
   - 使用yield进行setup/teardown

pytest配置说明：
  - log_cli: 显示控制台日志
  - log_level: 日志级别设置（INFO/DEBUG/WARNING）
  - addopts: 额外的pytest选项
  - 支持-n参数进行并行执行
  - 支持标记(markers)区分测试类型

使用示例：
    def test_with_config(config_manager):
        # 使用全局fixture
        db_config = config_manager.get_db_config('mysql')
        assert db_config is not None
    
    @pytest.mark.integration
    def test_adapter_integration(adapter_factory):
        # 使用适配器工厂
        http_adapter = adapter_factory.get_protocol_adapter('http')
        response = http_adapter.get(url='https://example.com')
"""
import pytest
import logging
from core.config_manager import ConfigManager
from core.adapter_factory import AdapterFactory
from adapters.protocol_adapter import HTTPAdapter, SOAPAdapter, GraphQLAdapter
from adapters.database_adapter import MySQLAdapter, OracleAdapter, PostgreSQLAdapter


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup test environment once at the start of test session."""
    # Initialize config manager
    config = ConfigManager()
    config.load_config("dev")
    
    # Register adapters
    AdapterFactory.register_protocol_adapter("http", HTTPAdapter)
    AdapterFactory.register_protocol_adapter("soap", SOAPAdapter)
    AdapterFactory.register_protocol_adapter("graphql", GraphQLAdapter)
    
    AdapterFactory.register_database_adapter("mysql", MySQLAdapter)
    AdapterFactory.register_database_adapter("oracle", OracleAdapter)
    AdapterFactory.register_database_adapter("postgresql", PostgreSQLAdapter)
    
    yield
    
    # Cleanup


@pytest.fixture
def config_manager():
    """Provide config manager instance."""
    return ConfigManager()


@pytest.fixture
def adapter_factory():
    """Provide adapter factory."""
    return AdapterFactory


@pytest.fixture
def http_adapter():
    """Provide HTTP adapter."""
    return HTTPAdapter(base_url="http://localhost:8080")


@pytest.fixture
def mock_http_response():
    """Provide mock HTTP response."""
    def _response(status=200, data=None):
        return {
            "status": status,
            "body": data or {},
            "headers": {"Content-Type": "application/json"}
        }
    return _response


def pytest_collection_modifyitems(config, items):
    """Modify test items before collection."""
    for item in items:
        # Mark slow tests
        if "slow" in item.nodeid:
            item.add_marker(pytest.mark.slow)
        
        # Add environment marker
        if "integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "unit" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        elif "performance" in item.nodeid:
            item.add_marker(pytest.mark.performance)
        elif "security" in item.nodeid:
            item.add_marker(pytest.mark.security)
