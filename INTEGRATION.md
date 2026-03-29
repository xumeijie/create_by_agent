# 框架集成指南 (Framework Integration Guide)

本文档说明如何将该测试自动化框架集成到新的系统中，需要修改哪些文件，以及如何进行必要的配置。

## 📋 快速概览

将框架集成到新系统需要修改 **7 个关键文件**，按优先级排列：

| 优先级 | 文件 | 目的 | 修改内容 |
|------|------|------|---------|
| 🔴 高 | `config/dev.yaml` | 开发环境配置 | API端点、数据库连接 |
| 🔴 高 | `config/staging.yaml` | 测试环境配置 | 测试环境的API、数据库 |
| 🔴 高 | `config/prod.yaml` | 生产环境配置 | 生产环境的API、数据库 |
| 🟡 中 | `adapters/protocol_adapter.py` | 协议适配器 | 添加项目特需的通信协议 |
| 🟡 中 | `adapters/database_adapter.py` | 数据库适配器 | 支持新的数据库类型 |
| 🟡 中 | `conftest.py` | 测试配置 | 自定义Fixture和全局设置 |
| 🟢 低 | `tests/` | 测试套件 | 编写项目特定的测试 |

---

## 第一步：配置环境文件（必需）

### 1.1 修改 `config/dev.yaml`

**用途**：配置本地开发环境的API端点和数据库连接

**原始内容示例**：
```yaml
# Development environment configuration
environment: development
log_level: DEBUG

# API Configuration
api:
  base_url: http://localhost:8080
  timeout: 30
  retry_count: 3
```

**修改步骤**：

```yaml
# Development environment configuration
environment: development
log_level: DEBUG

# API Configuration - 【修改这里】
api:
  base_url: http://你的开发API地址:端口      # 例如: http://192.168.1.100:8080
  timeout: 30
  retry_count: 3
  
  # 如果有多个API端点，添加它们
  endpoints:
    user_api: http://dev-user-api:8081
    product_api: http://dev-product-api:8082
    order_api: http://dev-order-api:8083

# Database Configuration - 【修改这里】
database:
  mysql:
    host: localhost                    # 修改为你的MySQL主机
    port: 3306
    username: root                     # 修改为你的用户名
    password: ${MYSQL_PASSWORD}        # 建议使用环境变量
    database: test_db                  # 修改为你的数据库名
    charset: utf8mb4
    
  postgresql:
    host: localhost                    # PostgreSQL主机
    port: 5432
    username: postgres
    password: ${PG_PASSWORD}
    database: test_db
    
  # 如果使用Oracle或其他数据库，配置如下
  oracle:
    host: localhost
    port: 1521
    username: system
    password: ${ORACLE_PASSWORD}
    database: ORCL

# 认证配置（如果需要）
auth:
  enabled: true
  type: bearer                         # 或 basic, oauth2
  token: ${AUTH_TOKEN}                # 从环境变量读取
```

**环境变量设置**：
```bash
# 在 .env 文件中添加敏感信息
export MYSQL_PASSWORD="your_mysql_password"
export PG_PASSWORD="your_pg_password"
export ORACLE_PASSWORD="your_oracle_password"
export AUTH_TOKEN="your_auth_token"
```

---

### 1.2 修改 `config/staging.yaml`

**用途**：配置测试（预发布）环境配置

**修改内容**：
- 连接到测试环境的API和数据库
- 通常与生产配置类似，但使用测试数据库
- 配置测试专用的认证凭证

```yaml
# Staging environment configuration
environment: staging
log_level: INFO

api:
  base_url: http://staging-api.company.com    # 测试环境API地址
  timeout: 30
  retry_count: 3

database:
  mysql:
    host: staging-mysql.company.com
    port: 3306
    username: staging_user
    password: ${STAGING_MYSQL_PASSWORD}
    database: staging_db
    charset: utf8mb4

auth:
  enabled: true
  type: bearer
  token: ${STAGING_AUTH_TOKEN}
```

