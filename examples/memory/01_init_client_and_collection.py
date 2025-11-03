# coding:utf-8
"""
Example 1: Initialize Viking Memory Client
"""

import os
from vikingdb.memory import VikingMemClient


def init_client():
    """Initialize client"""
    # Method 1: Using environment variables (recommended)
    client = VikingMemClient(
        host="api-knowledgebase.mlp.cn-beijing.volces.com",
        region="cn-beijing",
        ak=os.getenv("VOLC_ACCESSKEY", "your_ak"),
        sk=os.getenv("VOLC_SECRETKEY", "your_sk"),
        scheme="http",
    )
    
    print("✅ Client initialized successfully")
    return client



if __name__ == "__main__":
    # Recommended to use environment variables
    # export VOLC_ACCESSKEY="your_ak"
    # export VOLC_SECRETKEY="your_sk"
    
    client = init_client()
    
    # Test if AK/SK are correct, if correct, ping will succeed
    client.ping()
    
    # initialize collection
    ## example 1: using collection_name and project_name
    collection = client.get_collection(
        collection_name="sdk_demo1",  # Replace with your collection name
        project_name="default"
    )

    ## example 2: using resource_id
    collection = client.get_collection(
        resource_id="col-abc123xyz"
    )
    


