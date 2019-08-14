# -*- coding: UTF-8 -*-
from flask import current_app, app
from . import db
import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from .extensions import login_manager
from werkzeug.security import check_password_hash  # 导入hash 加密包
from flask_login import UserMixin   # 引用包方便login调用*
from jieba.analyse.analyzer import ChineseAnalyzer


class User(UserMixin, db.Model):    # 继承UserMixin类
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)   # 主键
    username = db.Column(db.String(128), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    is_super = db.Column(db.Boolean, default=False)  # 辨认是否为admin
    is_activate = db.Column(db.Boolean, default=False)  # 账号是否激活
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    # 个性签名
    autograph = db.Column(db.String(256))
    # 设置默认头像
    icon = db.Column(db.String(70), default='default.jpg')
    pages = db.relationship('PageInfo', backref='user')  # 建立与外键联系的关系
    page_draft = db.relationship('PageDraft', backref='user')
    icon_life_debunk = db.relationship('LifeDebunk', backref='user')

    @property  # 明文只读
    def password(self):
        raise ArithmeticError(u'文明密码不可读')

    '''# 转为hash存入数
    def password(self, value):  # *变量及返回值

        self.password_hash = generate_password_hash(value)
    '''

    # 随机生成token, 一小时后过期
    def generate_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)  # dict {'':''}
        return s.dumps({'id': self.id})  # dict 转成 str {"":""}
    # 验证token的模块 ,login views 调用

    @staticmethod  # 静态方法
    def check_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']  # {u''}
        except KeyError:
            return False
        u = User.query.get(id)
        if u == '':
            return False
        if not u.is_activate:  # 判断is_activate ，更新激活状态
            u.is_activate = True
            db.session.commit()  # 更新数据提交
        return True  # 返回TRUE views 判断

    # 验证hash密码是否一致  return 0 ,1
    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)  # (密码，文明码)

    # 后台显示用户名
    def __repr__(self):
        return '<User %r>' % self.username


# 返回数据    *与前端的current_user调用 ，返回user_id
# 这个回调用于从会话中存储的用户 ID 重新加载用户对象。 它应该接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象。
@login_manager.user_loader   # 指定登陆route
def loader_user(user_id):
    return User.query.get(int(user_id))


class PageInfo(db.Model):
    __tablename__ = 'pages'
    __searchable__ = ['title', 'content']
    __analyzer__ = ChineseAnalyzer()
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.Unicode(100))
    content = db.Column(db.TEXT)
    content_see = db.Column(db.Integer)
    content_good = db.Column(db.Integer)
    content_time = db.Column(db.DateTime, default=datetime.datetime.now())
    content_img = db.Column(db.String(256))
    content_keyword = db.Column(db.String(256))
    content_type = db.Column(db.String(64), default='other')
    is_public = db.Column(db.Boolean, default=False)  # 是否公布
    is_admin_good = db.Column(db.Boolean, default=False)  # 推荐
    page_id = db.Column(db.String(13), index=True)  # 这个id是文章路由，随机生成的
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    page_keyword = db.relationship('PageKeyWord', backref='pages')   # 建立关系
    page_guest_book = db.relationship('GuestBook', backref='pages')  # GuestBook 与 page表建立关系

    def __repr__(self):
        return '<PageInfo %r>' % self.title


class GuestBook(db.Model):
    __tablename__ = 'pages_guest_book'  # 文章的留言板记录
    id = db.Column(db.Integer, primary_key=True, index=True)
    guest_content = db.Column(db.String(450))   # 140字内
    guest_user = db.Column(db.String(64))  # 留言用户名，默认类型 一楼 二楼、、
    guest_time = db.Column(db.DateTime, default=datetime.datetime.now())
    page_id = db.Column(db.String(13), db.ForeignKey('pages.page_id'), index=True)

    @staticmethod   # 登陆状态就返回用户名，否则返回游客
    def guest_username(username):
        if not username:
            return '游客'
        else:
            return username


class PageKeyWord(db.Model):
    __tablename__ = 'page_keyword'
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(256))
    content_keyword = db.Column(db.String(256))
    page_id = db.Column(db.String(13), db.ForeignKey('pages.page_id'))


class PageDraft(db.Model):
    __tablename__ = 'page_draft'
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(100))
    content = db.Column(db.TEXT(0))
    page_id = db.Column(db.String(13), index=True)  # 这个id是文章路由，随机生成的
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 增加一个外键，是user表的id


class Bookmarking(db.Model):
    __tablename__ = 'web_marking'
    id = db.Column(db.Integer, primary_key=True, index=True)  # 主键
    web_name = db.Column(db.String(100))
    web_introduction = db.Column(db.String(258))
    web_url = db.Column(db.String(100), index=True)
    web_logo = db.Column(db.String(100))
    web_type = db.Column(db.String(64))


class LifeDebunk(db.Model):
    """ team life 消息发送表"""
    __tablename__ = 'TeamDebunk_message'
    id = db.Column(db.Integer, primary_key=True, index=True)
    icon = db.Column(db.String(256), db.ForeignKey('user.autograph'))  # 头像
    DebunkContent = db.Column(db.TEXT(),)  # 黑洞内容
    DebunkTime = db.Column(db.DateTime, default=datetime.datetime.now())
    DebunkID = db.Column(db.String(13),)


class LifeDebunkReply(db.Model):
    """ """


class LeavingWord(db.Model):
    __tablename__ = 'web_leave'  # 网站留言板数据
    id = db.Column(db.Integer, primary_key=True, index=True)  # 主键
    LeavingName = db.Column(db.String(30))
    LeavingWord = db.Column(db.String(500))
    LeavingTime = db.Column(db.DateTime, default=datetime.datetime.now())
    LeavingContact = db.Column(db.String(64))
    LeavingReply = db.Column(db.String(500))


class WorkplaceBookCollect(db.Model):
    __tablename__ = 'book_collect'  # 前沿技术记录表
    id = db.Column(db.Integer, primary_key=True, index=True)  # 主键
    book_name = db.Column(db.String(120))
    book_introduce = db.Column(db.TEXT(0))  # 书籍文章内容感想，推荐
    book_recommend_time = db.Column(db.DateTime, default=datetime.datetime.now())
    book_introduce_count = db.Column(db.Integer)

