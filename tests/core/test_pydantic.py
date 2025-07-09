import unittest

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional, Union
from datetime import datetime


class Address(BaseModel):
    street: str = Field(..., alias='streetName')  # 必选字段，映射到streetName
    city: str = Field(..., alias='cityName')  # 必选字段，映射到cityName
    state: Optional[str] = None  # 可选字段
    zip_code: Optional[str] = Field(None, alias='postalCode')  # 可选字段，映射到postalCode


class BillingInfo(BaseModel):
    payment_method: str = Field(..., alias='paymentMethod')  # 必选字段
    card_last_four: Optional[str] = Field(None, alias='cardLastFour')  # 可选字段


class User(BaseModel):
    id: int = Field(..., gt=0)  # 必选字段，必须大于0
    name: str  # 必选字段
    age: Optional[int] = Field(None, ge=0)  # 可选字段，必须大于等于0

    # 嵌套结构 - 必选字段
    address: Optional[Address] = None

    # 嵌套结构 - 可选字段
    billing: Optional[BillingInfo] = None

    # 列表类型 - 必选字段
    preferences: List[str] = Field(default_factory=list)

    # 复杂嵌套列表 - 可选字段
    orders: Optional[List[Dict[str, Union[str, int, float]]]] = None

    # 自动生成的字段
    created_at: datetime = Field(default_factory=datetime.now)


class TestPydantic(unittest.TestCase):
    """测试客户端初始化和配置"""

    def test_p1(self):
        json_data = {
            "id": "123a",
            "name": "Alice Smith",
            "email": "alice@example.com",
            "age": 3,
            "address": {
                "streetName": "123 Main St",  # 映射到Address.street
                "cityName": "New York",  # 映射到Address.city
                "postalCode": "10001",  # 映射到Address.zip_code
            },
            "billing": {
                "paymentMethod": "credit_card",
                "cardLastFour": "4242"
            },
            "preferences": ["books", "music"],
            "orders": [
                {"order_id": 1001, "total": 49.99, "status": "shipped"},
                {"order_id": 1002, "total": 19.95, "status": "pending"}
            ]
        }

        # 反序列化：JSON → 对象
        user = User(**json_data)

        # 验证对象属性
        print(f"Name: {user.name}")  # 输出: Alice Smith
        print(f"Billing: {user.billing.card_last_four}")  # 输出: 4242
        print(f"Created At: {user.created_at}")  # 输出: 当前时间

        # 序列化：对象 → JSON（使用别名）
        json_output = user.model_dump_json(
            by_alias=True,  # 使用字段别名
            exclude_none=True,  # 排除None值字段
            indent=2  # 格式化输出
        )

        print(json_output)