# -*- coding:utf-8 -*-
from flask_script import Manager
from app import create_app,db
from app.models import User, Role, Post, Comment
from flask_migrate import Migrate,MigrateCommand,upgrade
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
#生成数据库，并进行初始化工作。
@manager.command
def deploy():
    from app.models import Role
    upgrade()
    Role.seed()

@manager.command
def forged():  #随机批量生成用户、帖子、评论数据
    from forgery_py import basic, lorem_ipsum, name, internet, date
    from random import randint

    db.drop_all()
    db.create_all()

    Role.seed()

    guests = Role.query.first()

    def generate_comment(func_author, func_post):
        return Comment(body=lorem_ipsum.paragraphs(),
                       created=date.date(past=True),
                       author=func_author(),
                       post=func_post())

    def generate_post(func_author):
        return Post(title=lorem_ipsum.title(),
                    body=lorem_ipsum.paragraphs(),
                    created=date.date(),
                    author=func_author())

    def generate_user():
        return User(name=internet.user_name(),
                    email=internet.email_address(),
                    password=basic.text(6, at_least=6, spaces=False),
                    role=guests)

    users = [generate_user() for i in range(0, 5)]
    db.session.add_all(users)

    random_user = lambda: users[randint(0, 4)]

    posts = [generate_post(random_user) for i in range(0, randint(50, 200))]
    db.session.add_all(posts)

    random_post = lambda: posts[randint(0, len(posts) - 1)]

    comments = [generate_comment(random_user, random_post) for i in range(0, randint(2, 100))]
    db.session.add_all(comments)

    db.session.commit()


# 主要的引导文件。
if __name__ == '__main__':
    manager.run()

