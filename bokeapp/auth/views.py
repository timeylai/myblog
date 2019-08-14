# -*- coding: utf-8 -*-

"""
    author: timey
    功能： 用户登录后的操作
          功能1 写文章，管理文章页面，。
"""
import os
import re
import random
import json
from flask import render_template, redirect, url_for, request
from bokeapp.auth import auth
from bokeapp.auth.forms import SettingForm, WriteForm
from bokeapp.models import User, PageInfo, PageKeyWord
from bokeapp import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, current_user  # 视图权限访问限制
import datetime
import flask_whooshalchemyplus
import jieba
import jieba.analyse
from config import Config


@auth.route('/information')
@login_required
def user_info():
    """用户路由传参"""
    user1 = current_user.username
    return redirect(url_for('auth.user_manage', user=user1))


@auth.route('/<user>/manage')
@login_required
def user_manage(user):
    """用户文章及信息管理页"""
    user_id = current_user.id
    page_all = PageInfo.query.filter_by(user_id=user_id)
    return render_template('user/user_manage.html', user=user, page=page_all)   # * 参数必须要 =


@auth.route('/<user>/p/<page_id>')
def user_show_page(user, page_id):
    """user page to main page show """
    return redirect(url_for('main.page_url', user=user, page_id=page_id))


'''
@auth.route('/setting', methods=['GET', 'POST'])
def setting_password():
    username = request.cookies.get("username")  # 获取登陆当前用户名
    # password = request.cookies.get("password")   # 获取的应该是hash文码
    if username:
        form = SettingForm()
        user = User.query.filter_by(username).first()
        if user.check_password_hash(form.password.data):  # 判断原密码是否正确
            user.password_hash = generate_password_hash(form.new_password.data)
            db.session.commit()
            flash('密码更改成功,请重新登陆')
            return redirect(url_for('main.login'))
    else:
        flash('请先登陆')
        return render_template('user/login.html')


@auth.route('/autograph', methods=['GET', 'POST'])
def setting_info():
    username = request.cookies.get('username')
    if username:
        new_autograph = request.form.get('autograph')  # js中获取个性签名,js代写
        if new_autograph != '':
            user = User.query.filter_by(username).first()
            user.autograph = new_autograph
            db.session.commit()
        return redirect(url_for('auth.username_info', name=username))   # 返回一个参数到路由
    return render_template('main/index.html')
'''


def get_page_id():
    """ get random number to sign page url """
    temp_id = str(random.randrange(10000, 99999))
    time_id = datetime.datetime.now().strftime(u'%d%H%M%S')
    page_id = '%s%s' % (time_id, temp_id)
    return page_id


@auth.route('/write', methods=['GET', 'POST'])
@login_required
def write_page():
    """ save to mysql  文章表单保存到mysql """
    form = WriteForm()
    if request.method == "GET":
        return render_template('user/write.html', form=form)
    if request.method == "POST":
        page_id = get_page_id()
        if form.title.data != "" or form.body.data != "":
            content_temp = form.body.data
            r = 'src="(.+?.(?:bmp|jpg|png|gif))"'   # 正则表达式，获取第一张图片路径
            temp = "" if not re.findall(r, content_temp) else re.findall(r, content_temp)[0]
            keyword = ','.join(get_page_key(content_temp))    # 转化str  list  Mysql not save
            page = PageInfo(title=form.title.data, content=form.body.data, content_see=0,
                            content_good=0, is_public=False, user_id=current_user.id,
                            content_img=temp, page_id=page_id)
            db.session.add(page), db.session.commit()
            flask_whooshalchemyplus.index_one_model(PageInfo)  # 增加文章就加入索引index
            key = PageKeyWord(title=form.title.data, content_keyword=keyword,
                              page_id=page_id)
            db.session.add(key), db.session.commit()
            return redirect(url_for('auth.user_manage', user=current_user.username))
    else:
        return render_template('user/write.html', msg="文章或标题不能为空")


def get_page_key(page):
    """ 结巴分词，产生关键词，需要优化"""
    keywords = jieba.analyse.extract_tags(sentence=page, topK=20,
                                          withWeight=False, allowPOS=('n', 'nr', 'ns'))
    # print(keywords)
    return keywords


def upload_file():
    """str(random.randrange(1, 10))随机函数,  get a some filename"""
    username = current_user.username  # 获取当前登录user信息
    user_id = current_user.id
    filename_prefix = datetime.datetime.now().strftime(u'%Y%m%d%H%M%S')
    temp = '%s%s|%s' % (user_id, username, filename_prefix)
    return temp


@auth.route('/ck_upload', methods=['GET', 'POST'])
@login_required
def ck_upload():
    """ CKEditor file upload ,编辑器图片上传"""
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    error = ''
    url = ''
    # callback = request.args.get('CKEditorFunNum')
    if request.method == 'POST':
        up_file = request.files['upload']    # * get('upload')  filename 看data的参数
        f_name, extensions = os.path.splitext(up_file)  # 分割名字，后缀
        temp = upload_file().split('|')[0]   # get id_user str
        r_name = '%s%s' % (upload_file().split('|')[1], extensions)  # 重定义文件命名
        file_path = os.path.join(basedir, 'static\\uploads', temp, r_name)   # get 路径 有文件名及后缀
        dirname = os.path.dirname(file_path)    # 上一级路径
        if not os.path.exists(dirname):  # 判断路径 uploads 文件夹是否存在
            try:
                os.mkdir(dirname)
            except:
                error = '创建uploads文件夹失败'
        elif not os.access(dirname, os.W_OK):  # 判断是否有读写权限
            error = 'ERROR_DIR_NOT_WRITABLE'

        if not error:
            up_file.save(file_path)
            url = url_for('static', filename='%s/%s/%s' % ('uploads', temp, r_name))
    else:
        error = "post_error"
    res = {
        "uploaded": 1,    # * 命名固定
        "filename": r_name,
        "url": url
    }
    response = json.dumps(res)
    return response


