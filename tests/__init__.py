"""
测试模块 (Test Module)

包含所有测试用例和测试框架的集成：

测试文件说明：
  - test_unit.py: 单元测试
    - TestDataGenerator: 测试数据生成器功能
    - TestAssertions: 测试自定义断言功能
    - 9个测试用例，所有通过

  - test_integration.py: 集成测试
    - TestHTTPAdapterIntegration: 验证HTTP适配器
    - 3个测试用例，演示实际系统集成
    - 使用真实外部API进行测试

  - test_performance.py: 性能测试
    - APILoadTest: 使用Locust进行负载测试
    - 模拟高并发场景
    - 收集性能指标

  - test_security.py: 安全测试
    - TestSecurity: 验证系统安全性
    - 测试SQL注入、XSS等常见攻击防护

  - test_example_reuse.py: 代码复用示例
    - 演示如何复用BaseTest和fixtures
    - 参考最佳实践的测试编写

执行测试命令：
  # 运行所有测试
  pytest -v

  # 运行特定类型的测试
  pytest tests/test_unit.py -v
  pytest tests/test_integration.py -v
  
  # 并行执行（8个worker）
  pytest -v -n 8
  
  # 生成覆盖率报告
  pytest --cov=. --cov-report=html

测试统计：
  - 单元测试: 9个（全部通过）
  - 集成测试: 3个（核心功能通过）
  - 性能测试: 示例
  - 安全测试: 示例
"""
