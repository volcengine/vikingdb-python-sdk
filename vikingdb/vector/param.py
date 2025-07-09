from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union, Any, Generic, TypeVar


class __ReqBaseDataApi(BaseModel):
    project_name: Optional[str] = Field(None, alias='project_name')


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
    partition: Optional[str] = Field(None, alias='partition')
    output_fields: Optional[List[str]] = Field(None, alias='output_fields')


class __RespBaseResult(BaseModel):
    pass


R = TypeVar('R', bound=__RespBaseResult)


class FetchDataItemInCollection(BaseModel):
    id: Union[int, str] = Field(..., alias='id')
    fields: Dict[str, Any] = Field(..., alias='fields')


class FetchDataItemInIndex(BaseModel):
    id: Union[int, str] = Field(..., alias='id')
    fields: Dict[str, Any] = Field(..., alias='fields')
    dense_vector: List[float] = Field(..., alias='dense_vector')
    dense_dim: int = Field(..., alias='dense_dim')


FDI = TypeVar('FDI', bound=Union[FetchDataItemInCollection, FetchDataItemInIndex])


class RespBaseDataApi(BaseModel, Generic[R]):
    api: str = Field(..., alias='api')
    request_id: str = Field(..., alias='request_id')
    code: str = Field(..., alias='code')
    message: str = Field(..., alias='message')
    result: R = Field(..., alias='result')


class __ResultBaseFetchData(__RespBaseResult, Generic[FDI]):
    fetch: List[FDI] = Field(..., alias='fetch')
    ids_not_exists: List[Dict[str, Any]] = Field(..., alias='ids_not_exists')


class ResultFetchDataInCollection(__ResultBaseFetchData[FetchDataItemInCollection]):
    pass


class ResultFetchDataInIndex(__ResultBaseFetchData[FetchDataItemInIndex]):
    pass


class TokenUsage(BaseModel):
    prompt_tokens: int = Field(0, alias='prompt_tokens')
    completion_tokens: int = Field(0, alias='completion_tokens')
    image_tokens: int = Field(0, alias='image_tokens')
    total_tokens: int = Field(0, alias='total_tokens')
