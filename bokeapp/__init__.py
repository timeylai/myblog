'''
author: timey
应用拓展实例化
'''
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
# 导入实例化拓展应用
from .extensions import extension_config
import os
from config import Config


db = SQLAlchemy()  # db数据库不放在拓展功能


def create_app(config_name):   # 初始化app调用情况
    app = Flask(__name__)
    app.config['MAIL_PASSWORD'] = 'bcfnjvqlhotybhgg'  # 邮箱授权码
    app.config.from_object(Config[config_name])
    Config[config_name].init_app(app)   # init_app 方法调用
    db.init_app(app)
    extension_config(app)  # 所有拓展应用

    from .auth import auth as auth_blueprint     #
    from .main import main as main_blueprint     # 单个蓝图导入app下的main蓝图
    from .admin import admin as admin_blueprint    # 单个蓝图导入
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)
    return app



