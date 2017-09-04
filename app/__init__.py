# -*- coding:utf-8 -*-
from os import path  # 上传文件是指定路径。服务器地址

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import *
from flask_sqlalchemy import SQLAlchemy
from werkzeug.routing import BaseConverter  # 德文写的正则模块包


class RegexConverter(BaseConverter):  # 正则表达式转换器
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


basedir = path.abspath(path.dirname(__file__))  # 配置绝对路径，当前的项目路径

bootstrap = Bootstrap()  # 这个变量是全局变量，引用这个文件的时候可以使用
nav = Nav()
db = SQLAlchemy()


# 使用工厂方法创建app
def create_app():
    app = Flask(__name__)
    app.url_map.converters['regex'] = RegexConverter
    # 初始化时把他初始化到url_map中，取名字叫regex
    app.config.from_pyfile('config')
    # 配置数据库连接
    # app.config['SQLALCHEMY_DATABASE_URI'] = \
    #     'sqlite:///' + path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://root:zhangxu860404@localhost/gloryroad'
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    nav.register_element('top', Navbar(u'光荣之路',
                                       View(u'主页', 'main.index'),
                                       View(u'关于', 'main.about'),
                                       View(u'服务', 'main.services'),
                                       View(u'登录', 'auth.login')))
    db.init_app(app)  # 将插件进行初始化
    bootstrap.init_app(app)
    nav.init_app(app)

    #导入蓝图
    from auth import auth as auth_blueprint
    from main import main as main_blueprint
    #注册蓝图
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    # app.register_blueprint(main_blueprint,static_folder='static')
    app.register_blueprint(main_blueprint)
    return app
