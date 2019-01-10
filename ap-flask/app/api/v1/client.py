""" 
@Time    : 2018/7/17 19:28
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : client.py
@Desc    :
"""
from flask import request

from app.libs.email import send_mail
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import Success, ClientTypeError
from app.libs.redprint import Redprint
from app.libs.token_auth import create_token, verify_token, auth
from app.models.base import db
from app.models.user import User
from app.validators.client_forms import ClientForm, UserEmailForm, ModifyPasswordForm

api = Redprint('client')

@api.route('/register',methods=['POST'])
def create_client():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email,
        ClientTypeEnum.USER_MINA: __register_user_by_mina
    }
    promise[form.type.data]()
    return Success()

@api.route('/register',methods=['GET'])
def create_email_user():
    token = request.args['token']
    data = verify_token(token)
    if data['type'] == 100:
        User.register_by_email(data['nickname'], data['email'], data['secret'])
    else:
        raise ClientTypeError()

    return 'abc'

@api.route('/modify',methods=['POST'])
@auth.login_required
def modify_password():
    form = ModifyPasswordForm().validate_for_api()
    user = User.query.filter_by(email=form.account.data).first_or_404()
    user.modify_password(form.secret.data,form.newSecret.data)

    return Success()

@api.route('/forget',methods=['POST'])
def forget_password():
    form = ClientForm().validate_for_api()
    user = User.query.filter_by(email=form.account.data).first_or_404()
    if user:
        token = create_token(email=form.account.data, type=form.type.data.value, secret=form.secret.data)
        send_mail(form.account.data, '重置密码', 'email/reset_password.html', [],user=user, token=token)

    return Success()

@api.route('/reset',methods=['GET'])
def reset_password():
    token = request.args['token']
    data = verify_token(token)
    if data['type'] == 100:
        with db.auto_commit():
            user = User.query.filter_by(email=data['email']).first_or_404()
            user.password = data['secret']
            db.session.add(user)

    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    token = create_token(email =form.account.data,type=form.type.data.value,secret=form.secret.data,nickname=form.nickname.data)
    send_mail(form.account.data,'用户注册','email/register.html',[],form=form,token=token)



def __register_user_by_mina():
    pass