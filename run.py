# encoding:utf-8
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html', title='Welcome!')


@app.route('/services')
def services():
    return 'Service'


@app.route('/about')
def about():
    return 'About'


@app.route('/user/<username>')  #路由的变量名一定与参数名对应
def user(username):
    return 'User %s' % username


if __name__ == '__main__':
    app.run(debug=True)
