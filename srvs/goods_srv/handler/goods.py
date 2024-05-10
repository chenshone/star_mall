import json
import grpc
from loguru import logger
from goods_srv.proto import goods_pb2, goods_pb2_grpc
from goods_srv.model.models import Banner, Brands, Category, Goods, GoodsCategoryBrand
from google.protobuf import empty_pb2

import peewee


class GoodsServicer(goods_pb2_grpc.GoodsServicer):
    def category_model_to_dict(self, category):
        re = {}

        re["id"] = category.id
        re["name"] = category.name
        re["level"] = category.level
        re["parent"] = category.parent_category_id
        re["is_tab"] = category.is_tab

        return re

    def convert_model_to_message(self, goods):
        info_resp = goods_pb2.GoodsInfoResponse()

        info_resp.id = goods.id
        info_resp.categoryId = goods.category_id
        info_resp.name = goods.name
        info_resp.goodsSn = goods.goods_sn
        info_resp.clickNum = goods.click_num
        info_resp.soldNum = goods.sold_num
        info_resp.favNum = goods.fav_num
        info_resp.marketPrice = goods.market_price
        info_resp.shopPrice = goods.shop_price
        info_resp.goodsBrief = goods.goods_brief
        info_resp.shipFree = goods.ship_free
        info_resp.goodsFrontImage = goods.goods_front_image
        info_resp.isNew = goods.is_new
        info_resp.descImages.extend(goods.desc_images)
        info_resp.images.extend(goods.desc_images)
        info_resp.isHot = goods.is_hot
        info_resp.onSale = goods.on_sale

        info_resp.category.id = goods.category.id
        info_resp.category.name = goods.category.name

        info_resp.brand.id = goods.brand.id
        info_resp.brand.name = goods.brand.name
        info_resp.brand.logo = goods.brand.logo

        return info_resp

    @logger.catch
    def GoodsList(self, request, context):
        """商品列表页"""
        resp = goods_pb2.GoodsListResponse()

        goods = Goods.select()
        if request.keyWords:
            goods = goods.filter(Goods.name.contains(request.keyWords))
        if request.isHot:
            goods = goods.filter(Goods.is_hot == True)
        if request.isNew:
            goods = goods.filter(Goods.is_new == True)
        if request.priceMin:
            goods = goods.filter(Goods.shop_price >= request.priceMin)
        if request.priceMax:
            goods = goods.filter(Goods.shop_price <= request.priceMax)
        if request.brand:
            goods = goods.filter(Goods.brand_id == request.brand)
        if request.topCategory:
            # 通过category来查询商品， 这个category可能是一级、二级或者三级分类
            try:
                ids = []
                category = Category.get(Category.id == request.topCategory)
                level = category.level

                if level == 1:
                    c2 = Category.alias()
                    categories = Category.select(Category.id).where(
                        Category.parent_category_id.in_(
                            c2.select(c2.id).where(
                                c2.parent_category_id == request.topCategory
                            )
                        )
                    )
                    for category in categories:
                        ids.append(category.id)
                elif level == 2:
                    categories = Category.select(Category.id).where(
                        Category.parent_category_id == request.topCategory
                    )
                    for category in categories:
                        ids.append(category.id)
                elif level == 3:
                    ids.append(request.topCategory)

                goods = goods.where(Goods.category_id.in_(ids))

            except Exception as e:
                pass
        # 分页
        start, per_page_nums = 0, 10
        if request.pagePerNums:
            per_page_nums = request.pagePerNums
        if request.pages:
            start = per_page_nums * (request.pages - 1)

        goods = goods.limit(per_page_nums).offset(start)

        resp.total = goods.count()

        for good in goods:
            resp.data.append(self.convert_model_to_message(good))

        return resp

    @logger.catch
    def BatchGetGoods(self, request: goods_pb2.BatchGoodsIdInfo, context):
        """现在用户提交订单有多个商品，批量查询商品的信息
        批量获取商品信息
        """
        resp = goods_pb2.GoodsListResponse()

        goods = Goods.select().where(Goods.id.in_(list(request.id)))

        resp.total = goods.count()

        for good in goods:
            resp.data.append(self.convert_model_to_message(good))

        return resp

    @logger.catch
    def DeleteGoods(
        self, request: goods_pb2.DeleteGoodsInfo, context: grpc.ServicerContext
    ):
        try:
            goods = Goods.get(Goods.id == request.id)
            goods.delete_instance()
        except peewee.DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("商品不存在")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
        finally:
            return empty_pb2.Empty()

    @logger.catch
    def GetGoodsDetail(
        self, request: goods_pb2.GoodInfoRequest, context: grpc.ServicerContext
    ):
        # 获取商品的详情
        try:
            goods = Goods.get(Goods.id == request.id)

            # 每次请求增加click_num
            goods.click_num += 1
            goods.save()

            return self.convert_model_to_message(goods)
        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return goods_pb2.GoodsInfoResponse()

    @logger.catch
    def CreateGoods(self, request: goods_pb2.CreateGoodsInfo, context):
        # 新建商品
        try:
            category = Category.get(Category.id == request.categoryId)
        except peewee.DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("商品分类不存在")
            return goods_pb2.GoodsInfoResponse()

        try:
            brand = Brands.get(Brands.id == request.brandId)
        except peewee.DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("品牌不存在")
            return goods_pb2.GoodsInfoResponse()

        goods = Goods()
        goods.brand = brand
        goods.category = category
        goods.name = request.name
        goods.goods_sn = request.goodsSn
        goods.market_price = request.marketPrice
        goods.shop_price = request.shopPrice
        goods.goods_brief = request.goodsBrief
        goods.ship_free = request.shipFree
        goods.images = list(request.images)
        goods.desc_images = list(request.descImages)
        goods.goods_front_image = request.goodsFrontImage
        goods.is_new = request.isNew
        goods.is_hot = request.isHot
        goods.on_sale = request.onSale

        goods.save()

        # TODO 此处完善库存的设置 - 分布式事务
        return self.convert_model_to_message(goods)

    @logger.catch
    def UpdateGoods(self, request: goods_pb2.CreateGoodsInfo, context):
        # 商品更新
        try:
            category = Category.get(Category.id == request.categoryId)
        except peewee.DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("商品分类不存在")
            return goods_pb2.GoodsInfoResponse()

        try:
            brand = Brands.get(Brands.id == request.brandId)
        except peewee.DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("品牌不存在")
            return goods_pb2.GoodsInfoResponse()

        try:
            goods = Goods.get(Goods.id == request.id)
        except peewee.DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("商品不存在")
            return goods_pb2.GoodsInfoResponse()

        goods.brand = brand
        goods.category = category
        goods.name = request.name
        goods.goods_sn = request.goodsSn
        goods.market_price = request.marketPrice
        goods.shop_price = request.shopPrice
        goods.goods_brief = request.goodsBrief
        goods.ship_free = request.shipFree
        goods.images = list(request.images)
        goods.desc_images = list(request.descImages)
        goods.goods_front_image = request.goodsFrontImage
        goods.is_new = request.isNew
        goods.is_hot = request.isHot
        goods.on_sale = request.onSale

        goods.save()

        # TODO 此处完善库存的设置 - 分布式事务
        return self.convert_model_to_message(goods)

    @logger.catch
    def GetAllCategorysList(self, request: empty_pb2.Empty, context):
        # 商品的分类
        """
        [{ // 一级分类
            "name":"xxx",
            "id":xxx,
            "sub_category":[
                { // 二级分类
                    "id":xxx,
                    "name":"xxx”,
                    “sub_category”:[
                    ]
                }
            ]
        },{}, {}, {}]
        """
        level1 = []
        level2 = []
        level3 = []

        category_list_resp = goods_pb2.CategoryListResponse()

        category_list_resp.total = Category.select().count()

        for category in Category.select():
            category_resp = goods_pb2.CategoryInfoResponse()

            category_resp.id = category.id
            category_resp.name = category.name
            if category.parent_category_id:
                category_resp.parentCategory = category.parent_category_id
            category_resp.level = category.level
            category_resp.isTab = category.is_tab

            category_list_resp.data.append(category_resp)

            if category.level == 1:
                level1.append(self.category_model_to_dict(category))
            elif category.level == 2:
                level2.append(self.category_model_to_dict(category))
            elif category.level == 3:
                level3.append(self.category_model_to_dict(category))

        # 开始整理
        for data3 in level3:
            for data2 in level2:
                if data3["parent"] == data2["id"]:
                    if "sub_category" not in data2:
                        data2["sub_category"] = [data3]
                    else:
                        data2["sub_category"].append(data3)

        for data2 in level2:
            for data1 in level1:
                if data2["parent"] == data1["id"]:
                    if "sub_category" not in data1:
                        data1["sub_category"] = [data2]
                    else:
                        data1["sub_category"].append(data2)

        category_list_resp.jsonData = json.dumps(level1)
        return category_list_resp

    @logger.catch
    def GetSubCategory(self, request: goods_pb2.CategoryListRequest, context):
        category_list_resp = goods_pb2.SubCategoryListResponse()

        try:
            category_info = Category.get(Category.id == request.id)
            category_list_resp.info.id = category_info.id
            category_list_resp.info.name = category_info.name
            category_list_resp.info.level = category_info.level
            category_list_resp.info.isTab = category_info.is_tab
            if category_info.parent_category:
                category_list_resp.info.parentCategory = (
                    category_info.parent_category_id
                )
        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return goods_pb2.SubCategoryListResponse()

        categories = Category.select().where(Category.parent_category == request.id)
        category_list_resp.total = categories.count()
        for category in categories:
            category_resp = goods_pb2.CategoryInfoResponse()
            category_resp.id = category.id
            category_resp.name = category.name
            if category_info.parent_category:
                category_resp.parentCategory = category_info.parent_category_id
            category_resp.level = category.level
            category_resp.isTab = category.is_tab

            category_list_resp.subCategorys.append(category_resp)

        return category_list_resp

    @logger.catch
    def CreateCategory(self, request: goods_pb2.CategoryInfoRequest, context):
        try:
            category = Category()
            category.name = request.name
            if request.level != 1:
                category.parent_category = request.parentCategory
            category.level = request.level
            category.is_tab = request.isTab
            category.save()

            category_resp = goods_pb2.CategoryInfoResponse()
            category_resp.id = category.id
            category_resp.name = category.name
            if category.parent_category:
                category_resp.parentCategory = category.parent_category.id
            category_resp.level = category.level
            category_resp.isTab = category.is_tab
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("创建类别失败: " + str(e))
            return goods_pb2.CategoryInfoResponse()

        return category_resp

    @logger.catch
    def DeleteCategory(self, request: goods_pb2.DeleteCategoryRequest, context):
        try:
            category = Category.get(request.id)
            category.delete_instance()

            # TODO 删除响应的category下的商品

        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
        finally:
            return empty_pb2.Empty()

    @logger.catch
    def UpdateCategory(self, request: goods_pb2.CategoryInfoRequest, context):
        try:
            category = Category.get(request.id)
            if request.name:
                category.name = request.name
            if request.parentCategory:
                category.parent_category = request.parentCategory
            if request.level:
                category.level = request.level
            if request.isTab:
                category.is_tab = request.isTab
            category.save()

        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
        finally:
            return empty_pb2.Empty()

    ##轮播图
    @logger.catch
    def BannerList(self, request: empty_pb2.Empty, context):
        # 获取分类列表
        resp = goods_pb2.BannerListResponse()
        banners = Banner.select()

        resp.total = banners.count()
        for banner in banners:
            banner_resp = goods_pb2.BannerResponse()

            banner_resp.id = banner.id
            banner_resp.image = banner.image
            banner_resp.index = banner.index
            banner_resp.url = banner.url

            resp.data.append(banner_resp)

        return resp

    @logger.catch
    def CreateBanner(self, request: goods_pb2.BannerRequest, context):
        banner = Banner()

        banner.image = request.image
        banner.index = request.index
        banner.url = request.url
        banner.save()

        banner_resp = goods_pb2.BannerResponse()
        banner_resp.id = banner.id
        banner_resp.image = banner.image
        banner_resp.url = banner.url

        return banner_resp

    @logger.catch
    def DeleteBanner(self, request: goods_pb2.BannerRequest, context):
        try:
            banner = Banner.get(request.id)
            banner.delete_instance()

        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
        finally:
            return empty_pb2.Empty()

    @logger.catch
    def UpdateBanner(self, request: goods_pb2.BannerRequest, context):
        try:
            banner = Banner.get(request.id)
            if request.image:
                banner.image = request.image
            if request.index:
                banner.index = request.index
            if request.url:
                banner.url = request.url

            banner.save()

        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
        finally:
            return empty_pb2.Empty()

    # 品牌相关的接口

    @logger.catch
    def BrandList(self, request: empty_pb2.Empty, context):
        # 获取品牌列表
        resp = goods_pb2.BrandListResponse()
        brands = Brands.select()

        resp.total = brands.count()
        for brand in brands:
            brand_resp = goods_pb2.BrandInfoResponse()

            brand_resp.id = brand.id
            brand_resp.name = brand.name
            brand_resp.logo = brand.logo

            resp.data.append(brand_resp)

        return resp

    @logger.catch
    def CreateBrand(self, request: goods_pb2.BrandRequest, context):
        brands = Brands.select().where(Brands.name == request.name)
        if brands:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("记录已经存在")
            return goods_pb2.BrandInfoResponse()

        brand = Brands()

        brand.name = request.name
        brand.logo = request.logo

        brand.save()

        resp = goods_pb2.BrandInfoResponse()
        resp.id = brand.id
        resp.name = brand.name
        resp.logo = brand.logo

        return resp

    @logger.catch
    def DeleteBrand(self, request: goods_pb2.BrandRequest, context):
        try:
            brand = Brands.get(request.id)
            brand.delete_instance()

        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
        finally:
            return empty_pb2.Empty()

    @logger.catch
    def UpdateBrand(self, request: goods_pb2.BrandRequest, context):
        try:
            brand = Brands.get(request.id)
            if request.name:
                brand.name = request.name
            if request.logo:
                brand.logo = request.logo

            brand.save()

        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
        finally:
            return empty_pb2.Empty()

    @logger.catch
    def CategoryBrandList(self, request: empty_pb2.Empty, context):
        # 获取品牌分类列表
        resp = goods_pb2.CategoryBrandListResponse()
        category_brands = GoodsCategoryBrand.select()

        # 分页
        start = 0
        per_page_nums = 10
        if request.pagePerNums:
            per_page_nums = request.PagePerNums
        if request.pages:
            start = per_page_nums * (request.pages - 1)

        category_brands = category_brands.limit(per_page_nums).offset(start)

        resp.total = category_brands.count()
        for category_brand in category_brands:
            category_brand_resp = goods_pb2.CategoryBrandResponse()

            category_brand_resp.id = category_brand.id
            category_brand_resp.brand.id = category_brand.brand.id
            category_brand_resp.brand.name = category_brand.brand.name
            category_brand_resp.brand.logo = category_brand.brand.logo

            category_brand_resp.category.id = category_brand.category.id
            category_brand_resp.category.name = category_brand.category.name
            category_brand_resp.category.parentCategory = (
                category_brand.category.parent_category_id
            )
            category_brand_resp.category.level = category_brand.category.level
            category_brand_resp.category.isTab = category_brand.category.is_tab

            resp.data.append(category_brand_resp)
        return resp

    @logger.catch
    def GetCategoryBrandList(self, request, context):
        # 获取某一个分类的所有品牌
        resp = goods_pb2.BrandListResponse()
        try:
            category = Category.get(Category.id == request.id)
            category_brands = GoodsCategoryBrand.select().where(
                GoodsCategoryBrand.category == category
            )
            resp.total = category_brands.count()
            for category_brand in category_brands:
                brand_resp = goods_pb2.BrandInfoResponse()
                brand_resp.id = category_brand.brand.id
                brand_resp.name = category_brand.brand.name
                brand_resp.logo = category_brand.brand.logo

                resp.data.append(brand_resp)
        except peewee.DoesNotExist as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return resp

        return resp

    @logger.catch
    def CreateCategoryBrand(self, request: goods_pb2.CategoryBrandRequest, context):
        category_brand = GoodsCategoryBrand()

        try:
            brand = Brands.get(request.brandId)
            category_brand.brand = brand
            category = Category.get(request.categoryId)
            category_brand.category = category
            category_brand.save()

            resp = goods_pb2.CategoryBrandResponse()
            # 只返回id, 因为create的时候brand和category的信息前端都知道
            resp.id = category_brand.id

            return resp
        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
            return goods_pb2.CategoryBrandResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("内部错误")
            return goods_pb2.CategoryBrandResponse()

    @logger.catch
    def DeleteCategoryBrand(self, request: goods_pb2.CategoryBrandRequest, context):
        try:
            category_brand = GoodsCategoryBrand.get(request.id)
            category_brand.delete_instance()

        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
        finally:
            return empty_pb2.Empty()

    @logger.catch
    def UpdateCategoryBrand(self, request: goods_pb2.CategoryBrandRequest, context):
        try:
            category_brand = GoodsCategoryBrand.get(request.id)
            brand = Brands.get(request.brandId)
            category_brand.brand = brand
            category = Category.get(request.categoryId)
            category_brand.category = category
            category_brand.save()

        except peewee.DoesNotExist:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("记录不存在")
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("内部错误")
        finally:
            return empty_pb2.Empty()
