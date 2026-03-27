# Project Structure & File Organization

Complete reference for all files in the test automation framework.

## 📁 Directory Tree

```
project_0318/
│
├── 📄 README.md                     # Full documentation
├── 📄 QUICKSTART.md                 # 5-minute quick start guide
├── 📄 REUSABILITY.md                # Detailed reusability guide
├── 📄 COPY_PASTE_GUIDE.md           # Copy-paste instructions (THIS FILE)
├── 📄 PROJECT_STRUCTURE.md          # This file - complete reference
│
├── 🔧 setup.sh                      # Automated setup script
├── 🔧 .gitignore                    # Git ignore rules
├── 🔧 requirements.txt              # Python dependencies (17 packages)
├── 🔧 pytest.ini                    # Pytest configuration
├── 🔧 conftest.py                   # Pytest fixtures & plugins
├── 🔧 Jenkinsfile                   # CI/CD pipeline (Jenkins)
│
├── 📂 config/                       # 🔴 MUST UPDATE
│   ├── environments.yaml            # Unified config (dev/staging/prod)
│   ├── dev.yaml                     # Dev environment (optional, legacy)
│   ├── staging.yaml                 # Staging environment (optional, legacy)
│   └── prod.yaml                    # Production environment (optional, legacy)
│
├── 📂 core/                         # Framework foundation (DO NOT MODIFY)
│   ├── __init__.py                  # Package marker
│   ├── base_test.py                 # BaseTest class with fixtures
│   ├── config_manager.py            # Configuration management (singleton)
│   └── adapter_factory.py           # Factory pattern for adapters
│
├── 📂 adapters/                     # Protocol & database adapters
│   ├── __init__.py                  # Package marker
│   ├── protocol_adapter.py          # HTTP, SOAP, GraphQL adapters
│   ├── database_adapter.py          # MySQL, Oracle, PostgreSQL adapters
│   ├── template_adapter.py          # Template for custom adapters
│   └── [custom_adapter.py]          # 🟢 ADD YOUR CUSTOM ADAPTERS HERE
│
├── 📂 tests/                        # Test suites
│   ├── __init__.py                  # Package marker
│   ├── test_unit.py                 # Unit test examples
│   ├── test_integration.py          # Integration test examples
│   ├── test_performance.py          # Performance test examples (Locust)
│   ├── test_security.py             # Security test examples
│   ├── test_example_reuse.py        # 🟢 COPY THIS FOR YOUR TESTS
│   └── [test_my_api.py]             # 🟢 ADD YOUR TEST FILES HERE
│
├── 📂 utils/                        # Helper utilities
│   ├── __init__.py                  # Package marker
│   ├── assertions.py                # Custom assertion helpers
│   ├── data_generator.py            # Test data generation
│   ├── mocking.py                   # Mocking utilities
│   └── [custom_assertions.py]       # 🟢 ADD YOUR CUSTOM ASSERTIONS HERE
│
├── 📂 reports/                      # Test reports (generated)
│   ├── html/                        # HTML reports (pytest --html)
│   ├── allure-results/              # Allure reports (pytest --alluredir)
│   └── junit.xml                    # JUnit XML (pytest --junit-xml)
│
└── 📂 .git/                         # Git repository
    └── [git files]
```

---

## 📋 File Details

### Root Configuration Files

| File | Purpose | Modify? |
|------|---------|---------|
| `setup.sh` | Automated setup script | ❌ Keep as-is |
| `.gitignore` | Git ignore rules (excludes .env, venv) | ⚠️ Add your ignores |
| `requirements.txt` | Python dependencies | ⚠️ Add new packages if needed |
| `pytest.ini` | Pytest settings (markers, plugins) | ⚠️ Customize markers |
| `conftest.py` | Pytest fixtures & setup | ✅ Register adapters here |
| `Jenkinsfile` | Jenkins CI/CD pipeline | ⚠️ Modify for your CI/CD |

### Configuration (config/)

| File | Purpose | Modify? |
|------|---------|---------|
| `environments.yaml` | **Unified config (dev/staging/prod)** | 🔴 **MUST UPDATE** |
| `dev.yaml` | Legacy dev config | ⚠️ Optional |
| `staging.yaml` | Legacy staging config | ⚠️ Optional |
| `prod.yaml` | Legacy prod config | ⚠️ Optional |

**⚠️ Use `environments.yaml` - it's the modern approach!**

### Core Framework (core/)

| File | Class/Function | Purpose |
|------|----------------|---------|
| `base_test.py` | `BaseTest` | Base class for all tests with setup/teardown |
| `config_manager.py` | `ConfigManager` | Singleton for config management |
| `adapter_factory.py` | `AdapterFactory` | Factory for creating adapters |

**Note:** Do NOT modify core files - they're the framework foundation.

### Adapters (adapters/)

