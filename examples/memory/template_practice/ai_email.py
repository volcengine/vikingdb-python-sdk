# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Best Practice: Email Summary (邮件总结)
总结邮件结论与待办，便于追踪

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

EVENT_TEMPLATES = ["event_email"]
PROFILE_TEMPLATES = ["profile_email"]


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


def add_email_session():
    now_ts = int(time.time() * 1000)

    messages = [
        {
            "role": "user",
            "content": "Subject: [Action Required] 推荐页改版 V2 灰度发布计划确认（01/27）\n\n各位好，\n\n我们计划在 01/27（周一）开启 V2 的 10% 灰度，01/29（周三）视数据决定是否全量。请大家确认以下事项：\n\n1) 埋点字段是否今日可冻结（exposure_id、rank_index、event_time 毫秒）\n2) 客户端是否能在周一 10:00 前提供提测包\n3) 后端 /v2/feed 接口提测时间与回滚开关说明\n4) QA 回归范围与灰度验收口径\n\n文档：\n- 发布计划（草稿）：https://doc.example.com/reco-v2-release-plan\n\n请在今天 18:00 前邮件回复确认/风险。\n\nThanks,\nAlice",
        },
        {
            "role": "user",
            "content": "Re: [Action Required] 推荐页改版 V2 灰度发布计划确认（01/27）\n\nAlice 好，\n\n1) 埋点字段我今天 18:00 前可以冻结并补充字段定义（必填/可选）。\n- exposure_id：必填\n- rank_index：必填\n- event_time：新埋点统一毫秒（旧链路保持原样），我会在数据层做兼容转换，避免口径混乱。\n\n我会把最终版埋点文档更新到：\nhttps://doc.example.com/reco-v2-tracking-spec\n\n另外灰度期间我会按小时监控 CTR、完播率、负反馈率，并在群里同步异常。\n\nBob",
        },
        {
            "role": "user",
            "content": "Re: [Action Required] 推荐页改版 V2 灰度发布计划确认（01/27）\n\n确认后端计划：\n2) /v2/feed 接口今天 20:00 前提测。\n- 默认 AB 分桶：若请求缺少 ab_group，会走对照组逻辑，但我会加告警（缺失率>1% 报警）。\n- 回滚：保留 /v1/feed，灰度开关关闭后端仍可回退到 v1，预计无需重启。\n\n回滚说明我会在 01/24（周五）下班前补到发布计划文档。\n\nCharlie",
        },
        {
            "role": "user",
            "content": "Re: [Action Required] 推荐页改版 V2 灰度发布计划确认（01/27）\n\n我这边有风险需要同步：\n- 目前联调完成约 80%，但有 2 个疑似与图片缓存相关的 crash 在排查。\n- 我可以承诺：：明天（01/24）11:00 前给定位结论。\n\n对发布节奏建议：\n- 01/24 先给内测包\n- 01/27 周一 10:00 前给提测包\n- 若 crash 风险较高，建议先 1% 观察 2 小时再扩到 10%\n\n另外 event_time 毫秒口径：我会保证推荐页 V2 新埋点上报毫秒，不动公共库，避免影响其他页面。\n\nDiana",
        },
        {
            "role": "user",
            "content": "Re: [Action Required] 推荐页改版 V2 灰度发布计划确认（01/27）\n\nQA 侧确认：\n- 如果周一（01/27）要灰度 10%，我最晚需要周一 10:00 拿到冻结提测包。\n- 回归重点：AB 分桶是否生效、曝光埋点触发时机、灰度开关/回滚是否可用。\n\n请补充：\n1) 灰度开关配置路径/操作人\n2) 关键验收指标阈值（例如 CTR 下跌多少触发回滚）\n\nEllen",
        },
        {
            "role": "user",
            "content": "Re: [Action Required] 推荐页改版 V2 灰度发布计划确认（01/27）\n\n感谢大家，结论我汇总如下（如有遗漏请直接 reply）：\n\n【结论/决策】\n- 灰度节奏：01/27（周一）10% 灰度；若 crash 风险高则先 1% 观察 2 小时再扩；01/29（周三）视数据与稳定性决定是否全量。\n- 埋点口径：V2 新埋点 event_time 统一毫秒；旧链路保持不变；数据层做兼容转换。\n\n【待办（Owner/DDL）】\n1) Bob：01/23 18:00 前冻结埋点文档（含字段定义、必填/可选）\n   - https://doc.example.com/reco-v2-tracking-spec\n2) Charlie：01/23 20:00 前 /v2/feed 提测；01/24（周五）下班前补回滚说明与 ab_group 缺失告警策略\n3) Diana：01/24 11:00 前给 crash 定位结论；01/27 10:00 前提供提测包；补端上灰度/回滚开关说明\n4) Ellen：拿到周一提测包后开始回归；灰度阶段重点验证 AB/曝光埋点/回滚\n\n【待确认】\n- 灰度开关配置路径与操作人（Charlie/Diana 请在文档补充）\n- 验收阈值（CTR/负反馈触发回滚的阈值）：Bob 提个建议，我来拍板写入发布计划\n\n下次同步：01/27（周一）16:00 复盘灰度数据与稳定性。\n\nAlice",
        },
    ]

    result = collection.add_session(
        session_id="email_session_001",
        messages=messages,
        metadata={
            "default_user_id": "user_email_001",
            "default_user_name": "EmailUser",
            "default_assistant_id": "assistant_email_001",
            "default_assistant_name": "Email Summary",
            "time": now_ts,
        },
    )

    return result


def search_email_memories():
    event_result = None
    profile_result = None

    if EVENT_TEMPLATES:
        event_filter = {
            "user_id": "user_email_001",
            "assistant_id": "assistant_email_001",
            "memory_type": EVENT_TEMPLATES,
        }
        event_result = collection.search_event_memory(
            query="灰度发布 待办", filter=event_filter, limit=5
        )

    if PROFILE_TEMPLATES:
        profile_filter = {
            "user_id": "user_email_001",
            "assistant_id": "assistant_email_001",
            "memory_type": PROFILE_TEMPLATES,
        }
        profile_result = collection.search_profile_memory(
            filter=profile_filter, limit=5
        )

    return {"event_memories": event_result, "profile_memories": profile_result}


if __name__ == "__main__":
    print("=== Email Summary Best Practice ===\n")

    print("Step 1: Adding email session...")
    add_result = add_email_session()
    print(f"Add session result: {add_result}\n")

    print("Step 2: Waiting 30 seconds for data processing...")
    time.sleep(30)
    print("✅ Wait completed\n")

    print("Step 3: Searching email memories...")
    search_result = search_email_memories()
    print(f"Search result: {search_result}\n")

    print("✅ Email Summary workflow completed")
