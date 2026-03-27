# Quick Start Guide - Test Automation Framework

Get up and running in 5 minutes!

## Step 1: Copy Framework to Your Project

```bash
# Clone or copy the entire framework to your project
cp -r test-automation-framework your-project/automation
cd your-project/automation
```

## Step 2: Update Configuration

Edit `config/environments.yaml` with your system details:

```yaml
environments:
  dev:
    apis:
      http:
        base_url: https://your-api.example.com  # ← Change this
        timeout: 30
    
    databases:
      mysql:
        host: your-mysql-host              # ← Change this
        port: 3306
        user: your-user
        password: your-password
        database: your-database
```

**Tip:** Use environment variables for sensitive data:
```yaml
password: ${DB_PASSWORD}  # Will use DB_PASSWORD env var
```

## Step 3: Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Step 4: Create Your First Test

Create `tests/test_my_api.py`:

```python
from core.base_test import BaseTest
from core.adapter_factory import AdapterFactory
from utils.assertions import assert_status_code

class TestMyAPI(BaseTest):
    """Test my API endpoints."""
    
    def setup_method(self):
        """Setup before each test."""
        self.adapter = AdapterFactory.get_protocol_adapter(
            "http",
            base_url="https://your-api.example.com"
        )
    
    def test_get_users(self):
        """Test getting users list."""
        response = self.adapter.send_request("GET", "/api/users")
        assert_status_code(response, 200)
```

## Step 5: Run Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_my_api.py::TestMyAPI::test_get_users

# Run with specific environment
pytest tests/ -m dev

# Run in parallel
pytest -n auto
```

## Step 6: View Reports

```bash
# HTML Report
open reports/html/*.html

# Or with Allure
pip install allure-commandline
pytest --alluredir=reports/allure
allure serve reports/allure
```

---

## Common Customizations

### 1. Add a New Database Adapter

Create `adapters/custom_db_adapter.py`:

```python
from adapters.database_adapter import DatabaseAdapter

class RedisAdapter(DatabaseAdapter):
    """Custom Redis adapter."""
    
    def connect(self):
        import redis
        self.connection = redis.Redis(
            host=self.host,
            port=self.port,
            decode_responses=True
        )
    
    def disconnect(self):
        self.connection.close()
    
    def execute_query(self, query):
        return self.connection.get(query)
    
    def execute_update(self, query):
        return True
```

Register in `conftest.py`:

```python
from adapters.custom_db_adapter import RedisAdapter

AdapterFactory.register_database_adapter("redis", RedisAdapter)
```

### 2. Add a New Protocol Adapter

Create `adapters/custom_protocol_adapter.py`:

```python
from adapters.protocol_adapter import ProtocolAdapter

class WebSocketAdapter(ProtocolAdapter):
    """WebSocket protocol adapter."""
    
    def __init__(self, url: str, timeout: int = 30):
        super().__init__(timeout)
        self.url = url
    
    def send_request(self, **kwargs):
        return {"status": 200, "body": {}}
```

Register in `conftest.py`:

```python
from adapters.custom_protocol_adapter import WebSocketAdapter

AdapterFactory.register_protocol_adapter("websocket", WebSocketAdapter)
```

### 3. Custom Test Data Generation

Create `utils/custom_data.py`:

```python
from utils.data_generator import DataGenerator

class CustomDataGenerator(DataGenerator):
    """Extended data generator."""
    
    @staticmethod
    def generate_order_data():
        return {
            "order_id": DataGenerator.random_string(8).upper(),
            "items": []
        }
```

### 4. Custom Assertions

Create `utils/custom_assertions.py`:

```python
def assert_order_valid(order):
    """Assert order structure."""
    assert "order_id" in order
    assert "items" in order
```

---

## Project Structure After Customization

```
your-project/
├── automation/
│   ├── config/
│   │   └── environments.yaml        ← Update with your config
│   ├── adapters/
│   │   ├── protocol_adapter.py      (keep)
│   │   ├── database_adapter.py      (keep)
│   │   └── custom_db_adapter.py     ← Add custom adapters
│   ├── tests/
│   │   ├── test_my_api.py           ← Add your tests
│   │   └── test_my_features.py      ← Add more tests
│   ├── utils/
│   │   ├── assertions.py            (keep)
│   │   ├── custom_data.py           ← Custom generators
│   │   └── custom_assertions.py     ← Custom assertions
│   ├── core/                        (keep as-is)
│   ├── reports/                     (keep as-is)
│   ├── conftest.py                  ← Register custom adapters
│   ├── pytest.ini                   (keep)
│   └── requirements.txt             (keep)
```

---

## Environment Variable Setup

For sensitive data, use environment variables:

```bash
# .env (don't commit to git!)
export DB_PASSWORD="your-secret-password"
export API_TOKEN="your-api-token"
```

Load before running tests:

```bash
source .env
pytest tests/
```

Or install `python-dotenv`:

```bash
pip install python-dotenv
```

Create `.env`:
```
DB_PASSWORD=your-secret-password
API_TOKEN=your-api-token
```

In `conftest.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Next Steps

1. **Read full documentation** - See [README.md](README.md)
2. **Explore examples** - Check `tests/test_*.py`
3. **Customize adapters** - Add domain-specific adapters
4. **Extend utilities** - Use `adapters/template_adapter.py`
5. **Setup CI/CD** - Modify `Jenkinsfile`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `Connection refused` | Update `config/environments.yaml` |
| `ImportError on adapter` | Register in `conftest.py` |
| `pytest not found` | Activate venv: `source .venv/bin/activate` |

---

## Tips for Reusability

✅ **Update `config/environments.yaml`** before using  
✅ **Create custom adapters** following patterns  
✅ **Use ConfigManager** for all config  
✅ **Inherit from BaseTest** for consistency  
✅ **Keep adapters generic**  
✅ **Use mocking** for external deps  
✅ **Add fixtures** in `conftest.py`  

---

Happy testing! 🚀
