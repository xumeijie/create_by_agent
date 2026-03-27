"""
核心模块 (Core Module)

本模块包含测试框架的核心功能：
- 基础测试类 (BaseTest): 所有测试类的父类，提供通用setup/teardown
- 配置管理器 (ConfigManager): 管理不同环境的配置，支持dev/staging/prod
- 适配器工厂 (AdapterFactory): 使用工厂模式创建协议和数据库适配器

使用方式：
    from core.base_test import BaseTest
    from core.config_manager import ConfigManager
    from core.adapter_factory import AdapterFactory
"""
