# -*- coding: UTF-8 -*-
# flask 中的定向调转函数
"""
author: timey
main 网站主体，login ,register , 主页操作等等。

"""
from flask import render_template, redirect, flash, url_for, request, session
from bokeapp.main import main    # 把main包导入，init初始化中有蓝图
# from bokeapp import models   #  models 生成，经过
from .forms import UserLoginFrom, RegisterForm
from ..models import User, PageInfo, Bookmarking, GuestBook  # 导入
from bokeapp import db  # 导入db操作数据库
from werkzeug.security import generate_password_hash, check_password_hash  # 导入hash 加密包
from flask_login import login_user, logout_user, current_user
from ..emails import send_mail
from datetime import timedelta
import re
import json


@main.route('/register',  methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "GET":
        return render_template('user/register.html', form=form)
    elif request.method == 'POST':
        if form.email.data != '' and form.username.data != '' \
                and form.password.data != '' and form.password_confirm.data != '':
            # 应用User模型封装表单的username, password, email ,token 数据到user
            user = User(username=form.username.data,
                        password_hash=generate_password_hash(form.password.data),
                        email=form.email.data)
            db.session.add(user)  # 增加注册用户
            db.session.commit()
            token = user.generate_token()  # 生成token  user表调用generate_token方法
            ''' 向user.email 发送激活邮件   发送参数（收件人邮箱+邮箱标题+ 激活html路径(邮箱内容） +账号+token）
            '''
            send_mail(user.email, '请激活账号', 'email/activate', username=form.username.data, token=token)
            # 提示用户激活
            flash('注册成功去邮箱中激活')
            return redirect(url_for('main.login'))
        else:
            flash('不能为空')
    return render_template('user/register.html')


@main.route('/active/<token>/')
def activate(token):
    if User.check_token(token):   # model 中User 方法引用
        return redirect(url_for('main.login'))
    else:
        flash('激活失败')


# 登陆
@main.route('/', methods=['POST'])  # 登陆后调转路由* 注意顺序，POST表单验证登陆
@main.route('/login', methods=['GET', 'POST'])
def login():
    # 表单类型化
    form = UserLoginFrom()
    if request.method == 'GET':
        return render_template('user/login.html', form=form)
    if request.method == 'POST':
        if form.username.data != '' and form.password.data != '':
            user = User.query.filter_by(username=form.username.data).first()
            if not user:
                flash('该用户不存在')
            elif not user.is_activate:
                flash('该用户尚未激活')
            elif user.check_password_hash(form.password.data):
                flash('登陆成功')
                '''login_user方法已经封装好cookies ，不需要自己再构建方法
                '''
                login_user(user, remember=True, duration=timedelta(hours=2))  # remember True duration=设置时间
                # session['username'] = user.username
                # session.permanent = True
                '''未登录视图指定跳转到index'''
                next_url = request.args.get('next')
                if not next_url or not next_url.startswith('/'):   #
                    next_url = url_for('main.index')
                return redirect(next_url)
            else:
                flash('密码错误')
        else:
            flash('账号密码不能为空')
    return render_template('user/login.html', form=form)


# 退出
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for('index'))


@main.route('/')
@main.route('/index')
def index():
    """ 首页展示，所有的文章"""
    all_page = PageInfo.query.filter_by().order_by(PageInfo.content_time.desc()).limit(3)    # 初始化展示的内容
    page_list = index_deal_page(all_page, False)
    is_admin_page = PageInfo.query.filter_by(is_admin_good=True).order_by(PageInfo.content_time.desc()).limit(10)
    admin_good_page = index_deal_page(is_admin_page, True)
    content_see_desc = PageInfo.query.filter_by().order_by(PageInfo.content_see.desc()).limit(10)
    content_look_desc = index_deal_page(content_see_desc, True)
    return render_template('main/index.html', page_list=page_list,
                           admin_good_page=admin_good_page, content_look=content_look_desc)


def index_deal_page(temp_orm, is_true):
    """ 数据格式处理，进行简短展示处理"""
    result = []
    for page in temp_orm:
        temp = dict()
        if is_true:
            temp['content'] = html_to_str(page.content)[0:30] + "......"
        else:
            temp['content'] = html_to_str(page.content)[0:100] + "......"
        temp['page_id'] = page.page_id
        temp['title'] = page.title
        temp['time'] = page.content_time.strftime("%Y-%m-%d")
        temp['see'] = page.content_see
        temp['content_img'] = page.content_img
        result.append(temp)
    return result


