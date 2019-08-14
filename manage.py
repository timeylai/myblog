import os
# manage 应用下的模块导入
from bokeapp import create_app, db  # 导入实例化app
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app('default')  # 设定调用的环境 ，跳转到init ，引用方法
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command('shell', Shell(make_context=make_shell_context))  # 增加shell命令行
manager.add_command('db', MigrateCommand)    # 增加db 命令行


if __name__ == '__main__':
    manager.run()



