# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Best Practice: Customer Support (客服助理)
记录用户画像和重要事件，驱动高度个性化的服务

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

EVENT_TEMPLATES = ["event_customer_support"]
PROFILE_TEMPLATES = ["profile_customer_support"]


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


def add_support_session():
    now_ts = int(time.time() * 1000)

    messages = [
        {
            "role": "system",
            "content": "你是某电商平台的AI客服助手。你的目标是快速理解用户问题，先澄清关键信息，再给出可执行的解决方案。必要时引导用户提供订单号/手机号后四位等信息（注意隐私保护：不要索要完整身份证号/银行卡号）。语气友好、专业、简洁。",
        },
        {
            "role": "user",
            "content": "我昨天买的耳机到货了，但只有左边有声音，右边没声，怎么处理？",
        },
        {
            "role": "assistant",
            "content": "抱歉影响你使用了。我先帮你快速排查一下，通常是连接/音源或单只故障导致。\n\n请你确认3点：\n1）你用的是蓝牙还是有线？\n2）换一台手机/电脑连接，右耳仍然没声音吗？\n3）把左右耳互换佩戴/重置配对后有变化吗？\n\n另外，为了继续帮你发起售后，请发我：订单号（或截图打码）+ 收货手机号后四位。",
        },
        {
            "role": "user",
            "content": "蓝牙的。我换了手机还是右边没声。重置配对也不行。订单号是 1234567890，手机号后四位 8899。",
        },
        {
            "role": "assistant",
            "content": "收到。根据你的排查结果（换设备仍无声、重置无效），基本可判断为单只硬件异常。\n\n我这边给你两种处理方式，你选一个就行：\n- 方案A：换货（推荐）——寄回后我们给你换一副新的。\n- 方案B：退货退款——寄回验收后原路退款。\n\n补充确认两点以便我帮你提交：\n1）你更倾向换货还是退款？\n2）商品外观是否完好、配件（充电盒/线材/说明书）是否齐全？",
        },
        {"role": "user", "content": "换货吧。外观完好，配件都在。"},
        {
            "role": "assistant",
            "content": "好的，我帮你发起【换货】。\n\n流程说明：\n1）我将为订单 1234567890 创建换货申请；\n2）系统会生成上门取件/寄回地址（通常1小时内）；\n3）你把耳机和全部配件装回原包装（没有原箱也可用结实纸箱），外箱贴面单；\n4）仓库验收通过后，我们会安排补发新件。\n\n注意事项：\n- 请勿寄回个人赠品或非本订单物品；\n- 寄回前建议拍一张装箱照片，便于后续核对。\n\n你希望取件时间是：今天还是明天？大概哪个时间段（上午/下午/晚上）更方便？",
        },
        {"role": "user", "content": "明天下午吧。"},
        {
            "role": "assistant",
            "content": "可以的。我已为你提交换货申请，并备注【明天下午上门取件】。稍后你会在订单页看到换货单号和取件信息。\n\n如果明天取件前你想再自查一次，也可以试试：把耳机放回充电盒充满电后再重置一次（有时低电量会导致单耳失联）。不过按你目前情况，走换货会更省心。\n\n还有其他需要我一起处理的吗？",
        },
    ]

    result = collection.add_session(
        session_id="support_session_001",
        messages=messages,
        metadata={
            "default_user_id": "user_support_001",
            "default_user_name": "SupportUser",
            "default_assistant_id": "assistant_support_001",
            "default_assistant_name": "Customer Support",
            "time": now_ts,
        },
    )

    return result


def search_support_memories():
    event_result = None
    profile_result = None

    if EVENT_TEMPLATES:
        event_filter = {
            "user_id": "user_support_001",
            "assistant_id": "assistant_support_001",
            "memory_type": EVENT_TEMPLATES,
        }
        event_result = collection.search_event_memory(
            query="耳机 换货", filter=event_filter, limit=5
        )

    if PROFILE_TEMPLATES:
        profile_filter = {
            "user_id": "user_support_001",
            "assistant_id": "assistant_support_001",
            "memory_type": PROFILE_TEMPLATES,
        }
        profile_result = collection.search_profile_memory(
            filter=profile_filter, limit=5
        )

    return {"event_memories": event_result, "profile_memories": profile_result}


if __name__ == "__main__":
    print("=== Customer Support Best Practice ===\n")

    print("Step 1: Adding support session...")
    add_result = add_support_session()
    print(f"Add session result: {add_result}\n")

    print("Step 2: Waiting 30 seconds for data processing...")
    time.sleep(30)
    print("✅ Wait completed\n")

    print("Step 3: Searching support memories...")
    search_result = search_support_memories()
    print(f"Search result: {search_result}\n")

    print("✅ Customer Support workflow completed")
