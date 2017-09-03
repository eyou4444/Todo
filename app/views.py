# -*- coding:utf-8 -*-
from flask import flash, render_template, redirect


def init_views(app):
    @app.route('/')
    def index():
        # response = make_response(render_template('index.html', title='Welcome to GloryRoad!'))   对函数进行包装
        # #response.set_cookie('username', '')   使用response设置cookie
        # return response
        return render_template('index.html', title='Welcome to GloryRoad!')

    @app.template_filter('md')  # 定义模版中的装饰器，并注册到模版中使用
    def markdown_to_html(txt):  # 导入输入值
        from markdown import markdown
        return markdown(txt)  # 使用markdown函数输出

    def read_md(filename):  # 读取文件，输出到页面
        with open(filename) as md_file:
            content = reduce(lambda x, y: x + y, md_file.readlines())
            return content.decode('utf-8')

    @app.context_processor  # 将方法注册到模版中使用的装饰器
    def inject_methods():  # 方法名可以随便起
        return dict(read_md=read_md)  # 直接返回一个字典

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

    @app.route('/login', methods=['GET', 'POST'])  # methods ~  method+s
    def login():
        from app.forms import LoginForm
        form = LoginForm()
        flash(u'登录成功！')
        return render_template('login.html', title=u'登录', form=form)

    # 上传文件方法
    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':
            f = request.files['file']  # 与form获取的键值是一样的，对应到模版文件中的name的名称
            basepath = path.abspath(path.dirname(__file__))  # 获取当前文件的绝对路径
            upload_path = path.join(basepath, 'static\uploads', f.filename)  # 上传文件的路径，文件名被包装时，不能使用中文
            f.save(upload_path)  # 将文件直接存储到对应的目录,文件名使用secure_filename包装。
            return redirect(url_for('upload'))  # 当上传成功，返回upload,GET方法,与jinjia的区别是：这里不需要使用“点”
        return render_template('upload.html')  # 对于该方法，返回上传页面

    @app.errorhandler(404)  # 错误处理页面装饰器
    def page_not_found(error):
        return render_template('404.html'), 404  # 后面可以直接加错误码

    # 定义模板的测试函数，如果是当前访问的页面，就不显示链接
    @app.template_test('current_link')  # 定义名字
    def is_current_link(link):
        return link == request.path