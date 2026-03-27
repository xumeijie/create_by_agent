# Test Automation Framework - Complete Copy-Paste Reusability Guide

## 🎯 Framework Designed for Copy-Paste Reuse

This framework is **specifically designed to be copied and reused** across different projects with minimal changes. Follow these simple steps:

---

## 🚀 3-Minute Quick Start

### 1️⃣ Copy the Framework
```bash
cp -r test-automation-framework your-project/automation
cd your-project/automation
```

### 2️⃣ Update Configuration (Only Required Step!)
**File:** `config/environments.yaml`

Change these lines with your system details:
```yaml
your_instance:
  dev:
    databases:
      mysql:
        host: YOUR-HOST        # ← Your DB host
        user: YOUR-USER        # ← Your DB user
        password: YOUR-PASS    # ← Your DB password
        database: YOUR-DB      # ← Your DB name
    
    apis:
      http:
        base_url: YOUR-API-URL # ← Your API URL
```

### 3️⃣ Install & Test
```bash
./setup.sh                    # Automated setup
# or
pip install -r requirements.txt

pytest tests/                 # Run example tests
```

✅ **Done!** Framework is now configured for your system.

---

## 📋 What Changes vs What Stays the Same

### Don't Touch (Use As-Is)
```
✅ core/                  - Base framework classes
✅ adapters/              - Ready-to-use adapters  
✅ utils/                 - Helper utilities
✅ conftest.py            - Test configuration
✅ pytest.ini             - Pytest settings
✅ README.md              - Full documentation
✅ requirements.txt       - All dependencies
```

### Must Update
```
📝 config/environments.yaml - Update with YOUR system details
```

### Create Your Own
```
📝 tests/test_my_api.py         - Your test files
📝 adapters/my_adapter.py       - Custom adapters (if needed)
📝 utils/my_assertions.py       - Custom assertions (if needed)
```

---

## 🔧 Real-World Example: Testing Your REST API

### Step 1: Update Configuration
`config/environments.yaml`:
```yaml
environments:
  dev:
    apis:
      http:
        base_url: https://api.mycompany.com  # Your API URL
```

### Step 2: Create Your Test
`tests/test_my_api.py`:
```python
from core.base_test import BaseTest
from core.adapter_factory import AdapterFactory
from utils.assertions import assert_status_code

class TestMyAPI(BaseTest):
    def setup_method(self):
        self.api = AdapterFactory.get_protocol_adapter(
            "http",
            base_url="https://api.mycompany.com"
        )
    
    def test_get_users(self):
        """My first test!"""
        response = self.api.send_request("GET", "/api/users")
        assert_status_code(response, 200)
```

### Step 3: Run
```bash
pytest tests/test_my_api.py
```

✅ **That's it!** Your tests are running.

---

## 🎨 Common Customizations

### Adding Your Own Adapter

1. **Create:** `adapters/my_adapter.py`
2. **Implement:** Following the pattern in `adapters/template_adapter.py`
3. **Register:** In `conftest.py`:
   ```python
   from adapters.my_adapter import MyAdapter
   AdapterFactory.register_protocol_adapter("myprotocol", MyAdapter)
   ```
4. **Use:** In your tests
   ```python
   adapter = AdapterFactory.get_protocol_adapter("myprotocol", ...)
   ```

### Adding Custom Assertions

1. **Create:** `utils/my_assertions.py`
2. **Define:** Your assertion functions
3. **Use:** In your tests
   ```python
   from utils.my_assertions import my_assertion
   my_assertion(data)
   ```

### Adding Domain-Specific Data Generators

1. **Create:** `utils/my_data.py`
2. **Extend:** `DataGenerator` class
3. **Use:** In your tests
   ```python
   from utils.my_data import MyDataGenerator
   data = MyDataGenerator.generate_my_object()
   ```

---

## 📊 Project Structure & Organization

```
your-project/
├── automation/
│   ├── config/
│   │   └── environments.yaml        ← UPDATE WITH YOUR CONFIG
│   ├── adapters/
│   │   ├── (originals)
│   │   └── my_adapter.py            ← ADD YOUR ADAPTERS
│   ├── tests/
│   │   ├── (examples)
│   │   └── test_my_api.py           ← ADD YOUR TESTS
│   ├── utils/
│   │   ├── (originals)
│   │   └── my_assertions.py         ← ADD YOUR UTILITIES
│   ├── core/                        ← KEEP
│   ├── reports/                     ← KEEP
│   ├── conftest.py                  ← EXTEND WITH YOUR ADAPTERS
│   ├── pytest.ini                   ← KEEP
│   ├── requirements.txt             ← KEEP
│   ├── setup.sh                     ← KEEP
│   ├── README.md                    ← REFERENCE
│   ├── QUICKSTART.md                ← REFERENCE
│   ├── REUSABILITY.md               ← THIS FILE
│   ├── .gitignore                   ← KEEP
│   └── Jenkinsfile                  ← OPTIONAL
```

---

## 🔐 Handling Sensitive Data

### Never Commit Passwords!

Use environment variables:

```bash
# Set before running tests
export DB_PASSWORD="your-password"
export API_TOKEN="your-token"

pytest tests/
```

Or use `.env` file (add to `.gitignore`!):

```bash
# .env (DON'T COMMIT!)
DB_PASSWORD=your-password
API_TOKEN=your-token

# Load in conftest.py
from dotenv import load_dotenv
load_dotenv()
```

**Always add to `.gitignore`:**
```
.env
.env.local
```

---

## ✨ Key Features You Get Immediately

| Feature | How to Use |
|---------|-----------|
| **Multi-Protocol** | HTTP, SOAP, GraphQL adapters ready to go |
| **Database Support** | MySQL, Oracle, PostgreSQL adapters included |
| **Custom Adapters** | Easy to extend (follow `template_adapter.py`) |
| **Test Data** | `DataGenerator` for random/mock data |
| **Assertions** | Pre-built helpers for common assertions |
| **Mocking** | Built-in mocking utilities |
| **Reports** | HTML and Allure reporting |
| **Parallel Tests** | Run tests faster with `-n auto` |
| **CI/CD Ready** | Jenkins pipeline included |
| **Configuration** | Environment-based config with env vars |

---

## 📚 File Reference

### Where to Look for What

| Need | See File |
|------|----------|
| Quick start | `QUICKSTART.md` |
| Full docs | `README.md` |
| Reusability | `REUSABILITY.md` (this file) |
| Examples | `tests/test_example_reuse.py` |
| Adapter template | `adapters/template_adapter.py` |
| Configuration | `config/environments.yaml` |
| Code examples | Individual Python files have docstrings |

---

## 🧪 Running Your Tests

```bash
# All tests
pytest

# Specific test file
pytest tests/test_my_api.py

# Specific test class/method
pytest tests/test_my_api.py::TestMyAPI::test_get_users

# With markers
pytest -m integration      # Run only integration tests
pytest -m unit            # Run only unit tests

# Parallel execution (faster!)
pytest -n auto

# With coverage
pytest --cov=. --cov-report=html

# With Allure reports
pytest --alluredir=reports/allure
allure serve reports/allure
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `pytest not found` | `pip install -r requirements.txt` |
| `Connection refused` | Check `config/environments.yaml` host/port |
| `Module not found` | Verify virtual environment: `source .venv/bin/activate` |
| `YAML error` | Ensure spaces (not tabs) in `config/environments.yaml` |
| `${VAR} not replaced` | Set env var first: `export VAR="value"` |
| Tests pass locally but fail in CI | Check CI environment variables set correctly |

---

## ✅ Reusability Checklist

Before using the framework:

- [ ] Copied framework to project
- [ ] Updated `config/environments.yaml` with your system
- [ ] Ran `./setup.sh` or `pip install -r requirements.txt`
- [ ] Ran `pytest tests/test_example_reuse.py` - all pass?
- [ ] Created your own test file (copy from example)
- [ ] Updated your test with your API endpoints
- [ ] Successfully ran your tests
- [ ] Set up environment variables for sensitive data
- [ ] Ready for CI/CD pipeline

---

## 🚀 Pro Tips for Maximum Reusability

1. **Keep core framework unchanged** - Updates easier
2. **Update `environments.yaml` first** - Single source of truth
3. **Use environment variables** - For secrets/sensible data
4. **Follow adapter patterns** - Custom adapters are consistent
5. **Inherit from `BaseTest`** - Automatic setup/teardown
6. **Use `ConfigManager`** - Centralized config access
7. **Create fixtures in `conftest.py`** - Reusable across tests
8. **Use markers (`@pytest.mark`)** - Categorize tests
9. **Test one thing per test** - Easier to maintain
10. **Document your adapters** - Help future you and teammates

---

## 🎓 Learning Path

1. **Start:** Read `QUICKSTART.md` (5 minutes)
2. **Setup:** Run `./setup.sh` (2 minutes)
3. **Examine:** Look at `tests/test_example_reuse.py` (10 minutes)
4. **Create:** Make your first test (15 minutes)
5. **Extend:** Add custom adapter if needed (30 minutes)
6. **Run:** Execute full test suite (5 minutes)
7. **Report:** View test reports (5 minutes)
8. **Deploy:** Setup CI/CD pipeline (optional, varies)

**Total time to working test suite: ~1 hour**

---

## 📞 Quick Reference Commands

```bash
# Setup
pip install -r requirements.txt
./setup.sh

# Development
pytest                          # Run all tests
pytest -v tests/               # Verbose output
pytest -n auto tests/          # Parallel execution
pytest --lf                    # Last failed tests
pytest -s tests/               # Show print statements

# Reporting
pytest --html=reports/report.html
pytest --alluredir=reports/allure
allure serve reports/allure

# Debugging
pytest -x tests/               # Stop on first failure
pytest --pdb tests/            # Drop into debugger
pytest -vv tests/              # Very verbose

# CI/CD
pytest --junit-xml=reports/junit.xml
pytest --cov=. --cov-report=xml
```

---

## 🎯 Final Thoughts

This framework is built with **maximum reusability** in mind:

✅ **Copy & Use** - No complex setup required  
✅ **Minimal Changes** - Only update config file  
✅ **Extensible** - Easy to add custom adapters  
✅ **Well-Documented** - Every component explained  
✅ **Production-Ready** - Enterprise test patterns  
✅ **Community-Friendly** - Clear examples and guides  

**You can have a working test suite in under 30 minutes!**

---

**Next Step:** Read `QUICKSTART.md` and run `./setup.sh` 🚀
