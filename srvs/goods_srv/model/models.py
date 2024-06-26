from datetime import datetime
from peewee import *

from playhouse.mysql_ext import JSONField

# import sys
# import os

# # 获取当前文件的父目录路径
# current_dir = os.path.dirname(os.path.abspath(__file__))
# # 获取项目根目录路径（假设为父目录的父目录）
# project_root = os.path.dirname(os.path.dirname(current_dir))
# # 将项目根目录添加到模块搜索路径
# sys.path.append(project_root)

from goods_srv.settings import settings


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    is_deleted = BooleanField(default=False, verbose_name="是否删除")  # 逻辑删除
    update_time = DateTimeField(verbose_name="更新时间", default=datetime.now)

    def save(self, *args, **kwargs):
        # 判断这是一个新添加的数据还是更新的数据
        # self._pk 表示 primary key
        if self._pk is not None:
            # 这是一条已存在的数据
            self.update_time = datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def delete(cls, permanently=False):  # permanently表示是否永久删除
        if permanently:
            return super().delete()
        else:
            return super().update(is_deleted=True)

    def delete_instance(
        self, permanently=False, recursive=False, delete_nullable=False
    ):
        if permanently:
            return self.delete(permanently).where(self._pk_expr()).execute()
        else:
            self.is_deleted = True
            self.save()

    @classmethod
    def select(cls, *fields):
        return super().select(*fields).where(cls.is_deleted == False)

    class Meta:
        database = settings.DB


class Category(BaseModel):
    name = CharField(max_length=20, verbose_name="名称")
    parent_category = ForeignKeyField(
        "self", verbose_name="父类别", null=True
    )  # 一级类别可以没有父类别
    level = IntegerField(default=1, verbose_name="级别")
    is_tab = BooleanField(default=False, verbose_name="是否显示在首页tab")


class Brands(BaseModel):
    # 品牌
    name = CharField(max_length=50, verbose_name="名称", index=True, unique=True)
    logo = CharField(max_length=200, null=True, verbose_name="图标", default="")


class Goods(BaseModel):
    # 商品
    category = ForeignKeyField(Category, verbose_name="商品类目", on_delete="CASCADE")
    brand = ForeignKeyField(Brands, verbose_name="品牌", on_delete="CASCADE")
    on_sale = BooleanField(default=True, verbose_name="是否上架")
    goods_sn = CharField(
        max_length=50, default="", verbose_name="商品唯一货号, 后台系统使用"
    )
    name = CharField(max_length=100, verbose_name="商品名")
    click_num = IntegerField(default=0, verbose_name="点击数")
    sold_num = IntegerField(default=0, verbose_name="商品销售量")
    fav_num = IntegerField(default=0, verbose_name="收藏数")
    # stocks = IntegerField(default=0, verbose_name="库存数") 库存数使用分布式微服务
    market_price = FloatField(default=0, verbose_name="市场价格")
    shop_price = FloatField(default=0, verbose_name="本店价格")
    goods_brief = CharField(max_length=200, verbose_name="商品简短描述")
    ship_free = BooleanField(default=True, verbose_name="是否承担运费")
    images = JSONField(verbose_name="商品轮播图")
    desc_images = JSONField(verbose_name="详情页图片")
    goods_front_image = CharField(max_length=200, verbose_name="封面图")
    is_new = BooleanField(default=False, verbose_name="是否新品")
    is_hot = BooleanField(default=False, verbose_name="是否热销")


class GoodsCategoryBrand(BaseModel):
    # 品牌分类
    id = AutoField(primary_key=True, verbose_name="id")
    category = ForeignKeyField(Category, verbose_name="类别")
    brand = ForeignKeyField(Brands, verbose_name="品牌")

    class Meta:
        indexes = (
            # 联合主键
            (("category", "brand"), True),
        )


class Banner(BaseModel):
    """
    轮播的商品
    """

    image = CharField(max_length=200, default="", verbose_name="图片url")
    url = CharField(max_length=200, default="", verbose_name="访问url")
    index = IntegerField(default=0, verbose_name="轮播顺序")


if __name__ == "__main__":
    pass
    # settings.DB.create_tables([Category, Brands, Goods, GoodsCategoryBrand, Banner])
    # c1 = Category(name="bobby1", level=1)
    # c2 = Category(name="bobby2", level=1)
    # c1.save()
    # c2.save()
    # for c in Category.select():
    #     print(c.name, c.id)
    # c1 = Category.get(Category.id == 1)
    # c1.delete_instance()
    # Category.delete(permanently=True).where(Category.id == 2).execute()
