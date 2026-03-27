"""
适配器模块 (Adapters Module)

此模块提供协议和数据库的适配器帮手：

协议适配器 (Protocol Adapters):
- HTTPAdapter: REST/HTTP API测试，支持GET/POST/PUT/DELETE
- SOAPAdapter: SOAP Web服务测试，使用zeep库
- GraphQLAdapter: GraphQL API测试

数据库适配器 (Database Adapters):
- MySQLAdapter: MySQL数据库操作
- OracleAdapter: Oracle数据库操作
- PostgreSQLAdapter: PostgreSQL数据库操作

所有适配器都需要通过AdapterFactory来创建。
"""
