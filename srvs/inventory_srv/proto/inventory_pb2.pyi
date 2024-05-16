from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GoodsInvInfo(_message.Message):
    __slots__ = ("goodsId", "num")
    GOODSID_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    goodsId: int
    num: int
    def __init__(self, goodsId: _Optional[int] = ..., num: _Optional[int] = ...) -> None: ...

class SellInfo(_message.Message):
    __slots__ = ("goodsInfo", "orderSn")
    GOODSINFO_FIELD_NUMBER: _ClassVar[int]
    ORDERSN_FIELD_NUMBER: _ClassVar[int]
    goodsInfo: _containers.RepeatedCompositeFieldContainer[GoodsInvInfo]
    orderSn: str
    def __init__(self, goodsInfo: _Optional[_Iterable[_Union[GoodsInvInfo, _Mapping]]] = ..., orderSn: _Optional[str] = ...) -> None: ...
