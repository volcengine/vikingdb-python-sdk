# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Example 4: Exceptions
"""

import os
import time

from vikingdb import IAM
from vikingdb.memory import VikingMem


# Initialize client
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


def add_session_exception():    
    collection = client.get_collection(
        collection_name="sdk_missing",
        project_name="default"
    )
    now_ts = int(time.time() * 1000)
    # Add session messages
    result = collection.add_session(
        session_id="session_001",
        messages=[
            {
                "role": "user",
                "content": "Hello, how is the weather today?"
            },
            {
                "role": "assistant",
                "content": "Today is sunny with a temperature of 22 degrees, perfect for going out."
            }
        ],
        metadata = {
            "default_user_id": "user_3",
            "default_user_name": "Li",
            "default_assistant_id": "111",
            "default_assistant_name": "Smart Assistant",
            # "group_id": "",
            "time": now_ts,
        }
    )
    
    return result




if __name__ == "__main__":
    print("Viking Memory Add Session Messages Example\n")
    
    add_session_exception()
    