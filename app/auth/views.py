# -*- coding:utf-8 -*-
from flask import flash, render_template, redirect
from . import auth
@auth.route('/login', methods=['GET', 'POST'])  # methods ~  method+s
def login():
    from app.auth.forms import LoginForm
    form = LoginForm()
    flash(u'登录成功！')
    return render_template('login.html', title=u'登录', form=form)

@auth.route('/register',methods=['GET', 'POST'])
def register():
    return render_template('register.html',titile=u'注册')