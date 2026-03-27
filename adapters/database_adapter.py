"""
数据库适配器 (Database Adapters)

实现MySQL、Oracle、PostgreSQL三个数据库的测试适配器。

数据库支持：
1. MySQL
   - 使用mysql-connector-python驱动
   - 支持连接池
   - 高效率的查询一位归返

2. Oracle
   - 使用oracledb驱动
   - 支持事务预索
   - 常用的执行模式

3. PostgreSQL
   - 使用psycopg2驱动
   - 支持JSON数据类型
   - 整敏整软件处理

其中整敏操作：
- execute_query(sql): 执行SELECT查询，返回一个店对象列表
- execute_update(sql): 执行INSERT/UPDATE/DELETE，返回受影响行数

使用示例：
    from core.adapter_factory import AdapterFactory
    
    # 创建数据库连接
    db = AdapterFactory.get_database_adapter(
        "mysql",
        host="localhost",
        port=3306,
        user="root",
        password="password",
        database="test_db"
    )
    
    # 连接数据库
    db.connect()
    
    # 执行SELECT查询
    users = db.execute_query("SELECT * FROM users WHERE age > 18")
    print(f"Found {len(users)} users")
    
    # 执行更新
    affected = db.execute_update("UPDATE users SET status='active' WHERE id=1")
    print(f"Updated {affected} rows")
    
    # 断开连接
    db.disconnect()
"""
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


logger = logging.getLogger(__name__)


class DatabaseAdapter(ABC):
    """Base class for database adapters."""
    
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        """Initialize database adapter."""
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    @abstractmethod
    def connect(self) -> None:
        """Establish database connection."""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Close database connection."""
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a query and return results."""
        pass
    
    @abstractmethod
    def execute_update(self, query: str) -> int:
        """Execute an update/insert/delete and return row count."""
        pass


class MySQLAdapter(DatabaseAdapter):
    """MySQL database adapter."""
    
    def connect(self) -> None:
        """Connect to MySQL database."""
        try:
            import mysql.connector
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            logger.info(f"Connected to MySQL: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to MySQL: {str(e)}")
            raise
    
    def disconnect(self) -> None:
        """Disconnect from MySQL database."""
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from MySQL")
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute SELECT query."""
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def execute_update(self, query: str) -> int:
        """Execute update/insert/delete."""
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected


class OracleAdapter(DatabaseAdapter):
    """Oracle database adapter."""
    
    def connect(self) -> None:
        """Connect to Oracle database."""
        try:
            import oracledb
            self.connection = oracledb.connect(
                user=self.user,
                password=self.password,
                dsn=f"{self.host}:{self.port}/{self.database}"
            )
            logger.info(f"Connected to Oracle: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to Oracle: {str(e)}")
            raise
    
    def disconnect(self) -> None:
        """Disconnect from Oracle database."""
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from Oracle")
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute SELECT query."""
        cursor = self.connection.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()
        return results
    
    def execute_update(self, query: str) -> int:
        """Execute update/insert/delete."""
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected


class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL database adapter."""
    
    def connect(self) -> None:
        """Connect to PostgreSQL database."""
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.DictCursor = RealDictCursor
            logger.info(f"Connected to PostgreSQL: {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to connect to PostgreSQL: {str(e)}")
            raise
    
    def disconnect(self) -> None:
        """Disconnect from PostgreSQL database."""
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from PostgreSQL")
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute SELECT query."""
        cursor = self.connection.cursor(cursor_factory=self.DictCursor)
        cursor.execute(query)
        results = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        return results
    
    def execute_update(self, query: str) -> int:
        """Execute update/insert/delete."""
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected
