from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CategoryListRequest(_message.Message):
    __slots__ = ("id", "level")
    ID_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    id: int
    level: int
    def __init__(self, id: _Optional[int] = ..., level: _Optional[int] = ...) -> None: ...

class CategoryInfoRequest(_message.Message):
    __slots__ = ("id", "name", "parentCategory", "level", "isTab")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARENTCATEGORY_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    ISTAB_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    parentCategory: int
    level: int
    isTab: bool
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., parentCategory: _Optional[int] = ..., level: _Optional[int] = ..., isTab: bool = ...) -> None: ...

class DeleteCategoryRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class QueryCategoryRequest(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class CategoryInfoResponse(_message.Message):
    __slots__ = ("id", "name", "parentCategory", "level", "isTab")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARENTCATEGORY_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    ISTAB_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    parentCategory: int
    level: int
    isTab: bool
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., parentCategory: _Optional[int] = ..., level: _Optional[int] = ..., isTab: bool = ...) -> None: ...

class CategoryListResponse(_message.Message):
    __slots__ = ("total", "data", "jsonData")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    JSONDATA_FIELD_NUMBER: _ClassVar[int]
    total: int
    data: _containers.RepeatedCompositeFieldContainer[CategoryInfoResponse]
    jsonData: str
    def __init__(self, total: _Optional[int] = ..., data: _Optional[_Iterable[_Union[CategoryInfoResponse, _Mapping]]] = ..., jsonData: _Optional[str] = ...) -> None: ...

class SubCategoryListResponse(_message.Message):
    __slots__ = ("total", "info", "subCategorys")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    SUBCATEGORYS_FIELD_NUMBER: _ClassVar[int]
    total: int
    info: CategoryInfoResponse
    subCategorys: _containers.RepeatedCompositeFieldContainer[CategoryInfoResponse]
    def __init__(self, total: _Optional[int] = ..., info: _Optional[_Union[CategoryInfoResponse, _Mapping]] = ..., subCategorys: _Optional[_Iterable[_Union[CategoryInfoResponse, _Mapping]]] = ...) -> None: ...

class CategoryBrandFilterRequest(_message.Message):
    __slots__ = ("pages", "pagePerNums")
    PAGES_FIELD_NUMBER: _ClassVar[int]
    PAGEPERNUMS_FIELD_NUMBER: _ClassVar[int]
    pages: int
    pagePerNums: int
    def __init__(self, pages: _Optional[int] = ..., pagePerNums: _Optional[int] = ...) -> None: ...

class FilterRequest(_message.Message):
    __slots__ = ("pages", "pagePerNums")
    PAGES_FIELD_NUMBER: _ClassVar[int]
    PAGEPERNUMS_FIELD_NUMBER: _ClassVar[int]
    pages: int
    pagePerNums: int
    def __init__(self, pages: _Optional[int] = ..., pagePerNums: _Optional[int] = ...) -> None: ...

class CategoryBrandRequest(_message.Message):
    __slots__ = ("id", "categoryId", "brandId")
    ID_FIELD_NUMBER: _ClassVar[int]
    CATEGORYID_FIELD_NUMBER: _ClassVar[int]
    BRANDID_FIELD_NUMBER: _ClassVar[int]
    id: int
    categoryId: int
    brandId: int
    def __init__(self, id: _Optional[int] = ..., categoryId: _Optional[int] = ..., brandId: _Optional[int] = ...) -> None: ...

class CategoryBrandResponse(_message.Message):
    __slots__ = ("id", "brand", "category")
    ID_FIELD_NUMBER: _ClassVar[int]
    BRAND_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    id: int
    brand: BrandInfoResponse
    category: CategoryInfoResponse
    def __init__(self, id: _Optional[int] = ..., brand: _Optional[_Union[BrandInfoResponse, _Mapping]] = ..., category: _Optional[_Union[CategoryInfoResponse, _Mapping]] = ...) -> None: ...

class BannerRequest(_message.Message):
    __slots__ = ("id", "index", "image", "url")
    ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    id: int
    index: int
    image: str
    url: str
    def __init__(self, id: _Optional[int] = ..., index: _Optional[int] = ..., image: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class BannerResponse(_message.Message):
    __slots__ = ("id", "index", "image", "url")
    ID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    IMAGE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    id: int
    index: int
    image: str
    url: str
    def __init__(self, id: _Optional[int] = ..., index: _Optional[int] = ..., image: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class BrandFilterRequest(_message.Message):
    __slots__ = ("pages", "pagePerNums")
    PAGES_FIELD_NUMBER: _ClassVar[int]
    PAGEPERNUMS_FIELD_NUMBER: _ClassVar[int]
    pages: int
    pagePerNums: int
    def __init__(self, pages: _Optional[int] = ..., pagePerNums: _Optional[int] = ...) -> None: ...

class BrandRequest(_message.Message):
    __slots__ = ("id", "name", "logo")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOGO_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    logo: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., logo: _Optional[str] = ...) -> None: ...

class BrandInfoResponse(_message.Message):
    __slots__ = ("id", "name", "logo")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOGO_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    logo: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., logo: _Optional[str] = ...) -> None: ...