---

### 1.3 修改 `config/prod.yaml`

**用途**：配置生产环境配置

**修改内容**：
- 连接到生产环境的API和数据库
- 更严格的日志级别（INFO或WARNING）
- 更高的超时和重试设置

```yaml
# Production environment configuration
environment: production
log_level: WARNING

api:
  base_url: https://api.company.com          # 生产环境API地址
  timeout: 60
  retry_count: 5                             # 生产环境应该有更多重试次数

database:
  mysql:
    host: prod-mysql.company.com
    port: 3306
    username: prod_user
    password: ${PROD_MYSQL_PASSWORD}
    database: prod_db
    charset: utf8mb4

auth:
  enabled: true
  type: bearer
  token: ${PROD_AUTH_TOKEN}

# 生产环境应该启用更详细的日志和监控
logging:
  file: /var/log/test_automation/test.log
  rotation: daily
  retention: 30  # 保留30天的日志
```

---

## 第二步：适配通信协议（如果需要）

### 2.1 修改 `adapters/protocol_adapter.py`

**何时需要修改**：
- ✅ 需要支持WebSocket协议
- ✅ 需要支持gRPC协议
- ✅ 需要支持MessageQueue（MQ）
- ✅ 需要自定义HTTP头或认证方式
- ✅ 项目使用特殊的通信协议

**修改示例 - 添加WebSocket支持**：

```python
# 在现有的 HTTPAdapter, SOAPAdapter, GraphQLAdapter 之后添加

class WebSocketAdapter(BaseProtocolAdapter):
    """WebSocket协议适配器"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        """初始化WebSocket适配器"""
        super().__init__(base_url, timeout)
        self.ws = None
    
    def connect(self):
        """连接到WebSocket服务器"""
        import asyncio
        import websockets
        
        async def _connect():
            self.ws = await websockets.connect(self.base_url)
        
        asyncio.run(_connect())
    
    def send_message(self, message: dict) -> dict:
        """发送WebSocket消息"""
        import asyncio
        import json
        
        async def _send():
            await self.ws.send(json.dumps(message))
            response = await self.ws.recv()
            return json.loads(response)
        
        return asyncio.run(_send())
    
    def disconnect(self):
        """断开连接"""
        import asyncio
        asyncio.run(self.ws.close())
```

**修改示例 - 自定义HTTP认证**：

```python
# 修改 HTTPAdapter 类中的 request 方法

class HTTPAdapter(BaseProtocolAdapter):
    """HTTP协议适配器 - 已修改以支持自定义认证"""
    
    def __init__(self, base_url: str, timeout: int = 30, api_key: str = None):
        super().__init__(base_url, timeout)
        self.api_key = api_key
    
    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """发送HTTP请求，支持自定义认证"""
        url = f"{self.base_url}/{endpoint}"
        
        # 添加自定义认证头
        headers = kwargs.get("headers", {})
        if self.api_key:
            headers["X-API-Key"] = self.api_key  # 使用你的项目的认证头名称
        headers["Authorization"] = "Bearer YOUR_TOKEN"  # 添加Bearer token
        kwargs["headers"] = headers
        
        try:
            response = requests.request(method, url, timeout=self.timeout, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            self.logger.error(f"HTTP request failed: {e}")
            raise
```

---

## 第三步：适配数据库连接（如果需要）

### 3.1 修改 `adapters/database_adapter.py`

**何时需要修改**：
- ✅ 需要支持MongoDB等NoSQL数据库
- ✅ 需要支持Redis缓存
- ✅ 需要自定义连接池配置
- ✅ 需要特殊的数据库连接参数

**修改示例 - 添加MongoDB支持**：