@main.route('/blogsdata',  methods=['POST'])  # 若有post到后台，一定要用post打开路由方法
def get_blog_data():
    """ blog lazy loading 每次加载num_last ， * 会产生并发情况，需要优化"""
    flag = request.form.get('num')  # 获取懒加载js中的要加载的信息
    num_last = request.form.get('num_last', "0")   # 标记上一次哪里开始加载
    if flag == "true":  # 标记懒加载进行了
        num_last = int(int(num_last) + 3)  # 不+3 切片会[:num_last],导致从 0 开始
    all_page = PageInfo.query.filter_by().order_by(PageInfo.content_time.desc()).limit(num_last)
    page_list = index_deal_page(all_page, False)  # 返回的是字典了
    # print(page_list)
    temp = []
    for page in page_list[num_last - 3:num_last]:
        a = dict()
        a['page_id'] = page['page_id']
        a['content_title'] = page['title']
        a['content_page'] = page['content']
        a['content_time'] = page['time']
        a['see'] = page['see']
        a['content_img'] = page['content_img']
        temp.append(a)
    return json.dumps(temp)


def html_to_str(content):
    """ page 清洗 去除html标签 """
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    blank_line = re.compile('\n+')  # 去掉多余的空行
    """s to s """
    s = re_cdata.sub('', content)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    s = blank_line.sub('\n', s)
    s = s.replace('&nbsp;', '')    # 空格
    s = s.replace('&ldquo;', '“')  # 双引号左
    s = s.replace('&rdquo;', '”')  # 双引号右
    # s = replaceCharEntity(s)  # 替换实体,另写方法
    return s


@main.route('/share')
def share():
    web_making = Bookmarking.query.filter(Bookmarking.web_type != 'course').all()
    blog_making = Bookmarking.query.filter_by(web_type='course').all()
    return render_template('main/share.html', web_making=web_making, boke_making=blog_making)


@main.route('/share/<web_type>')
def share_type(web_type):
    web_making = Bookmarking.query.filter(Bookmarking.web_type == web_type).all()
    blog_making = Bookmarking.query.filter_by(web_type='course').all()
    return render_template('main/share.html', web_making=web_making, boke_making=blog_making)


@main.route('/workplace')
def collect():
    """ workplace data to show """
    all_page = PageInfo.query.filter_by().order_by(PageInfo.content_time.desc()).limit(3)
    page_list = index_deal_page(all_page, False)
    is_admin_page = PageInfo.query.filter_by(is_admin_good=True).order_by(PageInfo.content_time.desc()).limit(10)
    admin_good_page = index_deal_page(is_admin_page, True)
    return render_template('main/workplace.html', page_list=page_list, admin_good_page=admin_good_page)


@main.route('/type/blog',  methods=['POST'])  # 若有post到后台，一定要用post打开路由方法
def get_type_blog_data():
    """ blog lazy loading 每次加载num_last """
    flag = request.form.get('num')  # 获取懒加载js中的要加载的信息
    num_last = request.form.get('num_last', "0")   # 标记上一次哪里开始加载
    if flag == "true":  # 标记懒加载进行了
        num_last = int(int(num_last) + 3)  # 每次懒加载3个data
    content_type = request.form.get('content_type')
    if content_type == 'workplace':
        all_page = PageInfo.query.filter_by().order_by(PageInfo.content_time.desc()).limit(num_last)
    else:
        all_page = PageInfo.query.filter_by(content_type=content_type).order_by(
                   PageInfo.content_time.desc()).limit(num_last)
    page_list = index_deal_page(all_page, False)  # 返回的是字典了
    # print(page_list)
    """    elif content_type == 'play':
        all_page = PageInfo.query.filter(PageInfo.content_type == 'economic' and
                                         PageInfo.content_type == 'TeamManage'). \
                   order_by(PageInfo.content_time.desc()).limit(num_last)
    elif content_type == 'see':
        all_page = PageInfo.query.filter(PageInfo.content_type == 'PythonProject' and
                                         PageInfo.content_type == 'DirectionSkill'). \
                   order_by(PageInfo.content_time.desc()).limit(num_last) """
    temp = []
    for page in page_list[num_last - 3:num_last]:
        a = dict()
        a['page_id'] = page['page_id']
        a['content_title'] = page['title']
        a['content_page'] = page['content']
        a['content_time'] = page['time']
        a['see'] = page['see']
        a['content_img'] = page['content_img']
        temp.append(a)
    return json.dumps(temp)


@main.route('/workplace/<content_type>')
def collect_type(content_type):
    all_page = PageInfo.query.filter(PageInfo.content_type == content_type).order_by(
               PageInfo.content_time.desc()).limit(10)
    page_list = index_deal_page(all_page, False)
    is_admin_page = PageInfo.query.filter_by(is_admin_good=True).order_by(PageInfo.content_time.desc()).limit(10)
    admin_good_page = index_deal_page(is_admin_page, True)
    return render_template('main/workplace.html', page_list=page_list, admin_good_page=admin_good_page)


