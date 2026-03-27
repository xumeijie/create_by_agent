"""
协议适配器 (Protocol Adapters)

实现HTTP/REST、SOAP、GraphQL三种协议的测试适配器。

支持协议：
1. HTTP/REST
   - 支持标准HTTP方法: GET、POST、PUT、DELETE
   - 自动处理请求头和JSON序列化
   - 维护会话，方便测试API连接

2. SOAP
   - 使用zeep库实现WSDL解析
   - 支持自动化推导
   - 支持复杂多输入参数

3. GraphQL
   - 支持GraphQL查询语言
   - 支持变量传递
   - 返回结构化的JSON响应

使用示例：
    # HTTP适配器
    from core.adapter_factory import AdapterFactory
    adapter = AdapterFactory.get_protocol_adapter("http", base_url="http://api.example.com")
    response = adapter.send_request("GET", "/users")
    
    # SOAP适配器
    soap = AdapterFactory.get_protocol_adapter("soap", wsdl_url="http://example.com/service.wsdl")
    result = soap.send_request("UserService", "GetUser", user_id=1)
    
    # GraphQL适配器
    gql = AdapterFactory.get_protocol_adapter("graphql", endpoint="http://api.example.com/graphql")
    result = gql.send_request("query { users { id name } }")
"""
import requests
import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from zeep import Client as SoapClient


logger = logging.getLogger(__name__)


class ProtocolAdapter(ABC):
    """Base class for protocol adapters."""
    
    def __init__(self, timeout: int = 30):
        """Initialize protocol adapter."""
        self.timeout = timeout
    
    @abstractmethod
    def send_request(self, *args, **kwargs) -> Dict[str, Any]:
        """Send a request using the protocol."""
        pass


class HTTPAdapter(ProtocolAdapter):
    """HTTP/REST protocol adapter."""
    
    def __init__(self, base_url: str = "http://localhost:8080", timeout: int = 30):
        """Initialize HTTP adapter."""
        super().__init__(timeout)
        self.base_url = base_url
        self.session = requests.Session()
    
    def send_request(self, method: str, endpoint: str, 
                    data: Optional[Dict] = None, headers: Optional[Dict] = None) -> Dict[str, Any]:
        """Send HTTP request."""
        url = f"{self.base_url}{endpoint}"
        logger.info(f"HTTP {method} request to {url}")
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers, timeout=self.timeout)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, headers=headers, timeout=self.timeout)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, headers=headers, timeout=self.timeout)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            return {
                "status": response.status_code,
                "body": response.json() if response.text else {},
                "headers": dict(response.headers)
            }
        except Exception as e:
            logger.error(f"HTTP request failed: {str(e)}")
            raise


class SOAPAdapter(ProtocolAdapter):
    """SOAP protocol adapter."""
    
    def __init__(self, wsdl_url: str, timeout: int = 30):
        """Initialize SOAP adapter."""
        super().__init__(timeout)
        self.wsdl_url = wsdl_url
        self.client = SoapClient(wsdl=wsdl_url)
    
    def send_request(self, service: str, method: str, **kwargs) -> Dict[str, Any]:
        """Send SOAP request."""
        logger.info(f"SOAP request to {service}.{method}")
        
        try:
            service_obj = getattr(self.client.service, service)
            method_obj = getattr(service_obj, method)
            result = method_obj(**kwargs)
            
            return {
                "status": 200,
                "body": dict(result) if hasattr(result, '__dict__') else result,
                "headers": {}
            }
        except Exception as e:
            logger.error(f"SOAP request failed: {str(e)}")
            raise


class GraphQLAdapter(ProtocolAdapter):
    """GraphQL protocol adapter."""
    
    def __init__(self, endpoint: str = "http://localhost:8080/graphql", timeout: int = 30):
        """Initialize GraphQL adapter."""
        super().__init__(timeout)
        self.endpoint = endpoint
        self.session = requests.Session()
    
    def send_request(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """Send GraphQL request."""
        logger.info(f"GraphQL request to {self.endpoint}")
        
        try:
            payload = {
                "query": query,
                "variables": variables or {}
            }
            
            response = self.session.post(self.endpoint, json=payload, timeout=self.timeout)
            
            return {
                "status": response.status_code,
                "body": response.json() if response.text else {},
                "headers": dict(response.headers)
            }
        except Exception as e:
            logger.error(f"GraphQL request failed: {str(e)}")
            raise