| File | Class | Purpose | Status |
|------|-------|---------|--------|
| `protocol_adapter.py` | `HTTPAdapter` | REST API testing | ✅ Ready |
| `protocol_adapter.py` | `SOAPAdapter` | SOAP web services | ✅ Ready |
| `protocol_adapter.py` | `GraphQLAdapter` | GraphQL API testing | ✅ Ready |
| `database_adapter.py` | `MySQLAdapter` | MySQL database | ✅ Ready |
| `database_adapter.py` | `OracleAdapter` | Oracle database | ✅ Ready |
| `database_adapter.py` | `PostgreSQLAdapter` | PostgreSQL database | ✅ Ready |
| `template_adapter.py` | `[Template Classes]` | Custom adapter examples | 📚 Reference |
| `[custom].py` | `[Custom]` | Your adapters | 🟢 ADD HERE |

### Tests (tests/)

| File | Classes | Purpose |
|------|---------|---------|
| `test_unit.py` | `TestDataGenerator`, `TestAssertions` | Unit test examples |
| `test_integration.py` | `TestHTTPAdapterIntegration`, `TestAdapterFactory` | Integration examples |
| `test_performance.py` | `APILoadTest`, `TestPerformanceMetrics` | Performance test (Locust) |
| `test_security.py` | `TestSecurity` | Security test examples |
| `test_example_reuse.py` | `TestExampleAPI`, `TestAPIWithDatabase` | 🔥 **COPY THIS FILE** |
| `[test_my_api].py` | `[Your classes]` | 🟢 **ADD YOUR TESTS** |

### Utilities (utils/)

| File | Classes/Functions | Purpose |
|------|-------------------|---------|
| `assertions.py` | `assert_*` functions | Common assertions (20+) |
| `data_generator.py` | `DataGenerator`, `MockDataProvider` | Test data generation |
| `mocking.py` | `ResponseMocker`, `RequestMocker` | Mocking utilities |
| `[custom].py` | Your functions | 🟢 **ADD YOUR UTILITIES** |

### Documentation Files

| File | Purpose | Audience |
|------|---------|----------|
| `README.md` | Complete documentation | Everyone |
| `QUICKSTART.md` | 5-minute quick start | New users |
| `REUSABILITY.md` | Step-by-step reuse guide | Users copying framework |
| `COPY_PASTE_GUIDE.md` | Copy-paste instructions | Copy-paste users |
| `PROJECT_STRUCTURE.md` | This file | Reference |

---

## 🎯 How to Use This Structure

### For Initial Setup

1. **Update config:**
   ```bash
   vim config/environments.yaml  # Add your system details
   ```

2. **Install:**
   ```bash
   ./setup.sh
   ```

3. **Verify:**
   ```bash
   pytest tests/test_unit.py  # Should pass
   ```

### For Adding Your Tests

1. **Copy example:**
   ```bash
   cp tests/test_example_reuse.py tests/test_my_api.py
   ```

2. **Modify test file:**
   - Update class names
   - Change endpoints
   - Add your assertions

3. **Register adapters (if needed):**
   - Add to `conftest.py`:
   ```python
   from adapters.my_adapter import MyAdapter
   AdapterFactory.register_protocol_adapter("mine", MyAdapter)
   ```

4. **Run tests:**
   ```bash
   pytest tests/test_my_api.py -v
   ```

### For Custom Adapters

1. **Create adapter:**
   ```bash
   cp adapters/template_adapter.py adapters/my_adapter.py
   ```

2. **Implement:**
   - Follow the template
   - Inherit from base class
   - Implement required methods

3. **Register (in conftest.py):**
   ```python
   from adapters.my_adapter import MyAdapter
   AdapterFactory.register_protocol_adapter("myproto", MyAdapter)
   ```

4. **Use in tests:**
   ```python
   adapter = AdapterFactory.get_protocol_adapter("myproto", ...)
   ```

### For Custom Utilities

1. **Create file:**
   ```bash
   touch utils/my_assertions.py
   ```

2. **Add functions:**
   ```python
   def assert_my_thing(data):
       assert data is not None
   ```

3. **Import in tests:**
   ```python
   from utils.my_assertions import assert_my_thing
   ```

---

## 🔴 MUST DO BEFORE RUNNING TESTS

### 1. Update Configuration
Edit `config/environments.yaml`:
```yaml
environments:
  dev:
    databases:
      mysql:
        host: YOUR-MYSQL-HOST      ← Change
        user: YOUR-MYSQL-USER      ← Change
        password: YOUR-MYSQL-PASS  ← Change
        database: YOUR-DB-NAME     ← Change
    
    apis:
      http:
        base_url: YOUR-API-URL     ← Change
```

### 2. Set Environment Variables (for sensitive data)
```bash
export DB_PASSWORD="your-password"
export API_TOKEN="your-token"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
# or
./setup.sh
```

---

## 🟢 OPTIONAL CUSTOMIZATIONS