```python
# 在现有的 MySQLAdapter, OracleAdapter, PostgreSQLAdapter 之后添加

class MongoDBAdapter(BaseDatabaseAdapter):
    """MongoDB适配器"""
    
    def __init__(self, host: str, port: int = 27017, database: str = "test_db"):
        """初始化MongoDB适配器"""
        super().__init__(host, port, database)
        self.client = None
        self.db = None
    
    def connect(self) -> bool:
        """连接到MongoDB"""
        try:
            from pymongo import MongoClient
            
            self.client = MongoClient(f"mongodb://{self.host}:{self.port}/")
            self.db = self.client[self.database]
            self.logger.info(f"Successfully connected to MongoDB: {self.host}:{self.port}")
            return True
        except Exception as e:
            self.logger.error(f"MongoDB connection failed: {e}")
            return False
    
    def execute_query(self, collection: str, query: dict) -> list:
        """执行查询操作"""
        try:
            results = list(self.db[collection].find(query))
            return results
        except Exception as e:
            self.logger.error(f"MongoDB query failed: {e}")
            return []
    
    def execute_update(self, collection: str, filter_query: dict, update_data: dict) -> bool:
        """执行更新操作"""
        try:
            result = self.db[collection].update_one(filter_query, {"$set": update_data})
            return result.modified_count > 0
        except Exception as e:
            self.logger.error(f"MongoDB update failed: {e}")
            return False
    
    def disconnect(self) -> bool:
        """断开MongoDB连接"""
        try:
            if self.client:
                self.client.close()
            self.logger.info("Disconnected from MongoDB")
            return True
        except Exception as e:
            self.logger.error(f"MongoDB disconnection failed: {e}")
            return False
```

---

## 第四步：自定义测试Fixtures（可选）

### 4.1 修改 `conftest.py`

**何时需要修改**：
- ✅ 需要特殊的测试数据初始化
- ✅ 需要自定义的登录流程
- ✅ 需要在测试前后执行清理操作
- ✅ 需要定制化的报告生成

**修改示例 - 添加自定义登录Fixture**：

```python
# 在现有 fixture 之后添加

@pytest.fixture
def authenticated_http_adapter(adapter_factory, config_manager):
    """提供已认证的HTTP适配器（项目特定）"""
    adapter = adapter_factory.get_protocol_adapter('http')
    
    # 执行登录操作
    login_endpoint = config_manager.get_api_config()['endpoints']['login']
    credentials = {
        'username': config_manager.get('auth', 'username'),
        'password': config_manager.get('auth', 'password')
    }
    
    response = adapter.post(endpoint=login_endpoint, json=credentials)
    
    # 提取并设置认证token
    if response.status_code == 200:
        token = response.json().get('token')
        adapter.headers = {'Authorization': f'Bearer {token}'}
    
    yield adapter


@pytest.fixture
def test_database_setup(db_adapter):
    """在测试前初始化测试数据库"""
    # 测试前：创建测试数据
    db_adapter.execute_update('users', {}, {'status': 'inactive'})
    
    yield db_adapter
    
    # 测试后：清理测试数据
    db_adapter.execute_update('users', {'test': True}, {})


@pytest.fixture(scope="session")
def setup_test_data_files():
    """准备测试数据文件"""
    import json
    import os
    
    test_data_dir = "tests/test_data"
    os.makedirs(test_data_dir, exist_ok=True)
    
    # 生成示例测试数据文件
    test_data = {
        "users": [
            {"id": 1, "name": "Test User 1", "email": "user1@test.com"},
            {"id": 2, "name": "Test User 2", "email": "user2@test.com"}
        ]
    }
    
    with open(os.path.join(test_data_dir, "sample_data.json"), "w") as f:
        json.dump(test_data, f, indent=2)
    
    yield
    
    # 清理
    import shutil
    shutil.rmtree(test_data_dir, ignore_errors=True)
```

---

## 第五步：编写项目特定的测试（必需）

### 5.1 在 `tests/` 目录中创建测试文件

**文件命名规则**：
```
tests/test_<功能名>.py      # 例如：test_user_management.py
tests/test_<模块名>_<功能>.py  # 例如：test_api_authentication.py
```

