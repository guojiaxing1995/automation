""" 
@Time    : 2018/7/17 20:00
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : user.py
@Desc    : user模型
"""
import datetime

from sqlalchemy import Column, Integer, String, SmallInteger, orm, DateTime
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed, ModifyFailed
from app.models.base import Base, db


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    phone = Column(String(12))
    wx_open_id = Column(String(50))
    nickname = Column(String(24), unique=True)
    auth = Column(SmallInteger, default=1)
    __password = Column('password', String(128))
    #登陆时间 未登陆默认 1970-01-01 00:00:00
    login_time = Column(DateTime, default=datetime.datetime.fromtimestamp(86400), nullable=False)

    @orm.reconstructor
    def __init__(self):
        self.__return_json = ['id', 'email', 'nickname', 'auth']

    def keys(self):
        return self.__return_json

    def set_keys(self,*args):
        return_json = [str(arg) for arg in args]
        self.__return_json = return_json

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self,raw):
        self.__password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname,account,secret):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    @staticmethod
    def set_login_time(id,login_time):
        with db.auto_commit():
            user = User.query.filter_by(id=id).first()
            if not user:
                raise NotFound(msg='user not found')
            user.login_time = login_time

    @staticmethod
    def verify(email,password):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFound(msg='user not found')
        if not user.check_password(password):
            raise AuthFailed()
        scope_dict = {
            1: 'UserScope',
            2: 'AdminScope',
            3: 'SuperScope'
        }
        scope = scope_dict[user.auth]
        return {'uid': user.id, 'scope': scope, 'login_time':user.login_time}

    def check_password(self,raw):
        if not self.password:
            return False
        return check_password_hash(self.password,raw)

    def modify_password(self, password, new_password):
        if self.check_password(password):
            with db.auto_commit():
                self.password = new_password
                self.login_time = datetime.datetime.fromtimestamp(86400)
                db.session.add(self)
        else:
            raise ModifyFailed(msg='原密码错误')