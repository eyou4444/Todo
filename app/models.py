# -*- coding:utf-8 -*-
from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=True)
    users = db.relationship('User', backref='role')# 主表

    #定义一个静态的种子方法，自动初始化数据
    @staticmethod
    def seed():
        db.session.add_all(map(lambda r:Role(name=r),['Guests','Administrators']))
        db.session.commit()



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=True)
    password = db.Column(db.String(45), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 从表，有外键

    @staticmethod
    def on_created(target,value,oldvalue,initiator):
        target.role = Role.query.filter_by(name='Guests').first()



#监听当创建user时，默认的角色应该是Guest
db.event.listen(User.name,'set',User.on_created)
