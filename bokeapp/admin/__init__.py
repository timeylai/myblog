from flask import Blueprint
admin = Blueprint('admin', __name__)
#  ��ǰ�ļ�����views errors ģ��
from bokeapp.admin import views

