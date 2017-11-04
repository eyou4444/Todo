# -*- coding:utf-8 -*-
from . import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin  # 正常用户和匿名用户基类
from datetime import datetime
from markdown import markdown


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=True)
    users = db.relationship('User', backref='role')  # 主表

    # 定义一个静态的种子方法，自动初始化数据
    @staticmethod
    def seed():
        db.session.add_all(map(lambda r: Role(name=r), ['Guests', 'Administrators']))
        db.session.commit()


class User(UserMixin, db.Model):  # 继承多个基类
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=True)
    email = db.Column(db.String(45))
    password = db.Column(db.String(45), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 从表，有外键

    posts = db.relationship('Post', backref='author')
    comments = db.relationship('Comment', backref='author')

    @staticmethod
    def on_created(target, value, oldvalue, initiator):
        target.role = Role.query.filter_by(name='Guests').first()

# class AnonymousUser(AnonymousUserMixin):
#     @property
#     def locale(self):
#         return 'zh'
#
#     def is_administrator(self):
#         return False
#
# login_manager.anonymous_user = AnonymousUser


# 以下为钩子，不需要自己调用，程序需要时会自己调用
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# 监听当创建user时，默认的角色应该是Guest
db.event.listen(User.name, 'set', User.on_created)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45))
    body = db.Column(db.String(500))
    body_html = db.Column(db.String(500))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='post')
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        if value is None or (value is ''):
            target.body_html = ''
        else:
            target.body_html = markdown(value)


db.event.listen(Post.body, 'set', Post.on_body_changed)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(500))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))