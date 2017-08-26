# encoding:utf-8
from flask import Flask, render_template, request
from werkzeug.routing import BaseConverter  # 德文写的正则模块包


class RegexConverter(BaseConverter):  # 正则表达式转换器
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app = Flask(__name__)
app.url_map.converters['regex'] = RegexConverter  # 初始化时把他初始化到url_map中，取名字叫regex


@app.route('/')
def hello_world():
    return render_template('index.html', title='Welcome to GloryRoad!')


@app.route('/services')
def services():
    return 'Service'


@app.route('/user/<username>')  # 路由的变量名一定与参数名对应
def user(username):
    return 'User %s' % username


@app.route('/user_id/<int:user_id>')  # 三种系统路由转换器:int,float,path
def user_id(user_id):
    return 'User_id %d' % user_id


@app.route('/user_regex/<regex("[a-z]{3}"):user_regex>')  # 测试正则表达式,需要给一个3位的a-z的字符串
def user_regex(user_regex):  # 对于非常严格的路由规则的定义可以使用正则
    return 'User_id %s' % user_regex


@app.route('/about')  # 无杠代表指向一个文件名来访问,访问时打/，会无法访问
def about():
    return 'About'


@app.route('/projects/')  # 结尾斜杠代表指向一个目录，访问时可以不打/，自动补全
@app.route('/our-works/')  # 一个viewfuntion两个url地址，对于多重规则非常直观，自上而下匹配路由
def projects():
    return 'The project page'


@app.route('/login', methods=['GET', 'POST']) #methods ~  method+s
def login():
    return render_template('login.html', method=request.method)


if __name__ == '__main__':
    app.run(debug=True)