**创建示例 - `tests/test_user_api.py`**：

```python
"""
用户API集成测试 (User API Integration Tests)

测试用户管理相关的API端点
"""

import pytest
from core.base_test import BaseTest
from utils.assertions import assert_status_code, assert_dict_keys
from utils.data_generator import DataGenerator


class TestUserAPI(BaseTest):
    """用户API测试类"""
    
    @pytest.fixture(autouse=True)
    def setup_user_api(self, adapter_factory, config_manager):
        """设置API适配器和配置"""
        self.adapter = adapter_factory.get_protocol_adapter('http')
        self.api_config = config_manager.get_api_config()
        self.user_endpoint = self.api_config['endpoints']['user_api']
    
    def test_get_user(self):
        """测试获取用户信息"""
        user_id = 1
        response = self.adapter.get(endpoint=f"{self.user_endpoint}/users/{user_id}")
        
        assert_status_code(response, 200)
        assert_dict_keys(response.json(), ['id', 'name', 'email'])
    
    def test_create_user(self):
        """测试创建新用户"""
        user_data = DataGenerator.generate_user_data()
        
        response = self.adapter.post(
            endpoint=f"{self.user_endpoint}/users",
            json=user_data
        )
        
        assert_status_code(response, 201)
        result = response.json()
        assert result['name'] == user_data['name']
    
    def test_update_user(self):
        """测试更新用户信息"""
        user_id = 1
        update_data = {'name': 'Updated Name', 'status': 'active'}
        
        response = self.adapter.put(
            endpoint=f"{self.user_endpoint}/users/{user_id}",
            json=update_data
        )
        
        assert_status_code(response, 200)
    
    def test_delete_user(self):
        """测试删除用户"""
        user_id = 1
        
        response = self.adapter.delete(
            endpoint=f"{self.user_endpoint}/users/{user_id}"
        )
        
        assert_status_code(response, 204)
```

---

## 第六步：修改 `pyproject.toml`（如果需要新依赖）

**何时需要修改**：
- ✅ 添加WebSocket支持 → 添加 `websockets`
- ✅ 添加MongoDB支持 → 添加 `pymongo`
- ✅ 添加gRPC支持 → 添加 `grpcio`
- ✅ 其他特殊依赖

**修改示例**：

```toml
[tool.poetry.dependencies]
python = "^3.10"

# 现有依赖...

# 新增依赖（示例）
websockets = "^12.0"        # WebSocket支持
pymongo = "^4.6"           # MongoDB支持
redis = "^5.0"             # Redis支持
grpcio = "^1.60"           # gRPC支持
```

**安装新依赖**：
```bash
poetry add websockets
poetry add pymongo
poetry install
```

---

## 集成检查清单 ✅

在开始运行测试之前，请确保完成以下步骤：

- [ ] **第一步**：修改所有配置文件（dev.yaml, staging.yaml, prod.yaml）
  - [ ] API端点地址已更新
  - [ ] 数据库连接信息已配置
  - [ ] 认证凭证已设置

- [ ] **第二步**：如果需要特殊协议支持（可选）
  - [ ] 修改或添加协议适配器
  - [ ] 添加必要的依赖包

- [ ] **第三步**：如果需要特殊数据库支持（可选）
  - [ ] 修改或添加数据库适配器
  - [ ] 更新数据库配置

- [ ] **第四步**：自定义Fixtures（可选）
  - [ ] 添加项目特定的Fixture
  - [ ] 测试Fixture是否正常工作

- [ ] **第五步**：创建项目测试
  - [ ] 创建至少一个测试文件
  - [ ] 测试能否成功执行

- [ ] **第六步**：更新依赖（如需要）
  - [ ] 所有新依赖已安装
  - [ ] `poetry.lock` 已更新

---

## 验证集成 🧪

### 6.1 验证配置

