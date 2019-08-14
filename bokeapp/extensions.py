# -*- coding: UTF-8 -*-
"""
author: timey
exctension 拓展包引用到bokeapp

"""
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
import flask_whooshalchemyplus as wh

#   由于尚未初始化所需的程序实例，所以没有初始化扩展，创建扩展类时没有向构造函数传入参数。
bootstrap = Bootstrap()  #
login_manager = LoginManager()
mail = Mail()


def extension_config(app):  # 实例化接口
    bootstrap.init_app(app)
    login_manager.init_app(app=app)
    mail.init_app(app)
    # admin.init_app(app)
    wh.init_app(app)

    login_manager.login_view = 'main.login'   # 视图未授权跳转路由
    login_manager.login_message = '请先登陆后在访问'
    login_manager.session_protection = 'strong'
