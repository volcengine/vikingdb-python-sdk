import os
import sys
from vikingdb.auth import APIKey
from vikingdb.knowledge import VikingKnowledge
from vikingdb.knowledge.exceptions import VikingKnowledgeException
from vikingdb.knowledge.models.doc import AddDocV2Request
from vikingdb.knowledge.models.chat import ChatMessage
from vikingdb.knowledge.models.service_chat import ServiceChatRequest


def main():
    api_key = os.environ["VIKING_API_KEY"]

    endpoint = "api-knowledgebase.mlp.cn-beijing.volces.com"
    region = "cn-beijing"

    client = VikingKnowledge(
        host=endpoint,
        region=region,
        auth=APIKey(api_key=api_key),
        scheme="https",
    )

    collection_name = os.getenv("VIKING_COLLECTION_NAME") or "financial_reports"
    project_name = os.getenv("VIKING_PROJECT") or "default"

    collection = client.collection(
        collection_name=collection_name,
        project_name=project_name,
    )

    tos_uri = "tos://your-bucket/your-path/your-file.pdf"
    rsp = collection.add_doc_v2(
        AddDocV2Request(
            doc_id="your-doc-id",
            uri=tos_uri,
        )
    )
    print("add tos doc id:", rsp.result.doc_id)

    url_uri = "https://your-url.pdf"
    rsp = collection.add_doc_v2(
        AddDocV2Request(
            doc_id="your-doc-id",
            doc_name="your-file-name.pdf",
            uri=url_uri,
        )
    )
    print("add url doc id:", rsp.result.doc_id)

    query = "your query"
    req = ServiceChatRequest(
        service_resource_id=os.environ["VIKING_SERVICE_RID"],
        messages=[ChatMessage(role="user", content=query)],
        query_param=None,
        stream=False,
    )
    res = client.service_chat(req, timeout=120)
    print("service_chat:", res.model_dump(by_alias=True))



if __name__ == "__main__":
    try:
        main()
    except VikingKnowledgeException as e:
        print(f"Exception Code: {e.code}")
        print(f"Exception Message: {e.message}")
        print(f"Exception Request ID: {e.request_id}")
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)