```bash
# 检查配置是否可以正确加载
poetry run python -c "from core.config_manager import ConfigManager; cm = ConfigManager(); cm.load_config('dev.yaml'); print('✅ 配置加载成功')"
```

### 6.2 验证适配器

```bash
# 运行快速测试，验证适配器可以初始化
poetry run pytest tests/test_integration.py::TestHTTPAdapterIntegration::test_adapter_registration -v
```

### 6.3 验证数据库连接

```bash
# 如果修改了数据库配置，验证连接
poetry run python -c "
from core.config_manager import ConfigManager
from adapters.database_adapter import MySQLAdapter

cm = ConfigManager()
cm.load_config('dev.yaml')
db_config = cm.get_db_config('mysql')

adapter = MySQLAdapter(**db_config)
if adapter.connect():
    print('✅ 数据库连接成功')
    adapter.disconnect()
"
```

### 6.4 运行完整测试

```bash
# 执行所有测试
poetry run pytest -v

# 并行执行测试（更快）
poetry run pytest -v -n 8

# 生成覆盖率报告
poetry run pytest --cov=. --cov-report=html
```

---

## 常见问题排查 🔧

### 问题1：连接超时
**症状**：测试无法连接到API或数据库
**排查步骤**：
1. 验证 `config/dev.yaml` 中的主机地址和端口是否正确
2. 检查网络连接：`ping <host>`
3. 检查防火墙设置
4. 验证服务是否正在运行

### 问题2：认证失败
**症状**：HTTP 401 Unauthorized 错误
**排查步骤**：
1. 验证环境变量是否正确设置（AUTH_TOKEN等）
2. 检查认证令牌是否过期
3. 验证 `protocol_adapter.py` 中的认证头是否正确
4. 确认认证类型（Bearer, Basic, OAuth2等）

### 问题3：数据库连接错误
**症状**：数据库连接失败
**排查步骤**：
1. 验证数据库主机、端口、用户名密码
2. 确认数据库服务正在运行
3. 检查用户权限是否足够
4. 验证数据库存在且可访问

### 问题4：缺少依赖
**症状**：ImportError 或 ModuleNotFoundError
**排查步骤**：
```bash
# 重新安装所有依赖
poetry install

# 添加缺少的包
poetry add <package_name>

# 验证虚拟环境激活
poetry shell
```

---

## 最佳实践建议 💡

1. **配置管理**
   - ✅ 使用环境变量管理敏感信息（密码、令牌等）
   - ✅ 为每个环境（dev/staging/prod）创建单独的配置文件
   - ✅ 在版本控制中排除包含凭证的配置文件

2. **测试编写**
   - ✅ 遵循命名规范：`test_<功能名>.py`
   - ✅ 使用有意义的测试方法名：`test_get_user_success`, `test_invalid_user_id`
   - ✅ 每个测试只验证一个功能
   - ✅ 使用自定义断言函数简化代码

3. **数据管理**
   - ✅ 使用 `DataGenerator` 生成动态测试数据
   - ✅ 避免硬编码测试数据
   - ✅ 在测试后清理产生的测试数据

4. **错误处理**
   - ✅ 在适配器中添加适当的异常处理
   - ✅ 记录详细的错误日志
   - ✅ 不要忽略错误，要进行适当的恢复或重试

5. **性能优化**
   - ✅ 使用并行执行加快测试速度：`pytest -n 8`
   - ✅ 为不同类型的测试使用标记：`@pytest.mark.slow`, `@pytest.mark.integration`
   - ✅ 缓存重复的数据生成和连接

---

## 下一步 🚀

1. 按照本指南修改所需的文件
2. 运行验证命令确保集成成功
3. 编写项目特定的测试用例
4. 在CI/CD流程中集成该测试框架
5. 定期对测试和依赖进行更新和维护

**需要帮助？** 参考项目根目录的其他文档：
- [README.md](README.md) - 项目完整指南
- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
- [POETRY_SETUP.md](POETRY_SETUP.md) - Poetry环境配置详解
