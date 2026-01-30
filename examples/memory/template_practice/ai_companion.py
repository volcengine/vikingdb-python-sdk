# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Best Practice: AI Companion (情感陪伴)
通过记忆用户画像和重要事件，驱动高度个性化的交互

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

EVENT_TEMPLATES = ["event_v1"]
PROFILE_TEMPLATES = ["profile_v1"]


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


def add_companion_session():
    now_ts = int(time.time() * 1000)

    messages = [
        {"role": "user", "content": "我刚吃完晚饭，在沙发上摊着刷手机。"},
        {
            "role": "assistant",
            "content": "这种时刻很真实：身体终于坐下了，脑子还在滑来滑去。\n\n你晚饭吃了啥？我想听点生活细节。",
        },
        {"role": "user", "content": "点了个外卖，番茄牛腩饭，还行但有点咸。"},
        {
            "role": "assistant",
            "content": "番茄牛腩饭还行但偏咸这评价很到位。\n\n你吃饭的时候有配点啥吗？比如可乐/豆奶/汤？还是就硬吃？",
        },
        {"role": "user", "content": "就喝了点水。今天也没怎么运动。"},
        {
            "role": "assistant",
            "content": "那你现在如果愿意，我们做个超日常、超轻的：在家走 3 分钟。\n不用运动，不用出汗，就当把咸味散一散。\n\n你要是懒得起来也行，我换个问题：你今晚更想继续刷到困，还是想找个东西随便看两集/听点音乐？",
        },
        {"role": "user", "content": "继续刷到困吧，我最近脑子不想用力。"},
        {
            "role": "assistant",
            "content": "懂，今天的你想要的是省电模式。\n\n那我帮你把刷手机也刷得更舒服一点：\n- 你愿意把亮度调低一点吗？\n- 还有一个：定个小目标，比如再刷 15 分钟就去洗漱，别让它把你拖到太晚。\n\n我不催你，你就告诉我。你一般几点睡比较舒服？",
        },
        {"role": "user", "content": "12点左右吧，但经常拖到1点。"},
        {
            "role": "assistant",
            "content": "那我们不追求立刻变自律，就做一个更容易成功的版本：\n\n今晚的目标：**12:40 去洗漱**，洗完继续躺也可以。\n这样你不会被必须马上睡压到，但又能把入睡门槛降下来。\n\n你要不要我陪你做个小提醒？你回复我一个好，我就当作我们达成约定：到 12:40 你去洗漱。",
        },
    ]

    result = collection.add_session(
        session_id="companion_session_001",
        messages=messages,
        metadata={
            "default_user_id": "user_companion_001",
            "default_user_name": "CompanionUser",
            "default_assistant_id": "assistant_companion_001",
            "default_assistant_name": "AI Companion",
            "time": now_ts,
        },
    )

    return result


def search_companion_memories():
    event_result = None
    profile_result = None

    if EVENT_TEMPLATES:
        event_filter = {
            "user_id": "user_companion_001",
            "assistant_id": "assistant_companion_001",
            "memory_type": EVENT_TEMPLATES,
        }
        event_result = collection.search_event_memory(
            query="晚饭 睡觉", filter=event_filter, limit=5
        )

    if PROFILE_TEMPLATES:
        profile_filter = {
            "user_id": "user_companion_001",
            "assistant_id": "assistant_companion_001",
            "memory_type": PROFILE_TEMPLATES,
        }
        profile_result = collection.search_profile_memory(
            filter=profile_filter, limit=5
        )

    return {"event_memories": event_result, "profile_memories": profile_result}


if __name__ == "__main__":
    print("=== AI Companion Best Practice ===\n")

    print("Step 1: Adding companion session...")
    add_result = add_companion_session()
    print(f"Add session result: {add_result}\n")

    print("Step 2: Waiting 30 seconds for data processing...")
    time.sleep(30)
    print("✅ Wait completed\n")

    print("Step 3: Searching companion memories...")
    search_result = search_companion_memories()
    print(f"Search result: {search_result}\n")

    print("✅ AI Companion workflow completed")
