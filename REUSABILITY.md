# REUSABILITY GUIDE
# How to Copy-Paste This Framework to a New Project

## 📋 Step-by-Step Reuse Process

### 1. **Copy Framework Files**
```bash
# Copy entire framework to your project
cp -r test-automation-framework your-project/automation

cd your-project/automation

# Or initialize git
git init
```

### 2. **Update Core Configuration (5 minutes)**

The **only file you MUST change** to reuse this framework:

**File:** `config/environments.yaml`

```yaml
environments:
  dev:
    name: Development
    
    databases:
      mysql:
        host: YOUR-HOST        # ← Change here
        port: 3306
        user: YOUR-USER        # ← Change here
        password: YOUR-PASSWORD # ← Change here
        database: YOUR-DB      # ← Change here
    
    apis:
      http:
        base_url: YOUR-API-URL # ← Change here
        timeout: 30
```

**Use environment variables for sensitive data:**
```yaml
password: ${DB_PASSWORD}  # Reads from DB_PASSWORD env var
```

Set before running tests:
```bash
export DB_PASSWORD="your-secret-password"
pytest tests/
```

### 3. **Install & Verify**
```bash
# Option A: Manual setup
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Option B: Use setup script
chmod +x setup.sh
./setup.sh
```

### 4. **Create Tests for Your API**

**File:** `tests/test_your_api.py`

```python
from core.base_test import BaseTest
from core.adapter_factory import AdapterFactory
from utils.assertions import assert_status_code, assert_dict_keys
from utils.data_generator import DataGenerator

class TestUserAPI(BaseTest):
    """Test user management API."""
    
    def setup_method(self):
        """Setup - called before each test."""
        self.adapter = AdapterFactory.get_protocol_adapter(
            "http",
            base_url="https://api.example.com"
        )
    
    def test_get_all_users(self):
        """Test: GET /users should return 200 with user list."""
        response = self.adapter.send_request("GET", "/users")
        assert_status_code(response, 200)
        
        body = response.get("body", {})
        assert "users" in body
    
    def test_create_user(self):
        """Test: POST /users should create new user."""
        user_data = DataGenerator.generate_user_data()
        
        response = self.adapter.send_request(
            "POST", 
            "/users",
            data=user_data
        )
        assert_status_code(response, 201)
```

### 5. **Run Tests**

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_your_api.py

# Run with verbose output
pytest -v

# Run in parallel (faster!)
pytest -n auto