### Add These as Needed

```
✅ tests/test_my_api.py          - Your test files
✅ adapters/my_adapter.py        - Custom adapters
✅ utils/my_assertions.py        - Custom assertions
✅ utils/my_data.py              - Custom data generators
✅ conftest.py additions         - New fixtures
```

---

## 🚫 DO NOT MODIFY

```
❌ core/                         - Framework foundation
❌ adapters/protocol_adapter.py  - Unless extending
❌ adapters/database_adapter.py  - Unless extending
❌ utils/assertions.py           - Extend instead
❌ utils/data_generator.py       - Extend instead
❌ utils/mocking.py              - Build on top
❌ pytest.ini                    - Unless customizing
```

---

## 📊 Dependency Overview

### Core Dependencies (17 total)

```
Testing Framework:
- pytest 7.4.3          # Test runner
- pytest-xdist 3.5.0    # Parallel execution
- pytest-cov 4.1.0      # Coverage reports
- pytest-timeout 2.2.0  # Test timeout control

Protocols:
- requests 2.31.0       # HTTP client
- zeep 4.2.1           # SOAP client

Databases:
- mysql-connector-python 8.2.0  # MySQL
- oracledb 1.4.0                # Oracle
- psycopg2-binary 2.9.9         # PostgreSQL

Configuration:
- pyyaml 6.0.1          # YAML parsing

Performance:
- locust 2.18.0         # Load testing

Reporting:
- allure-pytest 2.13.2  # Allure reports
```

---

## 🔄 Configuration Priority

The framework resolves configuration in this order:

1. **Primary:** `config/environments.yaml` (unified, recommended)
2. **Fallback:** `config/{env}.yaml` (legacy, individual files)
3. **Default:** Built-in defaults if file not found
4. **Substitution:** Environment variables (`${VAR}` → `$VAR`)

**Best practice:** Use `environments.yaml` for everything.

---

## 🧪 Test Execution Flow

```
1. pytest discovers tests in tests/ directory
2. conftest.py runs (sets up fixtures, registers adapters)
3. ConfigManager loads config/environments.yaml
4. Each test class inherits from BaseTest
5. setup_method() runs before each test
6. Test method executes
7. teardown_method() runs after each test
8. Reports generated in reports/
```

---

## 📈 Scaling Your Test Suite

As your test suite grows:

```
tests/
├── test_unit.py                 # Unit tests
├── test_integration.py          # Integration tests
├── test_performance.py          # Performance/Load tests
├── test_security.py             # Security tests
├── api/                         # Your API tests
│   ├── test_users_api.py
│   ├── test_products_api.py
│   └── test_orders_api.py
├── database/                    # Your DB tests
│   ├── test_user_queries.py
│   └── test_data_integrity.py
└── workflows/                   # Multi-step workflows
    ├── test_checkout_flow.py
    └── test_subscription_flow.py

adapters/                        # Your custom adapters
├── grpc_adapter.py
├── websocket_adapter.py
└── custom_cache_adapter.py

utils/                           # Your custom utilities
├── domain_assertions.py
├── business_data_generators.py
└── custom_mocking.py
```

---

## ⚡ Quick Command Reference

```bash
# Setup & install
./setup.sh
pip install -r requirements.txt

# Run tests
pytest                              # All tests
pytest tests/test_my_api.py        # Specific file
pytest -v tests/                   # Verbose
pytest -n auto tests/              # Parallel
pytest -m integration tests/        # By marker
pytest -x tests/                   # Stop on failure

# Development
pytest --lf                        # Last failed
pytest -s tests/                   # Show output
pytest --pdb tests/                # Debugger

# Reports
pytest --html=reports/report.html
pytest --alluredir=reports/allure
allure serve reports/allure

# Coverage
pytest --cov=. --cov-report=html   # Generate coverage
pytest --cov=. --cov-report=term   # Terminal output
```

---

## ✅ Setup Verification Checklist

- [ ] Cloned/copied framework
- [ ] Updated `config/environments.yaml`
- [ ] Created virtual environment
- [ ] Installed dependencies: `pip install -r requirements.txt`
- [ ] Ran `pytest tests/test_unit.py` - all pass?
- [ ] Ran `pytest tests/test_integration.py` - all pass?
- [ ] Copied `tests/test_example_reuse.py` to `tests/test_my_api.py`
- [ ] Modified test with your endpoints
- [ ] Ran your tests: `pytest tests/test_my_api.py`
- [ ] Generated report: `pytest --html=reports/report.html`
- [ ] Viewed report in browser

✅ **All checked? You're ready to go!**

---

**Next Steps:**
1. Read `QUICKSTART.md` (5 min)
2. Run `./setup.sh` (2 min)
3. Modify `test_example_reuse.py` (10 min)
4. Run your first test (2 min)

**Total: ~20 minutes to first passing test!**
