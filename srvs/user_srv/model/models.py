from peewee import *

from user_srv.settings import settings


class BaseModel(Model):
    class Meta:
        database = settings.DB


# 用户模型
class User(BaseModel):
    GENDER_CHOICES = (
        ("female", "女"),
        ("male", "男")
    )

    ROLE_CHOICES = (
        (1, "普通用户"),
        (2, "管理员")
    )

    mobile = CharField(max_length=11, index=True, unique=True, verbose_name="手机号码")
    password = CharField(max_length=128, verbose_name="密码")  # 密文，不可反解
    nickname = CharField(max_length=20, null=True, verbose_name="昵称")
    avatar = CharField(max_length=255, null=True, verbose_name="头像")
    birthday = DateField(null=True, verbose_name="生日")
    address = CharField(max_length=255, null=True, verbose_name="地址")
    desc = TextField(null=True, verbose_name="个人简介")
    gender = CharField(max_length=6, choices=GENDER_CHOICES, null=True, verbose_name="性别")
    role = IntegerField(default=1, choices=ROLE_CHOICES, verbose_name="用户角色")


if __name__ == '__main__':
    settings.DB.create_tables([User])

    from passlib.hash import pbkdf2_sha256

    for i in range(10):
        user = User()
        user.mobile = f"138000000{i}"
        user.password = pbkdf2_sha256.hash("admin123")
        user.nickname = f"nickname{i}"
        user.save()
