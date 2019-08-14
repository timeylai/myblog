from flask import Blueprint

main = Blueprint('main', __name__)

#  当前文件导入views errors 模块
from . import views, errors

