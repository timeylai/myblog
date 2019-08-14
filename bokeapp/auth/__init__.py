from flask import Blueprint

auth = Blueprint('auth', __name__)

#  当前文件导入views errors 模块
from bokeapp.auth import views, errors

