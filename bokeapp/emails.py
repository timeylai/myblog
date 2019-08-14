from flask_mail import Message, Mail
from flask import render_template, current_app
from threading import Thread
from .extensions import mail   # 导入实例化之后的mail


# 获取文件上下文， 异步发送
def async_send_mail(app, msg):
    with app.app_context():
        mail.send(message=msg)


# 定义发送邮件函数(参数顺序)
def send_mail(to, subject, template, **kwargs):  # **kwargs 传递是dict  *args tuple
    # 线程有关，前提因为程序是单任务运行的，不可能说等到主线程# （即邮箱要返回点击结果）
    app = current_app._get_current_object()
    '''
    sender = app.config['MAIL_USERNAME']
    pwd = app.config['MAIL_PASSWORD']
    SERVER = app.config['MAIL_SERVER']
    recipients = [to] '''
    '''主题， sender发件人 recipients收件人'''
    msg = Message(subject=subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = render_template(template+'.html', **kwargs)
    send = Thread(target=async_send_mail, args=[app, msg])
    send.start()

