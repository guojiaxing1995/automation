""" 
@Time    : 2018/7/24 19:42
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : email.py
@Desc    : 发送邮件相关
"""
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from app import mail


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            pass


def send_mail(to, subject, template, cc,**kwargs):
    # Python email
    msg = Message('[automation]' + ' ' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to],cc=cc)
    msg.html = render_template(template, **kwargs)
    # current_app  app = Flask()
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()



