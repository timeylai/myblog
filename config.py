# encoding:utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))


# 类中通用配置
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'shen qi de mi yue'
    # PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 配置一个发送邮箱的邮箱
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USERNAME = '304479519@qq.com'
    # MAIl_PASSWORD = "bcfnjvqlhotybhgg"   # 授权码   # 原因未知，配置环境 email.py 无法获取，只能写在项目的初始化中
    WHOOSH_BASE = os.path.join(basedir, 'whoosh_index')  # 设置索引文件存放文件夹位置

    @staticmethod
    def init_app(app):       # 初始化app
        pass


DIALECT = 'mysql'  # 要用的什么数据库
DRIVER = 'pymysql' # 连接数据库驱动
USERNAME = 'root'  # 用户名
PASSWORD ='timeylai1996'  # 密码
HOST = 'localhost'  # 服务器
PORT ='3306' # 端口
DATABASE = 'mybokedata' # 数据库名


class DevelopmentConfig(Config):    # 开发环境，继承Config模块
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)


class TestingConfig(Config):  # 测试环境 选择测试型mysql
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)


class ProductionConFig(Config):  # 生产环境， 连接正式mysql
    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                           PORT, DATABASE)


Config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConFig,
    'default': DevelopmentConfig
}