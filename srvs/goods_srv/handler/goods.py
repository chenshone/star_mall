from loguru import logger
from goods_srv.proto import goods_pb2, goods_pb2_grpc
from goods_srv.model.models import Category, Goods


class GoodsServicer(goods_pb2_grpc.GoodsServicer):
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
