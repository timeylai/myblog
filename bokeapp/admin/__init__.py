from flask import Blueprint
admin = Blueprint('admin', __name__)
#  当前文件导入views errors 模块
from bokeapp.admin import views

