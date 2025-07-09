"""
异常处理模块

定义SDK特定的异常类，用于处理不同类型的错误。
"""

from typing import Optional

class VectorDBError(Exception):
    """向量库API错误基类
    
    所有SDK特定异常的基类。
    
    Attributes:
        code (str): 错误码
        message (str): 错误信息
        request_id (str): 请求ID
        status_code (int): HTTP状态码
    """
    
    def __init__(
        self,
        message: str = "未知错误",
        code: str = "Unknown",
        request_id: str = None,
        status_code: int = None
    ):
        """初始化异常
        
        Args:
            message (str, optional): 错误信息，默认为"未知错误"
            code (str, optional): 错误码，默认为"Unknown"
            request_id (str, optional): 请求ID
            status_code (int, optional): HTTP状态码
        """
        self.code = code
        self.message = message
        self.request_id = request_id
        self.status_code = status_code
        
        error_msg = f"{message}"
        if code:
            error_msg = f"[{code}] {error_msg}"
        if request_id:
            error_msg = f"{error_msg} (request_id: {request_id})"
        if status_code:
            error_msg = f"{error_msg} (status: {status_code})"
        
        super().__init__(error_msg)


class VectorDBAuthError(VectorDBError):
    """认证错误
    
    当API认证失败时抛出此异常。
    """
    
    def __init__(self, message: str = "认证失败", **kwargs):
        """初始化认证错误异常
        
        Args:
            message (str, optional): 错误信息，默认为"认证失败"
            **kwargs: 其他参数，传递给父类
        """
        super().__init__(message=message, code="AuthError", **kwargs)


class VectorDBRequestError(VectorDBError):
    """请求错误
    
    当请求发送失败时抛出此异常。
    """
    
    def __init__(self, message: str = "请求失败", **kwargs):
        """初始化请求错误异常
        
        Args:
            message (str, optional): 错误信息，默认为"请求失败"
            **kwargs: 其他参数，传递给父类
        """
        super().__init__(message=message, code="RequestError", **kwargs)


class VectorDBResponseError(VectorDBError):
    """响应错误
    
    当响应解析失败时抛出此异常。
    """
    
    def __init__(self, message: str = "响应解析失败", **kwargs):
        """初始化响应错误异常
        
        Args:
            message (str, optional): 错误信息，默认为"响应解析失败"
            **kwargs: 其他参数，传递给父类
        """
        super().__init__(message=message, code="ResponseError", **kwargs)


class VectorDBValidationError(VectorDBError):
    """验证错误
    
    当请求参数验证失败时抛出此异常。
    """
    
    def __init__(self, message: str = "参数验证失败", **kwargs):
        """初始化验证错误异常
        
        Args:
            message (str, optional): 错误信息，默认为"参数验证失败"
            **kwargs: 其他参数，传递给父类
        """
        super().__init__(message=message, code="ValidationError", **kwargs)


class VectorDBRateLimitError(VectorDBError):
    """速率限制错误
    
    当API请求超过速率限制时抛出此异常。
    """
    
    def __init__(self, message: str = "请求频率超过限制", **kwargs):
        """初始化速率限制错误异常
        
        Args:
            message (str, optional): 错误信息，默认为"请求频率超过限制"
            **kwargs: 其他参数，传递给父类
        """
        super().__init__(message=message, code="RateLimitError", **kwargs)