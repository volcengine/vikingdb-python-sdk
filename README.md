# Volcano VikingDB Python SDK

- Volcano VikingDB Python SDK 是一个用于访问向量库API的Python客户端库。该SDK提供了简单易用的接口，帮助开发者快速集成向量库服务到他们的应用中。
- Python库名：vikingdb

## 特性

- 简单易用的API接口
- 完善的错误处理机制
- 支持 Python 3.7 及以上版本
- 详细的文档和示例

## 安装

### 通过pip安装

```bash
pip install vikingdb
```

### 从源代码安装

```bash
git clone https://github.com/volcengine/vikingdb-python-sdk.git
cd vikingdb-python-sdk
pip install .
```

## 快速开始

### 初始化客户端

```python
from vikingdb import VectorDBClient

# 创建客户端实例
client = VectorDBClient(api_key="your_api_key")

# 或者稍后设置API密钥
client = VectorDBClient()
client.set_api_key("your_api_key")
```

### 创建向量

```python
vector_data = {
    "id": "vec1",
    "values": [0.1, 0.2, 0.3, 0.4],
    "metadata": {
        "text": "示例向量"
    }
}

result = client.create_vector(vector_data)
print(result)
```

### 搜索向量

```python
query_vector = {
    "values": [0.1, 0.2, 0.3, 0.4],
    "top_k": 5
}

result = client.search_vectors(query_vector)
print(result)
```

### 错误处理

```python
from core.exceptions import VectorDBError, VectorDBAuthError

try:
    result = client.search_vectors({"values": [0.1, 0.2, 0.3]})
except VectorDBAuthError as e:
    print(f"认证错误: {e}")
except VectorDBError as e:
    print(f"API错误: {e}")
    print(f"错误码: {e.code}")
    print(f"请求ID: {e.request_id}")
```

## 高级用法

### 自定义基础URL

```python
client = VectorDBClient(
    api_key="your_api_key",
    base_url="https://custom-api.volcstack.com"
)
```

### 设置请求超时

```python
client = VectorDBClient(
    api_key="your_api_key",
    timeout=60  # 60秒超时
)
```

### 直接使用HTTP方法

除了预定义的API方法外，您还可以直接使用HTTP方法访问任何API端点：

```python
# GET请求
result = client.get("/endpoint", params={"param1": "value1"})

# POST请求
result = client.post("/endpoint", data={"key": "value"})

# PUT请求
result = client.put("/endpoint", data={"key": "value"})

# DELETE请求
result = client.delete("/endpoint", params={"id": "123"})
```

## 错误码参考

SDK会抛出以下几种异常：

- `VectorDBError`: 所有异常的基类
- `VectorDBAuthError`: 认证错误
- `VectorDBRequestError`: 请求发送失败
- `VectorDBResponseError`: 响应解析失败
- `VectorDBValidationError`: 参数验证失败
- `VectorDBRateLimitError`: 请求频率超过限制

## 开发

### 运行测试

```bash
python -m unittest discover -s tests
```

### 构建文档

```bash
cd docs
make html
```

## 许可证

Apache 2.0 License