""" 
@Time    : 2018/7/16 19:52
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : user.py
@Desc    :
"""
from flask import jsonify, g

from app.libs.error_code import DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User

api = Redprint('user')

@api.route('/getUser/<int:auth>',methods=['GET'])
def get_user(auth):
    if auth:
        user = User.query.filter_by(id=auth).first_or_404()
        user.set_keys('id', 'nickname')
    else:
        user = User.query.filter_by().all()
        if user:
            for u in user:
                u.set_keys('id', 'nickname')
    return jsonify(user)

@api.route('/create')
def super_create_user():
    user = User.query.all()
    return jsonify(user)

