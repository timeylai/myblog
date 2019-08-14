from wtforms import BooleanField, ValidationError, validators, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf import FlaskForm  # 表单形式必须为FlaskFrom 防止warming, 无法验证
from bokeapp.models import User  # 表单导入user验证


class UserLoginFrom(FlaskForm):
    username = StringField(
        label=u'用户名',
        validators=[
            validators.DataRequired(message='用户名不能为空'),
            validators.length(min=1, max=18, message='用户名长度1-18位')
        ],

        render_kw={'type': 'text', 'placeholder': '请输入用户名，如：timey'},
    )
    password = PasswordField(
        label=u'密码',
        validators=[
            validators.DataRequired(message='密码不能为空'),
            validators.length(min=6, message='密码必须大于%（min）d'),
        ],

        render_kw={'type': 'password', 'placeholder': '请输入密码', 'required': 'required'},
    )
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField(
        u'用户名',
        validators=[DataRequired(message='用户名不能为空'), Length(min=1, max=12, message='用户名长度不超过12(6个字)')],
        render_kw={'type': 'text', 'placeholder': '请输入用户名，如：timey'},
        # default=''
    )
    password = PasswordField(
        u'密码',
        validators=[DataRequired(message='密码不能为空'), Length(min=6, max=12, message='密码长度6-12位')],
        render_kw={'type': 'password', 'placeholder': '请输入密码', 'required': 'required'},
    )
    password_confirm = PasswordField(
        u'密码',
        validators=[DataRequired(message='再次输入密码不能为空'),
                    Length(min=6, max=12, message='密码长度6-12位'),
                    EqualTo('password', message="两次密码不一致")],
        render_kw={'type': 'password', 'placeholder': '请再次输入密码'},
    )

    email = StringField(
        u'邮箱',
        validators=[Email(message='邮箱不能为空'), Email(message='邮箱格式错误')],
        render_kw={'type': 'email', 'placeholder': '请输入邮箱'},
    )
    submit = SubmitField('账号注册')

    # 自定义验证用户是否存在
    def validate_username(self, field):
        if User.query.filter(User.username == field.data).first():
            raise ValidationError('该用户已注册！')

    # 自定义验证邮箱是否存在
    def validata_email(self, field):
        if User.query.filter(User.email == field.data).first():
            raise ValidationError('该邮箱已注册！')

