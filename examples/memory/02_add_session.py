# coding:utf-8
"""
Example 2: Add Session Messages
"""

import os
import time
from vikingdb.memory import VikingMemClient


# Initialize client
client = VikingMemClient(
    host="api-knowledgebase.mlp.cn-beijing.volces.com",
    region="cn-beijing",
    ak=os.getenv("VOLC_ACCESSKEY", "your_ak"),
    sk=os.getenv("VOLC_SECRETKEY", "your_sk"),
    scheme="http"
)

collection = client.get_collection(
    collection_name="sdk_demo1",  # Replace with your collection name
    project_name="default"
)


def add_session():    

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
    
    # Add conversation
    add_session()
    
    