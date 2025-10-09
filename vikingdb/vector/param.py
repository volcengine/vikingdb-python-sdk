# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: Apache-2.0

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union, Any, Generic, TypeVar

"""
request parameter structure
"""

class __ReqBaseDataApi(BaseModel):
    # project_name: Optional[str] = Field(None, alias='project_name')
    pass


class __ReqBaseCollection(__ReqBaseDataApi):
    resource_id: Optional[str] = Field(None, alias='resource_id')
    collection_name: Optional[str] = Field(None, alias='collection_name')


class __ReqBaseIndex(__ReqBaseCollection):
    index_name: str = Field(..., alias='index_name')


class __ReqBaseWriteData(__ReqBaseCollection):
    fields: List[Dict[str, Any]] = Field(..., alias='fields')
    ttl: Optional[int] = Field(None, alias='ttl')


class ReqUpsertData(__ReqBaseWriteData):
    is_async: bool = Field(None, alias='async')


class ReqUpdateData(__ReqBaseWriteData):
    pass


class ReqDeleteData(__ReqBaseCollection):
    ids: Optional[List[Union[int, str]]] = Field(None, alias='ids')
    del_all: Optional[bool] = Field(None, alias='del_all')


class ReqFetchDataInCollection(__ReqBaseCollection):
    ids: Optional[List[Union[int, str]]] = Field(None, alias='ids')


class ReqFetchDataInIndex(__ReqBaseIndex):
    ids: Optional[List[Union[int, str]]] = Field(None, alias='ids')
    # partition: Optional[str] = Field(None, alias='partition')
    output_fields: Optional[List[str]] = Field(None, alias='output_fields')


class ReqSearchAdvance(BaseModel):
    dense_weight: Optional[float] = Field(None, alias='dense_weight')
    ids_in: Optional[List[Union[int, str]]] = Field(None, alias='ids_in')
    ids_not_in: Optional[List[Union[int, str]]] = Field(None, alias='ids_not_in')
    post_process_ops: Optional[List[Dict[str, Any]]] = Field(None, alias='post_process_ops')
    post_process_input_limit: Optional[int] = Field(None, alias='post_process_input_limit')
    scale_k: Optional[float] = Field(None, alias='scale_k')


class __ReqBaseSearch(__ReqBaseIndex):
    filter: Optional[Dict[str, Any]] = Field(None, alias='filter')
    limit: Optional[int] = Field(None, alias='limit')
    offset: Optional[int] = Field(None, alias='offset')
    # partition: Optional[str] = Field(None, alias='partition')
    output_fields: Optional[List[str]] = Field(None, alias='output_fields')
    advance: Optional[ReqSearchAdvance] = Field(None, alias='advance')


class ReqSearchByVector(__ReqBaseSearch):
    dense_vector: List[float] = Field(..., alias='dense_vector')
    sparse_vector: Optional[Dict[str, float]] = Field(None, alias='sparse_vector')


class ReqSearchByMultiModal(__ReqBaseSearch):
    text: Optional[str] = Field(None, alias='text')
    image: Optional[Union[str, Dict[str, Any]]] = Field(None, alias='image')
    video: Optional[Union[str, Dict[str, Any]]] = Field(None, alias='video')
    need_instruction: Optional[bool] = Field(None, alias='need_instruction')


class ReqSearchById(__ReqBaseSearch):
    id: Union[int, str] = Field(..., alias='id')


class ReqSearchByScalar(__ReqBaseSearch):
    field: str = Field(..., alias='field')
    order: Optional[str] = Field(None, alias='order')


class ReqSearchByKeywords(__ReqBaseSearch):
    keywords: List[str] = Field(..., alias='keywords')
    case_sensitive: Optional[bool] = Field(None, alias='case_sensitive')


class ReqSearchByRandom(__ReqBaseSearch):
    pass


class ReqAggregate(__ReqBaseIndex):
    filter: Optional[Dict[str, Any]] = Field(None, alias='filter')
    # partition: Optional[str] = Field(None, alias='partition')
    op: str = Field(..., alias='op')
    field: Optional[str] = Field(None, alias='field')
    cond: Optional[Dict[str, Any]] = Field(None, alias='cond')


