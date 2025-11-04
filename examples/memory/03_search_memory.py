# coding:utf-8
# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Example 3: Search Memories
"""

import os
import time

from vikingdb import IAM
from vikingdb.memory import VikingMem


# Initialize client (Recommended: initialize only once and reuse throughout the application lifecycle)
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

# Get collection (Recommended: get only once and reuse throughout the application lifecycle)
collection = client.get_collection(
    collection_name="sdk_test",  # Replace with your collection name
    project_name="default"
)


def search_user_profile():
    
    filter = {
        "user_id": "user_3",  
        "assistant_id": "111",
        "memory_type": ["profile_v1"],
    }
    result = collection.search_memory(
        filter=filter,
        limit=1
    )

    return result

def search_events_by_query(query: str):
    """Search events by query string"""
    filter = {
        "user_id": "user_3",  
        "assistant_id": "111",
        "memory_type": ["event_v1"],  # Search for event type
    }
    
    result = collection.search_memory(
        query=query,
        filter=filter,
        limit=10
    )
    return result

    
def search_recent_events():
    """Search recent events with time range filter"""
    # Get current timestamp in milliseconds
    current_time = int(time.time() * 1000)
    
    # Search events from last 24 hours
    one_day_ago = current_time - 24 * 60 * 60 * 1000
    
    filter = {
        "user_id": "user_3",
        "assistant_id": "111",
        "memory_type": ["event_v1"],  # Search for event type
        "start_time": one_day_ago,  # Start time in milliseconds
        "end_time": current_time,    # End time in milliseconds
    }

    result = collection.search_memory(
        filter=filter,
        limit=10
    )
    return result

if __name__ == "__main__":
    print("=== Viking Memory Search Examples ===\n")
    
    # 1. Search user profile
    res1 = search_user_profile()
    print("1. User profile search result:", res1)
    print()
    
    # 2. Search events by query
    res2 = search_events_by_query("how is the weather today")
    print("2. Event search by query result:", res2)
    print()
    
    # 3. Search recent events (with time range filter)
    res3 = search_recent_events()
    print("3. Recent events search result:", res3)
    print()
