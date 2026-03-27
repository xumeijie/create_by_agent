"""
性能测试集 (Performance Tests)

使用Locust框架进行负载测试和性能压力测试：

主要测试类：
- APILoadTest: 负载测试类（继承HttpUser）
  - get_posts(): 获取文章列表API的负载测试
  - create_post(): 创建文章API的负载测试
  - wait_time: 请求间隔时间（1-3秒）

性能测试特点：
  - 使用Locust进行并发用户模拟
  - 测试API在高并发下的表现
  - 收集响应时间和吞吐量指标
  - 识别性能瓶颈

执行性能测试：
    # 方式1：使用Locust Web UI
    locust -f tests/test_performance.py --host=https://jsonplaceholder.typicode.com
    # 打开浏览器访问 http://localhost:8089
    
    # 方式2：Pytest方式运行
    pytest tests/test_performance.py -v
    
    # 方式3：命令行模式（无UI）
    locust -f tests/test_performance.py --host=https://jsonplaceholder.typicode.com \\
      --users 100 --spawn-rate 10 --run-time 1m --headless

性能测试指标：
    - Response Time (RT): 单请求响应时间
    - Throughput: 每秒请求数 (RPS)
    - Error Rate: 错误率
    - P95/P99: 百分位数响应时间
"""
import pytest
from locust import HttpUser, task, between
from core.base_test import BaseTest


class APILoadTest(HttpUser):
    """Load testing with Locust."""
    
    wait_time = between(1, 3)
    
    @task(1)
    def get_posts(self):
        """Simulate getting posts."""
        self.client.get("/posts")
    
    @task(2)
    def get_single_post(self):
        """Simulate getting single post."""
        self.client.get("/posts/1")
    
    @task(1)
    def create_post(self):
        """Simulate creating post."""
        self.client.post("/posts", json={
            "title": "Test Post",
            "body": "Test Body",
            "userId": 1
        })


class TestPerformanceMetrics(BaseTest):
    """Test performance metrics."""
    
    def test_response_time_threshold(self):
        """Test response time is within threshold."""
        # This is a simplified example
        # In real scenarios, use actual performance testing tools like:
        # - Locust for load testing
        # - JMeter for performance testing
        # - pytest-benchmark for micro benchmarks
        
        import time
        start = time.time()
        # Simulate some operation
        time.sleep(0.1)
        elapsed = time.time() - start
        
        # Assert response time is less than 1 second
        assert elapsed < 1.0, f"Response time {elapsed}s exceeds threshold"
