""" 
@Time    : 2018/7/19 19:16
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : token.py
@Desc    :
"""
import time
from datetime import datetime

from flask import current_app, jsonify
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.libs.enums import ClientTypeEnum
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.client_forms import ClientForm

api = Redprint('token')

@api.route('',methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
    }
    #过期时间
    expiration = current_app.config['TOKEN_EXPIRATION']
    identity = promise[ClientTypeEnum(form.type.data)](form.account.data,form.secret.data)
    #当前时间
    now_time = datetime.now()
    token = generate_auth_token(identity['uid'],form.type.data,now_time,identity['scope'],expiration)
    t = {'token': token.decode('ascii')}
    #登陆成功后修改登陆时间
    User.set_login_time(identity['uid'],now_time)

    return jsonify(t),201

def generate_auth_token(uid,ac_type,login_time,scope=None,expiration=7200):
    #生成令牌
    s = Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope,
        'login_time': time.mktime(login_time.timetuple())
    })