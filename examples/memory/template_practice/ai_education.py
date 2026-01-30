# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Best Practice: Education Assistant (教育助手)
记录学生偏好与进度，持续个性化辅导

最佳实践说明：
1. 客户端和 Collection 初始化：
   - 客户端和 Collection 建议在应用启动时初始化一次，全局复用
   - 避免在每次请求时重复创建，可以显著降低调用成本

2. 批量添加会话：
   - 建议收集多条消息后批量调用 add_session，而非每条消息单独调用
   - 可以减少网络往返次数，降低延迟和成本

3. 调用间隔控制：
   - add_session 调用后建议等待 30 秒再进行下一次操作
   - 给服务端足够时间处理和索引数据，避免并发冲突

4. 搜索优化：
   - 使用 search_event_memory 和 search_profile_memory 分别搜索
   - 只在需要时调用对应的搜索方法，避免不必要的查询
   - 合理设置 limit 参数，避免返回过多数据

 5. Session 管理：
    - 相同用户的多轮对话建议使用相同的 session_id
    - 便于服务端关联和检索相关上下文
"""

import os
import time

from vikingdb import IAM
from vikingdb.memory import VikingMem


YOUR_COLLECTION_NAME = "your_collection_name"

EVENT_TEMPLATES = ["event_education"]
PROFILE_TEMPLATES = ["profile_education", "knowledge_mastery"]


_auth = IAM(
    ak=os.getenv("VIKINGDB_AK", "your_ak"),
    sk=os.getenv("VIKINGDB_SK", "your_sk"),
)
client = VikingMem(
    host="api-knowledgebase.mlp.cn-beijing.volces.com",
    region="cn-beijing",
    auth=_auth,
    scheme="http",
)

collection = client.get_collection(collection_name=YOUR_COLLECTION_NAME)


def add_education_session():
    now_ts = int(time.time() * 1000)

    messages = [
        {
            "role": "system",
            "content": "你是教育助手（Education Assistant）。你的目标是：记录学生偏好与学习进度，持续个性化辅导。教学风格：循序渐进、先结论后例题、鼓励学生用自己的话复述；遇到不确定要先澄清。每次讲解包含：核心概念→步骤/方法→例题→小练习→检查理解。",
        },
        {
            "role": "user",
            "content": "我总是不会把二次函数化成顶点式，尤其是配方法。能教我吗？",
        },
        {
            "role": "assistant",
            "content": "可以。我们就盯住一个知识点：**用配方法把二次函数化成顶点式**。\n\n**1）你要记住的目标形式**\n二次函数顶点式：\n> y = a(x - h)^2 + k\n这样顶点就是 (h, k)，且 a 决定开口方向与胖瘦。\n\n**2）配方法的固定套路（适用于 a=1 或先把 a 提出去）**\n对 y = ax^2 + bx + c：\n- 第一步：如果 a≠1，先把 a 从 x^2 和 x 项里提出：\n  y = a(x^2 + (b/a)x) + c\n- 第二步：在括号内补一个平方：\n  x^2 + px = (x + p/2)^2 - (p/2)^2\n  这里 p = b/a\n- 第三步：把补进去的减回来，并整理成 a(x-h)^2 + k。\n\n**3）例题：把 y = x^2 + 6x + 5 化成顶点式**\n(1) 先看 a=1，直接配：\n  x^2 + 6x + 5\n(2) 把 x^2+6x 配成完全平方：\n  x^2 + 6x = (x+3)^2 - 9\n(3) 代回去：\n  y = (x+3)^2 - 9 + 5 = (x+3)^2 - 4\n所以顶点式：\n> y = (x+3)^2 - 4\n顶点：(-3, -4)\n\n**4）你常见的坑（提前避开）**\n- 坑A：只加了 (p/2)^2，却忘了减回来。\n- 坑B：p 是 x 的系数，不是 b b本身；要先确保 x^2 系数为 1（或先提 a）。\n\n**5）小练习（你来做，我来帮你改）**\n把下面这个化成顶点式：\n> y = 2x^2 + 8x + 1\n提示：先把 2 提出去。\n\n你先告诉我：提 2 之后括号里变成什么？",
        },
        {"role": "user", "content": "是不是 y = 2(x^2 + 4x) + 1？"},
        {
            "role": "assistant",
            "content": "对，第一步完全正确。\n\n接下来我们配括号里的：x^2 + 4x。\n- 这里 p=4，所以 (p/2)^2 = 2^2 = 4。\n因此：\n  x^2 + 4x = (x+2)^2 - 4\n\n代回原式：\n  y = 2[(x+2)^2 - 4] + 1\n  y = 2(x+2)^2 - 8 + 1\n  y = 2(x+2)^2 - 7\n\n所以顶点式是：\n> y = 2(x+2)^2 - 7\n顶点：(-2, -7)\n\n为了确认你真的掌握了：\n**问题**：你能用一句话解释为什么要先把 2 提出去吗？",
        },
    ]

    result = collection.add_session(
        session_id="education_session_001",
        messages=messages,
        metadata={
            "default_user_id": "user_education_001",
            "default_user_name": "Student",
            "default_assistant_id": "assistant_education_001",
            "default_assistant_name": "Education Assistant",
            "time": now_ts,
        },
    )

    return result


def search_education_memories():
    event_result = None
    profile_result = None

    if EVENT_TEMPLATES:
        event_filter = {
            "user_id": "user_education_001",
            "assistant_id": "assistant_education_001",
            "memory_type": EVENT_TEMPLATES,
        }
        event_result = collection.search_event_memory(
            query="二次函数 配方法", filter=event_filter, limit=5
        )

    if PROFILE_TEMPLATES:
        profile_filter = {
            "user_id": "user_education_001",
            "assistant_id": "assistant_education_001",
            "memory_type": PROFILE_TEMPLATES,
        }
        profile_result = collection.search_profile_memory(
            filter=profile_filter, limit=5
        )

    return {"event_memories": event_result, "profile_memories": profile_result}


if __name__ == "__main__":
    print("=== Education Assistant Best Practice ===\n")

    print("Step 1: Adding education session...")
    add_result = add_education_session()
    print(f"Add session result: {add_result}\n")

    print("Step 2: Waiting 30 seconds for data processing...")
    time.sleep(30)
    print("✅ Wait completed\n")

    print("Step 3: Searching education memories...")
    search_result = search_education_memories()
    print(f"Search result: {search_result}\n")

    print("✅ Education Assistant workflow completed")