class BrandListResponse(_message.Message):
    __slots__ = ("total", "data")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    total: int
    data: _containers.RepeatedCompositeFieldContainer[BrandInfoResponse]
    def __init__(self, total: _Optional[int] = ..., data: _Optional[_Iterable[_Union[BrandInfoResponse, _Mapping]]] = ...) -> None: ...

class BannerListResponse(_message.Message):
    __slots__ = ("total", "data")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    total: int
    data: _containers.RepeatedCompositeFieldContainer[BannerResponse]
    def __init__(self, total: _Optional[int] = ..., data: _Optional[_Iterable[_Union[BannerResponse, _Mapping]]] = ...) -> None: ...

class CategoryBrandListResponse(_message.Message):
    __slots__ = ("total", "data")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    total: int
    data: _containers.RepeatedCompositeFieldContainer[CategoryBrandResponse]
    def __init__(self, total: _Optional[int] = ..., data: _Optional[_Iterable[_Union[CategoryBrandResponse, _Mapping]]] = ...) -> None: ...

class BatchGoodsIdInfo(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[_Iterable[int]] = ...) -> None: ...

class DeleteGoodsInfo(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class CategoryBriefInfoResponse(_message.Message):
    __slots__ = ("id", "name")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ...) -> None: ...

class CategoryFilterRequest(_message.Message):
    __slots__ = ("id", "isTab")
    ID_FIELD_NUMBER: _ClassVar[int]
    ISTAB_FIELD_NUMBER: _ClassVar[int]
    id: int
    isTab: bool
    def __init__(self, id: _Optional[int] = ..., isTab: bool = ...) -> None: ...

class GoodInfoRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class CreateGoodsInfo(_message.Message):
    __slots__ = ("id", "name", "goodsSn", "stocks", "marketPrice", "shopPrice", "goodsBrief", "goodsDesc", "shipFree", "images", "descImages", "goodsFrontImage", "isNew", "isHot", "onSale", "categoryId", "brandId")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    GOODSSN_FIELD_NUMBER: _ClassVar[int]
    STOCKS_FIELD_NUMBER: _ClassVar[int]
    MARKETPRICE_FIELD_NUMBER: _ClassVar[int]
    SHOPPRICE_FIELD_NUMBER: _ClassVar[int]
    GOODSBRIEF_FIELD_NUMBER: _ClassVar[int]
    GOODSDESC_FIELD_NUMBER: _ClassVar[int]
    SHIPFREE_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    DESCIMAGES_FIELD_NUMBER: _ClassVar[int]
    GOODSFRONTIMAGE_FIELD_NUMBER: _ClassVar[int]
    ISNEW_FIELD_NUMBER: _ClassVar[int]
    ISHOT_FIELD_NUMBER: _ClassVar[int]
    ONSALE_FIELD_NUMBER: _ClassVar[int]
    CATEGORYID_FIELD_NUMBER: _ClassVar[int]
    BRANDID_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    goodsSn: str
    stocks: int
    marketPrice: float
    shopPrice: float
    goodsBrief: str
    goodsDesc: str
    shipFree: bool
    images: _containers.RepeatedScalarFieldContainer[str]
    descImages: _containers.RepeatedScalarFieldContainer[str]
    goodsFrontImage: str
    isNew: bool
    isHot: bool
    onSale: bool
    categoryId: int
    brandId: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., goodsSn: _Optional[str] = ..., stocks: _Optional[int] = ..., marketPrice: _Optional[float] = ..., shopPrice: _Optional[float] = ..., goodsBrief: _Optional[str] = ..., goodsDesc: _Optional[str] = ..., shipFree: bool = ..., images: _Optional[_Iterable[str]] = ..., descImages: _Optional[_Iterable[str]] = ..., goodsFrontImage: _Optional[str] = ..., isNew: bool = ..., isHot: bool = ..., onSale: bool = ..., categoryId: _Optional[int] = ..., brandId: _Optional[int] = ...) -> None: ...

class GoodsReduceRequest(_message.Message):
    __slots__ = ("GoodsId", "nums")
    GOODSID_FIELD_NUMBER: _ClassVar[int]
    NUMS_FIELD_NUMBER: _ClassVar[int]
    GoodsId: int
    nums: int
    def __init__(self, GoodsId: _Optional[int] = ..., nums: _Optional[int] = ...) -> None: ...

class BatchCategoryInfoRequest(_message.Message):
    __slots__ = ("id", "goodsNums", "brandNums")
    ID_FIELD_NUMBER: _ClassVar[int]
    GOODSNUMS_FIELD_NUMBER: _ClassVar[int]
    BRANDNUMS_FIELD_NUMBER: _ClassVar[int]
    id: _containers.RepeatedScalarFieldContainer[int]
    goodsNums: int
    brandNums: int
    def __init__(self, id: _Optional[_Iterable[int]] = ..., goodsNums: _Optional[int] = ..., brandNums: _Optional[int] = ...) -> None: ...

