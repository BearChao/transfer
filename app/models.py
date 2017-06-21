# -*- coding: utf-8 -*-

from peewee import  Model, CharField, BooleanField, IntegerField
import json
from playhouse.sqlite_ext import SqliteExtDatabase
from werkzeug.security import check_password_hash
from flask_login import UserMixin
from app import login_manager
from conf.config import config
import os

cfg = config[os.getenv('FLASK_CONFIG') or 'default']

db = SqliteExtDatabase('conf/config.db')


class BaseModel(Model):
    class Meta:
        database = db

    def __str__(self):
        r = {}
        for k in self._data.keys():
            try:
                r[k] = str(getattr(self, k))
            except:
                r[k] = json.dumps(getattr(self, k))
        # return str(r)
        return json.dumps(r, ensure_ascii=False)


# 管理员工号
class User(UserMixin, BaseModel):
    username = CharField()  # 用户名
    password = CharField()  # 密码
    fullname = CharField()  # 真实性名
    email = CharField()  # 邮箱
    phone = CharField()  # 电话
    status = BooleanField(default=True)  # 生效失效标识

    def verify_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

#配置文件
class Task(BaseModel):
    finger = IntegerField() #任务编号
    name = CharField()  #任务名称
    dataType = IntegerField() #任务类型
    dir = CharField() #文件目录或者host地址
    username = CharField() #用户名
    password = CharField() #密码
    target = CharField() #目标文件夹或者数据库名
    port = CharField() #端口号
    tables = CharField() #数据表，空格间隔

@login_manager.user_loader
def load_user(user_id):
    return User.get(User.id == int(user_id))

# 建表
def create_table():
    db.connect()
    db.create_tables([User, Task])


if __name__ == '__main__':
    create_table()
