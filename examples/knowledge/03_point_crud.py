import os
import json
from vikingdb.knowledge import VikingKnowledge
from vikingdb.auth import IAM
from vikingdb.knowledge import (
    AddPointRequest,
    UpdatePointRequest,
    ListPointsRequest,
    DeletePointRequest,
)


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


def run_point_crud():
    client = init_client()
    kc = init_collection(client)
    doc_id = "google-report-2025-q1"
    chunk_type = "text"
    chunk_title = "Revenue Highlights"
    content = "Revenue grew 12% YoY to $3.4B."
    question = None
    fields = [
        {"field_name": "topic", "field_type": "string", "field_value": "revenue"},
        {"field_name": "year", "field_type": "int64", "field_value": 2025},
        {"field_name": "quarter", "field_type": "string", "field_value": "Q1"},
    ]

    add_req = AddPointRequest(
        doc_id=doc_id,
        chunk_type=chunk_type,
        chunk_title=chunk_title,
        content=content,
        question=question,
        fields=fields,
    )

    add_res = kc.add_point(add_req)
    print("add_point:", add_res)

    point_id = add_res.result.point_id

    info = kc.get_point(point_id, get_attachment_link=True)
    print("get_point:", info.model_dump(by_alias=True))


    upd_content = content + " Updated."
    upd_title = chunk_title + " (Updated)"
    upd_req = UpdatePointRequest(content=upd_content, chunk_title=upd_title)
    upd_res = kc.update_point(point_id, upd_req)
    print("update_point_content:", upd_res)


    upd_fields = [
        {"field_name": "topic", "field_type": "string", "field_value": "revenue"},
        {"field_name": "revised", "field_type": "bool", "field_value": True},
    ]
    upd_req = UpdatePointRequest(fields=upd_fields)
    upd_res = kc.update_point(point_id, upd_req)
    print("update_point_fields:", upd_res)

    list_req = ListPointsRequest(offset=0, limit=10, get_attachment_link=True)
    list_res = kc.list_points(list_req)
    print("list_points:", list_res.model_dump(by_alias=True))

    del_req = DeletePointRequest(point_id=point_id)
    del_res = kc.delete_point(del_req)
    print("delete_point:", del_res)


if __name__ == "__main__":
    run_point_crud()
