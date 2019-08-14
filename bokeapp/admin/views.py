# -*- coding: utf-8 -*-
# @Time    : 2019/5/22 19:19
# @Author  : timeylai
# @Site    : 
# @File    : views.py
# @Software: PyCharm


from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from bokeapp import create_app

admin = Admin()


def create_admin(app):  # 实例化flask_admin, 方法引入_init_
    admin.init_app(app)



