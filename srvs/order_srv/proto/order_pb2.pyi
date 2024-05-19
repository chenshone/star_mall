from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserInfo(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class ShopCartInfoResponse(_message.Message):
    __slots__ = ("id", "userId", "goodsId", "nums", "checked")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    GOODSID_FIELD_NUMBER: _ClassVar[int]
    NUMS_FIELD_NUMBER: _ClassVar[int]
    CHECKED_FIELD_NUMBER: _ClassVar[int]
    id: int
    userId: int
    goodsId: int
    nums: int
    checked: bool
    def __init__(self, id: _Optional[int] = ..., userId: _Optional[int] = ..., goodsId: _Optional[int] = ..., nums: _Optional[int] = ..., checked: bool = ...) -> None: ...

class CartItemListResponse(_message.Message):
    __slots__ = ("total", "data")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    total: int
    data: _containers.RepeatedCompositeFieldContainer[ShopCartInfoResponse]
    def __init__(self, total: _Optional[int] = ..., data: _Optional[_Iterable[_Union[ShopCartInfoResponse, _Mapping]]] = ...) -> None: ...

class CartItemRequest(_message.Message):
    __slots__ = ("userId", "goodsId", "nums", "checked")
    USERID_FIELD_NUMBER: _ClassVar[int]
    GOODSID_FIELD_NUMBER: _ClassVar[int]
    NUMS_FIELD_NUMBER: _ClassVar[int]
    CHECKED_FIELD_NUMBER: _ClassVar[int]
    userId: int
    goodsId: int
    nums: int
    checked: bool
    def __init__(self, userId: _Optional[int] = ..., goodsId: _Optional[int] = ..., nums: _Optional[int] = ..., checked: bool = ...) -> None: ...

class OrderRequest(_message.Message):
    __slots__ = ("id", "userId", "address", "mobile", "name", "post")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    MOBILE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    POST_FIELD_NUMBER: _ClassVar[int]
    id: int
    userId: int
    address: str
    mobile: str
    name: str
    post: str
    def __init__(self, id: _Optional[int] = ..., userId: _Optional[int] = ..., address: _Optional[str] = ..., mobile: _Optional[str] = ..., name: _Optional[str] = ..., post: _Optional[str] = ...) -> None: ...

class OrderInfoResponse(_message.Message):
    __slots__ = ("id", "userId", "orderSn", "payType", "status", "post", "total", "address", "name", "mobile", "addTime")
    ID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    ORDERSN_FIELD_NUMBER: _ClassVar[int]
    PAYTYPE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    POST_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MOBILE_FIELD_NUMBER: _ClassVar[int]
    ADDTIME_FIELD_NUMBER: _ClassVar[int]
    id: int
    userId: int
    orderSn: str
    payType: str
    status: str
    post: str
    total: float
    address: str
    name: str
    mobile: str
    addTime: str
    def __init__(self, id: _Optional[int] = ..., userId: _Optional[int] = ..., orderSn: _Optional[str] = ..., payType: _Optional[str] = ..., status: _Optional[str] = ..., post: _Optional[str] = ..., total: _Optional[float] = ..., address: _Optional[str] = ..., name: _Optional[str] = ..., mobile: _Optional[str] = ..., addTime: _Optional[str] = ...) -> None: ...

class OrderListResponse(_message.Message):
    __slots__ = ("total", "data")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    total: int
    data: _containers.RepeatedCompositeFieldContainer[OrderInfoResponse]
    def __init__(self, total: _Optional[int] = ..., data: _Optional[_Iterable[_Union[OrderInfoResponse, _Mapping]]] = ...) -> None: ...

class OrderFilterRequest(_message.Message):
    __slots__ = ("userId", "pages", "pagePerNums")
    USERID_FIELD_NUMBER: _ClassVar[int]
    PAGES_FIELD_NUMBER: _ClassVar[int]
    PAGEPERNUMS_FIELD_NUMBER: _ClassVar[int]
    userId: int
    pages: int
    pagePerNums: int
    def __init__(self, userId: _Optional[int] = ..., pages: _Optional[int] = ..., pagePerNums: _Optional[int] = ...) -> None: ...

class OrderItemResponse(_message.Message):
    __slots__ = ("id", "orderId", "goodsId", "goodsName", "goodsImage", "goodsPrice", "nums")
    ID_FIELD_NUMBER: _ClassVar[int]
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    GOODSID_FIELD_NUMBER: _ClassVar[int]
    GOODSNAME_FIELD_NUMBER: _ClassVar[int]
    GOODSIMAGE_FIELD_NUMBER: _ClassVar[int]
    GOODSPRICE_FIELD_NUMBER: _ClassVar[int]
    NUMS_FIELD_NUMBER: _ClassVar[int]
    id: int
    orderId: int
    goodsId: int
    goodsName: str
    goodsImage: str
    goodsPrice: float
    nums: int
    def __init__(self, id: _Optional[int] = ..., orderId: _Optional[int] = ..., goodsId: _Optional[int] = ..., goodsName: _Optional[str] = ..., goodsImage: _Optional[str] = ..., goodsPrice: _Optional[float] = ..., nums: _Optional[int] = ...) -> None: ...

class OrderInfoDetailResponse(_message.Message):
    __slots__ = ("orderInfo", "data")
    ORDERINFO_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    orderInfo: OrderInfoResponse
    data: _containers.RepeatedCompositeFieldContainer[OrderItemResponse]
    def __init__(self, orderInfo: _Optional[_Union[OrderInfoResponse, _Mapping]] = ..., data: _Optional[_Iterable[_Union[OrderItemResponse, _Mapping]]] = ...) -> None: ...

class OrderStatus(_message.Message):
    __slots__ = ("OrderSn", "status")
    ORDERSN_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OrderSn: str
    status: str
    def __init__(self, OrderSn: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...
