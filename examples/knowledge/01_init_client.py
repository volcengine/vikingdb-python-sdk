import os
from vikingdb.knowledge import VikingKnowledge
from vikingdb.auth import IAM


def init_client():
    ak = os.getenv("VOLC_AK")
    sk = os.getenv("VOLC_SK")
    client = VikingKnowledge(auth=IAM(ak=ak, sk=sk))
    return client


def init_collection(client: VikingKnowledge):
    resource_id = os.getenv("VIKING_COLLECTION_RID")
    collection_name = os.getenv("VIKING_COLLECTION_NAME") or "financial_reports"
    project_name = os.getenv("VIKING_PROJECT") or "default"
    return client.collection(resource_id=resource_id, collection_name=collection_name, project_name=project_name)


if __name__ == "__main__":
    client = init_client()
    collection = init_collection(client)
    print("client:", type(client).__name__)
    print("collection:", type(collection).__name__)
