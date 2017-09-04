# -*- coding:utf-8 -*-
#专门做登录的验证
from flask import Blueprint

auth = Blueprint('auth',__name__)

import forms,views