class GoodsFilterRequest(_message.Message):
    __slots__ = ("priceMin", "priceMax", "isHot", "isNew", "isTab", "topCategory", "pages", "pagePerNums", "keyWords", "brand")
    PRICEMIN_FIELD_NUMBER: _ClassVar[int]
    PRICEMAX_FIELD_NUMBER: _ClassVar[int]
    ISHOT_FIELD_NUMBER: _ClassVar[int]
    ISNEW_FIELD_NUMBER: _ClassVar[int]
    ISTAB_FIELD_NUMBER: _ClassVar[int]
    TOPCATEGORY_FIELD_NUMBER: _ClassVar[int]
    PAGES_FIELD_NUMBER: _ClassVar[int]
    PAGEPERNUMS_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    BRAND_FIELD_NUMBER: _ClassVar[int]
    priceMin: int
    priceMax: int
    isHot: bool
    isNew: bool
    isTab: bool
    topCategory: int
    pages: int
    pagePerNums: int
    keyWords: str
    brand: int
    def __init__(self, priceMin: _Optional[int] = ..., priceMax: _Optional[int] = ..., isHot: bool = ..., isNew: bool = ..., isTab: bool = ..., topCategory: _Optional[int] = ..., pages: _Optional[int] = ..., pagePerNums: _Optional[int] = ..., keyWords: _Optional[str] = ..., brand: _Optional[int] = ...) -> None: ...

class GoodsInfoResponse(_message.Message):
    __slots__ = ("id", "categoryId", "name", "goodsSn", "clickNum", "soldNum", "favNum", "marketPrice", "shopPrice", "goodsBrief", "goodsDesc", "shipFree", "images", "descImages", "goodsFrontImage", "isNew", "isHot", "onSale", "addTime", "category", "brand")
    ID_FIELD_NUMBER: _ClassVar[int]
    CATEGORYID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    GOODSSN_FIELD_NUMBER: _ClassVar[int]
    CLICKNUM_FIELD_NUMBER: _ClassVar[int]
    SOLDNUM_FIELD_NUMBER: _ClassVar[int]
    FAVNUM_FIELD_NUMBER: _ClassVar[int]
    MARKETPRICE_FIELD_NUMBER: _ClassVar[int]
    SHOPPRICE_FIELD_NUMBER: _ClassVar[int]
    GOODSBRIEF_FIELD_NUMBER: _ClassVar[int]
    GOODSDESC_FIELD_NUMBER: _ClassVar[int]
    SHIPFREE_FIELD_NUMBER: _ClassVar[int]
    IMAGES_FIELD_NUMBER: _ClassVar[int]
    DESCIMAGES_FIELD_NUMBER: _ClassVar[int]
    GOODSFRONTIMAGE_FIELD_NUMBER: _ClassVar[int]
    ISNEW_FIELD_NUMBER: _ClassVar[int]
    ISHOT_FIELD_NUMBER: _ClassVar[int]
    ONSALE_FIELD_NUMBER: _ClassVar[int]
    ADDTIME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    BRAND_FIELD_NUMBER: _ClassVar[int]
    id: int
    categoryId: int
    name: str
    goodsSn: str
    clickNum: int
    soldNum: int
    favNum: int
    marketPrice: float
    shopPrice: float
    goodsBrief: str
    goodsDesc: str
    shipFree: bool
    images: _containers.RepeatedScalarFieldContainer[str]
    descImages: _containers.RepeatedScalarFieldContainer[str]
    goodsFrontImage: str
    isNew: bool
    isHot: bool
    onSale: bool
    addTime: int
    category: CategoryBriefInfoResponse
    brand: BrandInfoResponse
    def __init__(self, id: _Optional[int] = ..., categoryId: _Optional[int] = ..., name: _Optional[str] = ..., goodsSn: _Optional[str] = ..., clickNum: _Optional[int] = ..., soldNum: _Optional[int] = ..., favNum: _Optional[int] = ..., marketPrice: _Optional[float] = ..., shopPrice: _Optional[float] = ..., goodsBrief: _Optional[str] = ..., goodsDesc: _Optional[str] = ..., shipFree: bool = ..., images: _Optional[_Iterable[str]] = ..., descImages: _Optional[_Iterable[str]] = ..., goodsFrontImage: _Optional[str] = ..., isNew: bool = ..., isHot: bool = ..., onSale: bool = ..., addTime: _Optional[int] = ..., category: _Optional[_Union[CategoryBriefInfoResponse, _Mapping]] = ..., brand: _Optional[_Union[BrandInfoResponse, _Mapping]] = ...) -> None: ...

class GoodsListResponse(_message.Message):
    __slots__ = ("total", "data")
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    total: int
    data: _containers.RepeatedCompositeFieldContainer[GoodsInfoResponse]
    def __init__(self, total: _Optional[int] = ..., data: _Optional[_Iterable[_Union[GoodsInfoResponse, _Mapping]]] = ...) -> None: ...