class ReqSort(__ReqBaseIndex):
    query_vector: List[float] = Field(..., alias='query_vector')
    ids: Optional[List[Union[int, str]]] = Field(None, alias='ids')


class EmbeddingModel(BaseModel):
    name: str = Field(..., alias='name')
    version: Optional[str] = Field(None, alias='version')
    dim: Optional[int] = Field(None, alias='dim')


class FullModalData(BaseModel):
    text: Optional[str] = Field(None, alias='text')
    image: Optional[Union[str, Dict[str, Any]]] = Field(None, alias='image')
    video: Optional[Union[str, Dict[str, Any]]] = Field(None, alias='video')


class EmbeddingData(BaseModel):
    text: Optional[str] = Field(None, alias='text')
    image: Optional[Union[str, Dict[str, Any]]] = Field(None, alias='image')
    video: Optional[Union[str, Dict[str, Any]]] = Field(None, alias='video')
    full_modal_seq: Optional[List[FullModalData]] = Field(None, alias='full_modal_seq')


class ReqEmbedding(__ReqBaseDataApi):
    dense_model: Optional[EmbeddingModel] = Field(None, alias='dense_model')
    sparse_model: Optional[EmbeddingModel] = Field(None, alias='sparse_model')
    data: Optional[List[EmbeddingData]] = Field(None, alias='data')


"""
response parameter structure
"""


class __RespBaseResult(BaseModel):
    pass


R = TypeVar('R', bound=__RespBaseResult)


class FetchDataItemInCollection(BaseModel):
    id: Union[int, str] = Field(..., alias='id')
    fields: Dict[str, Any] = Field(..., alias='fields')


class FetchDataItemInIndex(BaseModel):
    id: Union[int, str] = Field(..., alias='id')
    fields: Dict[str, Any] = Field(..., alias='fields')
    dense_vector: Optional[List[float]] = Field(None, alias='dense_vector')
    dense_dim: Optional[int] = Field(None, alias='dense_dim')


class SearchDataItem(BaseModel):
    id: Union[int, str] = Field(..., alias='id')
    fields: Dict[str, Any] = Field(..., alias='fields')
    score: float = Field(..., alias='score')
    ann_score: float = Field(None, alias='ann_score')


FDI = TypeVar('FDI', bound=Union[FetchDataItemInCollection, FetchDataItemInIndex])


class RespBaseDataApi(BaseModel, Generic[R]):
    api: str = Field(..., alias='api')
    request_id: str = Field(..., alias='request_id')
    code: str = Field(..., alias='code')
    message: str = Field(..., alias='message')
    result: R = Field(..., alias='result')


class ResultUpsertData(__RespBaseResult):
    token_usage: Optional[Any] = Field(None, alias='token_usage')


class ResultUpdateData(__RespBaseResult):
    token_usage: Optional[Any] = Field(None, alias='token_usage')


class ResultDeleteData(__RespBaseResult):
    pass


class __ResultBaseFetchData(__RespBaseResult, Generic[FDI]):
    fetch: List[FDI] = Field(..., alias='fetch')
    ids_not_exists: List[Dict[str, Any]] = Field(..., alias='ids_not_exists')


class ResultFetchDataInCollection(__ResultBaseFetchData[FetchDataItemInCollection]):
    pass


class ResultFetchDataInIndex(__ResultBaseFetchData[FetchDataItemInIndex]):
    pass


class ResultSearchData(__RespBaseResult):
    data: Optional[List[SearchDataItem]] = Field(None, alias='data')
    total_return_count: Optional[int] = Field(None, alias='total_return_count')
    filter_matched_count: Optional[int] = Field(None, alias='filter_matched_count')
    real_text_query: Optional[str] = Field(None, alias='real_text_query')
    token_usage: Optional[Any] = Field(None, alias='token_usage')

# # todo
# embedding
# sort
# agg
#
#
# class ResultAggregate(__RespBaseResult):
#     pass
