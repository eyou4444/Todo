# -*- coding:utf-8 -*-
from . import db


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=True)
    users = db.relationship('User', backref='role')  # 主表


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=True)
    password = db.Column(db.String(45), nullable=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))  # 从表，有外键
