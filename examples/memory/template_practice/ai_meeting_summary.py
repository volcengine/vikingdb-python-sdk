# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Best Practice: Meeting Summary (会议总结)
沉淀会议结论与待办，便于追踪

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

EVENT_TEMPLATES = ["meeting_summary"]
PROFILE_TEMPLATES = ["profile_meeting"]


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


def add_meeting_session():
    now_ts = int(time.time() * 1000)

    messages = [
        {
            "role": "user",
            "content": "大家好，开始今天的项目例会，主题：推荐页改版 V2 的发布评审。目标是对齐范围、风险、上线时间、以及各自 action items。",
        },
        {
            "role": "user",
            "content": "我先同步后端：接口改造基本完成，新增了 /v2/feed 接口，支持AB参数。现在卡点是埋点字段还没最终定，怕上线后数据口径变动。",
        },
        {
            "role": "user",
            "content": "埋点字段我这边建议本周内冻结。V2 需要新增 exposure_id 和 rank_index，否则后面归因会很难做。另外老字段 event_time 要统一成毫秒。",
        },
        {
            "role": "user",
            "content": "客户端这边 UI 已经联调到 80%。但如果 event_time 要改成毫秒，我们端上要改一处公共库，会影响别的页面，风险有点大。",
        },
        {
            "role": "user",
            "content": "先记一下争议点：event_time 口径要不要在本次上线强制统一。王五你觉得不统一会有什么后果？",
        },
        {
            "role": "user",
            "content": "不统一的话，会出现同一个指标在不同报表里差 1000 倍的问题，后面修成本更高。我们可以允许旧字段继续上报，但新埋点必须毫秒，同时在数据层做兼容转换。",
        },
        {
            "role": "user",
            "content": "数据层兼容我支持。后端接口里我也可以直接返回毫秒时间戳，端上只要不做二次转换就行。",
        },
        {
            "role": "user",
            "content": "如果只要求新埋点毫秒，但不改公共库，只在推荐页埋点里保证毫秒，那我这边可控。公共库改动就先不动。",
        },
        {
            "role": "user",
            "content": "OK，这里形成一个决策：本次上线推荐页 V2 新埋点使用毫秒，旧链路保持不变；数据层做兼容转换，避免口径混乱。",
        },
        {
            "role": "user",
            "content": "测试侧有两个风险：1）AB 分桶参数如果缺失会走默认逻辑，可能导致灰度失效；2）曝光埋点触发时机变了，需要重新跑一遍回归。上线时间如果是下周三，我需要最晚周一中午拿到冻结包。",
        },
        {
            "role": "user",
            "content": "排期我们原来是下周三（01/29）全量，上周五（01/24）开始 10% 灰度。赵六、李四，这个能保证吗？",
        },
        {
            "role": "user",
            "content": "我这边灰度 01/24 有点紧。UI 还有两个 crash 问题在排查，比较像是图片缓存引起的。保守点：01/24 做内测包，01/27 周一再灰度。",
        },
        {
            "role": "user",
            "content": "后端没问题，接口今天可以提测。AB 参数缺失默认逻辑我再加一个告警，如果请求里没有 ab_group 就打点并报警。",
        },
        {
            "role": "user",
            "content": "那我们调整发布节奏：01/27（周一）10% 灰度，01/29（周三）视数据与稳定性再全量。小周，按这个节奏你需要什么？",
        },
        {
            "role": "user",
            "content": "我需要：1）周一上午 10 点前给到提测包；2）埋点字段列表冻结，最好今天发邮件/飞书文档；3）灰度开关和回滚滚方案写清楚。",
        },
        {
            "role": "user",
            "content": "埋点字段我今天 18:00 前给出最终版文档，并在文档里标注必填/可选。灰度期间我会盯核心指标：CTR、完播率、负反馈率，按小时出监控。",
        },
        {
            "role": "user",
            "content": "补充一个行动项：赵六你提到的 crash 问题，最迟什么时候能定位？如果周一还没解决，我们灰度要不要延后？",
        },
        {
            "role": "user",
            "content": "我今晚先把图片缓存策略降级，明天上午 11 点前给定位结论。如果还是高风险，我建议灰度推迟到周二，并先在 1% 观察 2 小时。",
        },
        {
            "role": "user",
            "content": "好，记录：客户端 crash 明天 11:00 前出结论；如高风险，先 1% 观察再扩到 10%。回滚方案由李四提供接口回退开关说明，赵六提供端上开关说明。",
        },
        {
            "role": "user",
            "content": "最后确认一下行动项：\n1）王五：今日 18:00 前冻结埋点文档（含 exposure_id、rank_index、毫秒口径说明）。\n2）李四：今日提测 /v2/feed；补 ab_group 缺失告警；周五前给回滚说明。\n3）赵六：明天 11:00 前 crash 定位；周一 10:00 前给测试包；端上灰度/回滚开关说明。\n4）小周：基于周一包开始回归，灰度阶段重点验证曝光埋点与AB分桶。\n\n下次会议：周一 16:00 复盘灰度数据与稳定性，决定周三是否全量。",
        },
    ]

    result = collection.add_session(
        session_id="meeting_session_001",
        messages=messages,
        metadata={
            "default_user_id": "user_meeting_001",
            "default_user_name": "MeetingUser",
            "default_assistant_id": "assistant_meeting_001",
            "default_assistant_name": "Meeting Summary",
            "time": now_ts,
        },
    )

    return result


def search_meeting_memories():
    event_result = None
    profile_result = None

    if EVENT_TEMPLATES:
        event_filter = {
            "user_id": "user_meeting_001",
            "assistant_id": "assistant_meeting_001",
            "memory_type": EVENT_TEMPLATES,
        }
        event_result = collection.search_event_memory(
            query="灰度 发布 待办", filter=event_filter, limit=5
        )

    if PROFILE_TEMPLATES:
        profile_filter = {
            "user_id": "user_meeting_001",
            "assistant_id": "assistant_meeting_001",
            "memory_type": PROFILE_TEMPLATES,
        }
        profile_result = collection.search_profile_memory(
            filter=profile_filter, limit=5
        )

    return {"event_memories": event_result, "profile_memories": profile_result}


if __name__ == "__main__":
    print("=== Meeting Summary Best Practice ===\n")

    print("Step 1: Adding meeting session...")
    add_result = add_meeting_session()
    print(f"Add session result: {add_result}\n")

    print("Step 2: Waiting 30 seconds for data processing...")
    time.sleep(30)
    print("✅ Wait completed\n")

    print("Step 3: Searching meeting memories...")
    search_result = search_meeting_memories()
    print(f"Search result: {search_result}\n")

    print("✅ Meeting Summary workflow completed")
