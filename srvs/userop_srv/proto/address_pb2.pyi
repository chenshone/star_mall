from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddressRequest(_message.Message):
    __slots__ = ("id", "userId", "province", "city", "district", "address", "signerName", "signerMobile")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    PROVINCE_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    DISTRICT_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SIGNERNAME_FIELD_NUMBER: _ClassVar[int]
    SIGNERMOBILE_FIELD_NUMBER: _ClassVar[int]
    id: int
    userId: int
    province: str
    city: str
    district: str
    address: str
    signerName: str
    signerMobile: str
    def __init__(self, id: _Optional[int] = ..., userId: _Optional[int] = ..., province: _Optional[str] = ..., city: _Optional[str] = ..., district: _Optional[str] = ..., address: _Optional[str] = ..., signerName: _Optional[str] = ..., signerMobile: _Optional[str] = ...) -> None: ...

class AddressResponse(_message.Message):
    __slots__ = ("id", "userId", "province", "city", "district", "address", "signerName", "signerMobile")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    PROVINCE_FIELD_NUMBER: _ClassVar[int]
    CITY_FIELD_NUMBER: _ClassVar[int]
    DISTRICT_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SIGNERNAME_FIELD_NUMBER: _ClassVar[int]
    SIGNERMOBILE_FIELD_NUMBER: _ClassVar[int]
    id: int
    userId: int
    province: str
    city: str
    district: str
    address: str
    signerName: str
    signerMobile: str
    def __init__(self, id: _Optional[int] = ..., userId: _Optional[int] = ..., province: _Optional[str] = ..., city: _Optional[str] = ..., district: _Optional[str] = ..., address: _Optional[str] = ..., signerName: _Optional[str] = ..., signerMobile: _Optional[str] = ...) -> None: ...

class AddressListResponse(_message.Message):
    __slots__ = ("total", "data")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    total: int
    data: _containers.RepeatedCompositeFieldContainer[AddressResponse]
    def __init__(self, total: _Optional[int] = ..., data: _Optional[_Iterable[_Union[AddressResponse, _Mapping]]] = ...) -> None: ...