"""
@main.route('/work/<title_type>')
def collect_type_title(title_type):
    if title_type == 'see':
        all_page = PageInfo.query.filter(PageInfo.content_type == 'PythonProject' and
                                         PageInfo.content_type == 'DirectionSkill').\
                   order_by(PageInfo.content_time.desc()).limit(3)
    else:
        all_page = PageInfo.query.filter(PageInfo.content_type == 'economic' and
                                         PageInfo.content_type == 'TeamManage'). \
                   order_by(PageInfo.content_time.desc()).limit(3)
    page_list = index_deal_page(all_page, False)
    is_admin_page = PageInfo.query.filter_by(is_admin_good=True).order_by(PageInfo.content_time.desc()).limit(10)
    admin_good_page = index_deal_page(is_admin_page, True)
    return render_template('main/workplace.html', page_list=page_list, admin_good_page=admin_good_page)
"""


@main.route('/lifethinking')
def life_debunk():
    return render_template('main/life_debunk.html')


@main.route('/webword')
def word():
    return render_template('main/webword.html')


""" """


@main.route('/p/<page_id>')
def page_url(page_id):
    """ page url to show, index已经反回了page_id ,只是没有URL，这个是文章展示的url"""
    page = PageInfo.query.filter_by(page_id=page_id).first()
    # next = PageInfo.query.filter_by(id=page.id)
    user = User.query.filter_by(id=page.user_id).first()    # 根据文章的page_id 找到user_id (两者建立衍射关系），查到username
    try:
        if page.user_id == current_user.id:  # 判断是否自己账户在点击
            page.content_see = page.content_see
    except KeyError:
        page.content_see = page.content_see + 1
    db.session.add(page)
    db.session.commit()
    """ 此处需要 编写一个文章相似度算法， 暂时引用whoosh_ index, 根据page找到keyboard ,进行全中文检索. page.content_key
    是搜索词， order_by 用的是数据库模型 """
    page_list = PageInfo.query.whoosh_search(page.content_keyword).order_by(PageInfo.content_see.desc()).limit(6)
    """page De 排行 和 点击 """
    is_admin_page = PageInfo.query.filter_by(is_admin_good=True).order_by(PageInfo.content_time.desc()).limit(10)
    admin_good_page = index_deal_page(is_admin_page, True)
    content_see_desc = PageInfo.query.filter_by().order_by(PageInfo.content_see.desc()).limit(10)
    content_look_desc = index_deal_page(content_see_desc, True)
    page_guest_all = GuestBook.query.filter_by(page_id=page_id).all()
    return render_template('main/show_page.html', page=page, user=user, page_guest_all=page_guest_all,
                           page_list=page_list, admin_good_page=admin_good_page, content_look=content_look_desc)


@main.route('/<page_id>/guestbook', methods=['GET', 'POST'])
def guest_book(page_id):
    """ page add/show guest book """
    if request.method == 'POST':
        """ 无登录状态 current_user 方法报错，try ...except ... """
        try:
            user = current_user.username if current_user.username else ''
        except:
            user = ''
        content = request.form.get('GuestBook')
        page_guest_book = GuestBook(guest_content=content, guest_user=GuestBook.guest_username(user),
                                    page_id=page_id)
        db.session.add(page_guest_book)
        db.session.commit()
    return redirect(url_for('main.page_url', page_id=page_id))   # 重定向时，page_url 没有id参数，需要返回


@main.route('/<key>/search', methods=['GET'])
def key_search(key):
    """ 点击关键词进行搜索 """
    key_page = PageInfo.query.filter(PageInfo.content_keyword.like(key)).all()
    page_list = []
    for page in key_page:
        temp = dict()
        temp['page_id'] = page.page_id
        temp['title'] = page.title
        temp['content'] = html_to_str(page.content)  # 还未进行简短处理
        temp['time'] = page.content_time.strftime("%Y-%m-%d")
        temp['see'] = page.content_see
        page_list.append(temp)
    return render_template('main/search.html', page_list=page_list)  # 返回json格式到html ,注意数据的读取


@main.route('/search', methods=['POST'])
def search():
    """ index 输入搜索 """
    key_board = request.form.get("keyboard")   # *form 表单name 值
    if not key_board:
        return url_for('main.index')
    return redirect(url_for('main.search_result', key_board=key_board))


@main.route('/search/<key_board>')
def search_result(key_board):
    """ 搜索功能 ，需点击文章生成whoosh_index？,
         flask_whooshalchemyplus 只支持英文查询，中文需要引用yieba分词
    """
    try:
        results = PageInfo.query.whoosh_search(key_board).all()  # 查询返回的是list ,所以数list的引用
    except:
        return redirect(url_for('main.index'))
    page_list = []
    for page in results:
        temp = dict()
        temp['page_id'] = page.page_id
        temp['title'] = page.title
        temp['content'] = html_to_str(page.content)  # 还未进行简短处理
        temp['time'] = page.content_time.strftime("%Y-%m-%d")
        temp['see'] = page.content_see
        page_list.append(temp)
    return render_template('main/search.html', page_list=page_list)  # 返回json格式到html ,注意数据的读取


