# -*- coding:utf-8 -*-
from flask_script import Manager
from app import create_app,db
from flask_migrate import Migrate,MigrateCommand
app = create_app()
manager = Manager(app)

migrate =Migrate(app,db)
manager.add_command('db',MigrateCommand)

@manager.command
def dev():
    from livereload import Server
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')  # 指明一个需要监测的目录,表示监测所有目录
    #自己打开浏览器
    live_server.serve(open_url=True)

#测试使用
@manager.command
def test():
    pass

#第一次安装程序是使用，安装环境或者数据库等
@manager.command
def deploy():
    pass

# 主要的引导文件。
if __name__ == '__main__':
    manager.run()

