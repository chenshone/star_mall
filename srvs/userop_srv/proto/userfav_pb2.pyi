from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserFavRequest(_message.Message):
    __slots__ = ("userId", "goodsId")
    USERID_FIELD_NUMBER: _ClassVar[int]
    GOODSID_FIELD_NUMBER: _ClassVar[int]
    userId: int
    goodsId: int
    def __init__(self, userId: _Optional[int] = ..., goodsId: _Optional[int] = ...) -> None: ...

class UserFavResponse(_message.Message):
    __slots__ = ("userId", "goodsId")
    USERID_FIELD_NUMBER: _ClassVar[int]
    GOODSID_FIELD_NUMBER: _ClassVar[int]
    userId: int
    goodsId: int
    def __init__(self, userId: _Optional[int] = ..., goodsId: _Optional[int] = ...) -> None: ...

class UserFavListResponse(_message.Message):
    __slots__ = ("total", "data")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    total: int
    data: _containers.RepeatedCompositeFieldContainer[UserFavResponse]
    def __init__(self, total: _Optional[int] = ..., data: _Optional[_Iterable[_Union[UserFavResponse, _Mapping]]] = ...) -> None: ...
