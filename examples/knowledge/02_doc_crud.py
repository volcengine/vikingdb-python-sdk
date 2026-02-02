import os
import json
import time
from typing import List
from vikingdb.knowledge import VikingKnowledge
from vikingdb.auth import IAM
from vikingdb.knowledge import AddDocV2Request, ListDocsRequest, MetaItem, DedupOptions


def init_client():
    ak = os.getenv("VOLC_AK") or ""
    sk = os.getenv("VOLC_SK") or ""
    client = VikingKnowledge(auth=IAM(ak=ak, sk=sk))
    return client


def init_collection(client: VikingKnowledge):
    resource_id = os.getenv("VIKING_COLLECTION_RID")
    collection_name = os.getenv("VIKING_COLLECTION_NAME") or "financial_reports"
    project_name = os.getenv("VIKING_PROJECT") or "default"
    return client.collection(resource_id=resource_id, collection_name=collection_name, project_name=project_name)


def to_json_env(name: str):
    val = os.getenv(name)
    if not val:
        return None
    try:
        return json.loads(val)
    except Exception:
        return None

def add_doc_by_url(kc, *, doc_id: str, doc_name: str, doc_type: str, url: str, tag_list: List[MetaItem]):
    req = AddDocV2Request(
        doc_id=doc_id,
        doc_name=doc_name,
        doc_type=doc_type,
        uri=url,
        tag_list=tag_list,
    )
    res = kc.add_doc_v2(req)
    print("add_doc:", res)
    return res

def add_doc_by_tos(kc, *, doc_id: str, doc_name: str, doc_type: str, tos_path: str, tag_list: List[MetaItem]):
    req = AddDocV2Request(
        doc_id=doc_id,
        doc_name=doc_name,
        doc_type=doc_type,
        uri=tos_path,
        tag_list=tag_list,
    )
    res = kc.add_doc_v2(req)
    print("add_doc:", res)
    return res

def run_doc_crud():
    client = init_client()
    kc = init_collection(client)
    doc_id = "google-report-2025-q1"
    doc_name = "Google 2025 Q1 Financial Report"
    doc_type = "pdf"
    url = "https://pdf.dfcfw.com/pdf/H3_AP202504281663850212_1.pdf"
    meta = [
        MetaItem(field_name="category", field_type="string", field_value="financial_report"),
        MetaItem(field_name="quarter", field_type="string", field_value="Q1"),
        MetaItem(field_name="year", field_type="int64", field_value=2025),
    ]

    add_doc_by_url(
        kc,
        doc_id=doc_id,
        doc_name=doc_name,
        doc_type=doc_type,
        url=url,
        tag_list=meta,
    )
    info = kc.get_doc(doc_id, return_token_usage=True)
    print("get_doc:", info.model_dump(by_alias=True))

    meta.append(MetaItem(field_name="updated_at", field_type="int64", field_value=1714560000))
    upd_res = kc.update_doc_meta(doc_id, meta)
    print("update_doc_meta:", upd_res)

    time.sleep(30)

    new_name = doc_name + "-updated"
    upd_doc_res = kc.update_doc(doc_id, new_name)
    print("update_doc:", upd_doc_res)

    list_req = ListDocsRequest(offset=0, limit=10, return_token_usage=True)
    list_res = kc.list_docs(list_req)
    print("list_docs:", list_res.result.model_dump(by_alias=True))

    #del_res = kc.delete_doc(doc_id)
    #print("delete_doc:", del_res)


if __name__ == "__main__":
    run_doc_crud()
