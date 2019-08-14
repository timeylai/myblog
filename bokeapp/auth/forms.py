'''
author: timey
功能： 用戶登陸后的信息修改  密码修改
'''
from flask_wtf import FlaskForm  # 表单形式必须为FlaskFrom 防止warming, 无法验证
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from bokeapp.models import User  # 表单导入user验证


class SettingForm(FlaskForm):

    password = PasswordField(
        u'原密码',
        validators=[DataRequired(), Length(min=6, max=12, message='密码长度为6-12位')],
        render_kw={'type': 'password', 'placeholder': '请输入原密码'},
    )
    new_password = PasswordField(
        u'新密码',
        validators=[DataRequired(), Length(min=6, max=12, message='密码长度为6-12位')],
        render_kw={'type': 'password', 'placeholder': '请输入新密码'},

    )
    new_password_confirm = PasswordField(
        u'新密码',
        validators=[DataRequired(), Length(min=6, max=12, message='密码长度为6-12位'),
                    EqualTo('new_password', message="两次密码不一致")],
        render_kw={'type': 'password', 'placeholder': '请输入新密码'},

    )
    submit = SubmitField('账号注册')


class WriteForm(FlaskForm):
    temp_type = [
        ('PythonProject', 'python项目'),
        ('DirectionSkill', '前沿技术'),
        ('economic', '经济'),
        ('TeamManage', '团队协作'),
        ('other', '其他')
    ]
    title = StringField(u'文章标题', validators=[DataRequired()], render_kw={'class': 'cketitle'})
    body = TextAreaField('say something?', validators=[DataRequired()],
                         render_kw={'id': 'writebody'
                                    })
    page_type = SelectField(u'文章类型', choices=temp_type)
    submit = SubmitField(u'文章保存', render_kw={'class': 'submitstyle'})
