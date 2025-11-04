# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

"""
Example 1: Initialize VikingMem service
"""

import os

from vikingdb import IAM
from vikingdb.memory import VikingMem


"""Initialize VikingMem with environment-provided credentials."""
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

print("✅ Client initialized successfully")


if __name__ == "__main__":
    # Recommended to use environment variables
    # export VIKINGDB_AK="your_ak"
    # export VIKINGDB_SK="your_sk"

    # Test if IAM credentials are correct, if correct, ping will succeed
    client.ping()
    
    # initialize collection
    ## example 1: using collection_name and project_name
    collection1 = client.get_collection(
        collection_name="sdk_test",  # Replace with your collection name
        project_name="default"
    )

    ## example 2: using resource_id
    collection2 = client.get_collection(
        resource_id="col-abc123xyz"
    )
    
