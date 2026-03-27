"""
工具函数库 (Utils Module)

此模块提供测试框架的辅助工具函数：

1. 断言工具 (assertions.py)
   - 自定义的断言函数，提高代码可读性
   - 支持字典键检查、值验证、响应检查等
   - 提供详细的失败信息

2. 数据生成器 (data_generator.py)
   - 自动生成随机测试数据
   - 支持用户、产品、订单等多种数据类型
   - 生成随机电子邮件、电话号码、日期等

3. Mock工具 (mocking.py)
   - 模拟HTTP响应
   - 模拟数据库游标和连接
   - 简化外部依赖的模拟

使用方式：
    from utils.assertions import assert_status_code, assert_dict_keys
    from utils.data_generator import DataGenerator
    from utils.mocking import ResponseMocker
"""