# Run with coverage
pytest --cov=. --cov-report=html
```

### 6. **View Test Results**

```bash
# HTML Report
open reports/html/*.html

# Or with Allure (install first)
pip install allure-commandline
pytest --alluredir=reports/allure
allure serve reports/allure
```

---

## 🎨 Customization Examples

### Add Custom Database Adapter

**File:** `adapters/redis_adapter.py`

```python
from adapters.database_adapter import DatabaseAdapter

class RedisAdapter(DatabaseAdapter):
    """Redis cache adapter."""
    
    def connect(self):
        import redis
        self.connection = redis.Redis(
            host=self.host,
            port=self.port,
            decode_responses=True
        )
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query):
        return self.connection.get(query)
    
    def execute_update(self, query):
        return True
```

**Register in `conftest.py`:**

```python
from adapters.redis_adapter import RedisAdapter

AdapterFactory.register_database_adapter("redis", RedisAdapter)
```

**Use in tests:**

```python
def test_cache_hit(self):
    """Test Redis cache."""
    redis = AdapterFactory.get_database_adapter(
        "redis",
        host="localhost",
        port=6379,
        user="default",
        password="",
        database="0"
    )
    redis.connect()
    value = redis.execute_query("user:123")
    redis.disconnect()
```

### Add Custom Assertions

**File:** `utils/custom_assertions.py`

```python
def assert_user_valid(user):
    """Assert user object is valid."""
    from utils.assertions import assert_dict_keys
    
    required_keys = ["id", "name", "email"]
    assert_dict_keys(user, required_keys)
    
    assert len(user["name"]) > 0, "Name cannot be empty"
    assert "@" in user["email"], "Invalid email format"

def assert_error_response(response, expected_code):
    """Assert error response structure."""
    body = response.get("body", {})
    assert body.get("error_code") == expected_code
    assert "message" in body
```

### Add Custom Test Data

**File:** `utils/domain_data.py`

```python
from utils.data_generator import DataGenerator

class OrderDataGenerator:
    """Generate order test data."""
    
    @staticmethod
    def generate_order():
        return {
            "order_id": DataGenerator.random_string(8).upper(),
            "customer_email": DataGenerator.random_email(),
            "items": [
                {
                    "sku": DataGenerator.random_string(5).upper(),
                    "qty": DataGenerator.random_number(1, 10),
                    "price": DataGenerator.random_number(10, 1000)
                }
            ],
            "total": DataGenerator.random_number(100, 50000)
        }
```

---

## 📁 What to Keep vs Modify

### Keep As-Is (Don't Change)
```
✅ core/              - Base classes (well designed)
✅ adapters/          - Adapters (copy as template for custom)
✅ utils/             - Helpers (extend, don't modify)
✅ conftest.py        - Pytest config (add new fixtures)
✅ pytest.ini         - Test settings (optional tweaks)
✅ Jenkinsfile        - CI/CD (if using Jenkins)
✅ README.md          - Documentation
✅ requirements.txt   - Dependencies
```

### Modify for Your Project
```
📝 config/environments.yaml      - MUST update with your config
📝 tests/                        - Add your own test files
📝 adapters/                     - Add custom adapters
📝 utils/                        - Add custom generators/assertions
```

---

## 🚀 Typical Project Structure After Reuse

```
your-project/
├── automation/
│   ├── config/
│   │   └── environments.yaml          ✅ UPDATED
│   ├── adapters/
│   │   ├── protocol_adapter.py        (original)
│   │   ├── database_adapter.py        (original)
│   │   ├── template_adapter.py        (reference)
│   │   └── your_custom_adapter.py     ✅ ADDED
│   ├── tests/
│   │   ├── test_unit.py               (original examples)
│   │   ├── test_integration.py        (original examples)
│   │   ├── test_your_api.py           ✅ ADDED
│   │   └── test_your_features.py      ✅ ADDED
│   ├── utils/
│   │   ├── assertions.py              (original)
│   │   ├── data_generator.py          (original)
│   │   ├── mocking.py                 (original)
│   │   ├── domain_data.py             ✅ ADDED
│   │   └── custom_assertions.py       ✅ ADDED
│   ├── core/                          (original)
│   ├── reports/                       (original)
│   ├── conftest.py                    ✅ EXTENDED
│   ├── pytest.ini                     (original)
│   ├── requirements.txt               (original)
│   ├── README.md                      (original)
│   ├── QUICKSTART.md                  (reference)
│   ├── REUSABILITY.md                 (this file)
│   ├── Jenkinsfile                    (optional)
│   ├── setup.sh                       (automation)
│   └── .gitignore                     ✅ CREATED
```

---

## 🔧 Environment Variables Quick Reference

### Common Variables to Set

```bash
# Database credentials
export DB_PASSWORD="your-database-password"
export ORACLE_PASSWORD="oracle-password"
export PG_PASSWORD="postgres-password"

# API tokens
export API_TOKEN="your-api-token"
export JWT_TOKEN="your-jwt-token"

# Endpoints (optional - if not in config)
export API_ENDPOINT="https://api.example.com"

# Test environment
export TEST_ENV="dev"  # or "staging", "prod"

# CI/CD variables
export CI_BUILD_ID="12345"
export CI_JOB_NAME="test-suite"
```

### Load from .env file

**Create `.env` file:**
```bash
DB_PASSWORD=your-password
API_TOKEN=your-token
```

**Add to `conftest.py`:**
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env
```

**Add to `.gitignore`:**
```bash
.env
.env.local
```

---

## ✅ Reusability Checklist

- [ ] Copied framework to project
- [ ] Updated `config/environments.yaml`
- [ ] Ran `./setup.sh` or manual setup
- [ ] Created first test file
- [ ] Successfully ran `pytest`
- [ ] Viewed test report
- [ ] Created custom adapter (if needed)
- [ ] Added custom assertions (if needed)
- [ ] Set up environment variables
- [ ] Configured for CI/CD (if using)

---

## 📚 Best Practices

1. **Always update config first** before running any tests
2. **Use ConfigManager** for all config access
3. **Inherit from BaseTest** for consistency
4. **Create adapters following existing patterns**
5. **Keep business logic separate from adapters**
6. **Use mocking for external dependencies**
7. **Commit `.gitignore` and avoid committing `.env`**
8. **Document custom adapters and assertions**
9. **Test your adapters before using in suites**
10. **Keep fixture files organized in conftest.py**

---

## 🆘 Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `Connection refused` | Check host/port in `config/environments.yaml` |
| `pytest not found` | Activate venv: `source .venv/bin/activate` |
| `ImportError on custom adapter` | Register in `conftest.py` |
| `${VAR} not replaced` | Set env var: `export VAR="value"` |
| `Permission denied setup.sh` | `chmod +x setup.sh` |
| `YAML parse error` | Check YAML syntax (indent with spaces, not tabs) |

---

## 💡 Pro Tips

- **Use `-n auto` flag** - Runs tests in parallel for speed
- **Use `--alluredir`** - Better reports than plain HTML
- **Use markers** - `@pytest.mark.integration` for categorization
- **Use fixtures** - Create reusable test components
- **Use conftest.py** - Central place for shared fixtures
- **Use parametrize** - Test multiple scenarios with one function
- **Use mocking** - Isolate code under test from dependencies

---

Happy testing! 🎉

For questions, refer to:
- `README.md` - Full documentation
- `QUICKSTART.md` - Quick reference
- `adapters/template_adapter.py` - Custom adapter examples
- Individual file docstrings - Code documentation
