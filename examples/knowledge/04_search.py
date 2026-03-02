import os
from vikingdb.knowledge import VikingKnowledge, RerankDataItem
from vikingdb.auth import IAM, APIKey
from vikingdb.knowledge.models.search import (
    SearchCollectionRequest,
    SearchKnowledgeRequest,
    SearchKnowledgeResponse,
)
from vikingdb.knowledge.models.chat import ChatMessage, ChatCompletionRequest, ChatCompletionResponse
from vikingdb.knowledge.models.service_chat import ServiceChatRequest, ServiceChatResponse
from vikingdb.knowledge.exceptions import VikingKnowledgeException
from typing import cast


def init_client():
    ak = os.getenv("VOLC_AK")
    sk = os.getenv("VOLC_SK")
    client = VikingKnowledge(auth=IAM(ak=ak, sk=sk))
    return client

def init_client_by_apikey():
    api_key = os.getenv("VIKING_SERVICE_API_KEY")
    client = VikingKnowledge(auth=APIKey(api_key=api_key))
    return client


def init_collection(client: VikingKnowledge):
    resource_id = os.getenv("VIKING_COLLECTION_RID")
    collection_name = os.getenv("VIKING_COLLECTION_NAME") or "financial_reports"
    project_name = os.getenv("VIKING_PROJECT") or "default"
    return client.collection(resource_id=resource_id, collection_name=collection_name, project_name=project_name)


def run_search_collection():
    client = init_client()
    kc = init_collection(client)
    query = "2025 Q1 revenue growth"
    sc_req = SearchCollectionRequest(
        query=query,
        limit=10,
        dense_weight=0.5,
        rerank_switch=False,
        retrieve_count=25,
        endpoint_id=None,
        rerank_model="Doubao-pro-4k-rerank",
        rerank_only_chunk=False,
        query_param=None,
    )
    try:
        sc_res = kc.search_collection(sc_req)
        print("search_collection:", sc_res.model_dump(by_alias=True))
    except VikingKnowledgeException as e:
        print("search_collection_error:", e)


def run_search_knowledge():
    client = init_client()
    kc = init_collection(client)
    query = "2025 Q1 revenue growth"
    sk_req = SearchKnowledgeRequest(
        query=query,
        image_query=None,
        pre_processing=None,
        post_processing=None,
        query_param=None,
        limit=10,
        dense_weight=0.5,
    )
    try:
        sk_res = kc.search_knowledge(sk_req)
        print("search_knowledge:", sk_res.model_dump(by_alias=True))
        return sk_res
    except VikingKnowledgeException as e:
        print("search_knowledge_error:", e)

def make_messages(search_knowledge_rsp: SearchKnowledgeResponse, query: str):
    top_items = []
    for item in search_knowledge_rsp.result.result_list[:5]:
        title = item.chunk_title
        content = item.content
        top_items.append(f"【{title}】\n{content}")

    context_text = "\n\n".join(top_items) if top_items else "（检索结果为空或不可用）"
    system_prompt = (
        "你是一位专业的财报分析师，"
        "你需要根据「参考资料」来回答接下来的「用户问题」，这些信息在 <context></context> XML 标签之内。"
        "回答必须在参考资料范围内，尽可能简洁，无法回答时请礼貌说明并引导提供更多信息。"
        "\n\n<context>\n" + context_text + "\n</context>"
    )
    msgs = [
        ChatMessage(role="system", content=system_prompt),
        ChatMessage(role="user", content=query),
    ]
    return msgs


def run_search_knowledge_and_chat_completion():
    client = init_client()

    sk_res = cast(SearchKnowledgeResponse, run_search_knowledge())

    msgs = make_messages(sk_res, "总结下 2025 Q1 财报数据")

    req = ChatCompletionRequest(
        model="Doubao-1-5-pro-32k",
        messages=msgs,
        thinking=None,
        max_tokens=4096,
        temperature=0.1,
        return_token_usage=True,
        api_key=os.getenv("VIKING_CHAT_API_KEY"),
        stream=False,
    )
    try:
        res = cast(ChatCompletionResponse, client.chat_completion(req))
        print("chat_completion:", res.model_dump(by_alias=True))
    except VikingKnowledgeException as e:
        print("chat_completion_error:", e)

def run_search_knowledge_and_chat_completion_stream():
    client = init_client()
    sk_res = cast(SearchKnowledgeResponse, run_search_knowledge())

    msgs = make_messages(sk_res, "总结下 2025 Q1 财报数据")

    req = ChatCompletionRequest(
        model="Doubao-1-5-pro-32k",
        messages=msgs,
        thinking=None,
        max_tokens=4096,
        temperature=0.1,
        return_token_usage=True,
        api_key=os.getenv("VIKING_CHAT_API_KEY"),
        stream=True,
    )
    try:
        print("chat_completion_stream:")
        for chunk in client.chat_completion(req):
            print(chunk.result.generated_answer, end='')
        print("\n")
    except VikingKnowledgeException as e:
        print("chat_completion_stream_error:", e)


def run_service_chat():
    client = init_client_by_apikey()
    service_rid = os.getenv("VIKING_SERVICE_RID")
    msgs = [ChatMessage(role="user", content="列举 2025 Q1 财报里的三项亮点")]
    req = ServiceChatRequest(
        service_resource_id=service_rid,
        messages=msgs,
        query_param=None,
        stream=False,
    )
    try:
        res = cast(ServiceChatResponse, client.service_chat(req, timeout=120))

        print("service_chat:", res.model_dump(by_alias=True))
    except VikingKnowledgeException as e:
        print("service_chat_error:", e)

def run_service_chat_stream():
    client = init_client_by_apikey()
    service_rid = os.getenv("VIKING_SERVICE_RID")
    msgs = [ChatMessage(role="user", content="列举 2025 Q1 财报里的三项亮点")]
    req = ServiceChatRequest(
        service_resource_id=service_rid,
        messages=msgs,
        query_param=None,
        stream=True,
    )
    try:
        print("service_chat_stream:")
        for chunk in client.service_chat(req, timeout=120):
            print(chunk.result.generated_answer, end='')
        print("\n")
    except VikingKnowledgeException as e:
        print("service_chat_stream_error:", e)


def run_rerank_ops():
    client = init_client()
    query = "2025 Q1 revenue growth"
    datas = [
        RerankDataItem(query=query, content="Revenue grew 12% YoY to $3.4B.", title="Revenue"),
        RerankDataItem(query=query, content="Operating margin improved by 1.5pp to 17%.", title="Margin"),
    ]
    try:
        res = client.rerank(
            datas=datas,
            rerank_model="m3-v2-rerank",
            rerank_instruction=os.getenv("VIKING_RERANK_INSTRUCTION"),
            endpoint_id=None,
        )
        print("rerank:", res)
    except VikingKnowledgeException as e:
        print("rerank_error:", e)


if __name__ == "__main__":
    run_search_collection()
    run_search_knowledge()
    run_service_chat()
    run_service_chat_stream()
    run_rerank_ops()
    run_search_knowledge_and_chat_completion()
    run_search_knowledge_and_chat_completion_stream()
