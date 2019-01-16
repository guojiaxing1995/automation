""" 
@Time    : 2018/9/2 16:37
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : scheduler.py
@Desc    : 定時任務
"""
import datetime

from sqlalchemy import Column, Integer, ForeignKey, String, orm
from sqlalchemy.orm import relationship
from app import scheduler
from app.libs.email import send_mail
from app.models.base import Base, db
from app.models.task import Task
import requests
from flask import current_app

from app.models.user import User


class Scheduler(Base):
    id = Column(Integer, primary_key=True)
    scheduler_id = Column(String(150), nullable=False,default='default')
    task = relationship('Task')
    task_id = Column(Integer, ForeignKey('task.id'), nullable=False)
    running_state = Column(Integer, nullable=False,default=1)
    day_of_week = Column(String(20), nullable=False,default='mon-sun')
    hour = Column(Integer, nullable=False,default=6)
    minute = Column(Integer, nullable=False,default=30)
    user = relationship('User')
    user_id = Column(Integer, ForeignKey('user.id'))
    #抄送人
    copy_person = Column(String(180))
    next_run_time = ''

    @orm.reconstructor
    def __init__(self):
        self.__return_json = ['id', 'task', 'day_of_week', 'hour', 'minute', 'user', 'copy_person','running_state','next_run_time','scheduler_id']

    def keys(self):
        return self.__return_json

    def set_keys(self, *args):
        return_json = [str(arg) for arg in args]
        self.__return_json = return_json

    def create_scheduler_id(self):
        task = Task.query.filter_by(id=self.task_id).first_or_404()
        self.scheduler_id = task.name + '_scheduler_' + str(self.id)

    def add_scheduler(self):
        with db.auto_commit():
            db.session.add(self)
        with db.auto_commit():
            self.create_scheduler_id()

    def add_job(self,url):
        current_app.apscheduler.add_job(func=self.job, args=(self.task_id,url,self.task,self.scheduler_id),id=self.scheduler_id, trigger='cron',
                                        day_of_week=self.day_of_week,hour=self.hour,minute=self.minute, replace_existing=True)

    #恢复任务
    def resume_job(self):
        scheduler.resume_job(self.scheduler_id)

    def job(self,task_id,url,task,scheduler_id):

        data = {
            "task_id":task_id
        }
        res = requests.post(url=url,json=data)
        from app import app
        with app.app_context():
            #查询当前定时任务和维护人
            scheduler = Scheduler.query.filter_by(scheduler_id=scheduler_id).first_or_404()
            user = User.query.filter_by(id=scheduler.user_id).first_or_404()
            current_app.logger.info(scheduler.scheduler_id)
            cc = []
            copy_list = scheduler.copy_person.split(';')
            if copy_list:
                for c in copy_list:
                    if c:
                        cc.append(c)
            send_mail(user.email, '定时任务执行报告<' + task.name + '>', 'email/scheduler_reporter.html', cc, user=user, task=task,
                      res=res.json())

    def get_job(self):
        jobs = scheduler.get_jobs()
        return jobs

    #获取任务详情
    def get_job_detail(self):
        job_id_list = []
        next_run_time_dict = {}
        jobs = self.get_job()
        for job in jobs:
            job_id_list.append(job.id)
            next_run_time_str = None
            if isinstance(job.next_run_time,datetime.datetime):
                    next_run_time_str = job.next_run_time.strftime('%Y-%m-%d %H:%M:%S')
            next_run_time_dict[job.id]=next_run_time_str
        return job_id_list,next_run_time_dict

    #获取所有任务
    def all_jobs(self):
        jobs = Scheduler.query.filter_by().all()
        job_id_list, next_run_time_dict = self.get_job_detail()
        for job in jobs:
            if job.scheduler_id in job_id_list:
                job.running_state = 1
                job.next_run_time = next_run_time_dict[job.scheduler_id]
                #如果任务被暂停，置状态为未运行
                if job.next_run_time == None:
                    job.running_state = 0
            else:
                job.running_state = 0

        return jobs


    #暂停任务
    def pause_job(self):
        scheduler.pause_job(self.scheduler_id)
        with db.auto_commit():
            self.running_state = 0



    def update_scheduler(self,scheduler_id,user_id,day_of_week,hour,minute,copy_person):
        self = Scheduler.query.filter_by(scheduler_id=scheduler_id).first_or_404()
        with db.auto_commit():
            self.user_id = user_id
            self.minute = minute
            self.day_of_week = day_of_week
            self.hour = hour
            self.copy_person = copy_person

    def modify_job(self):
        scheduler.modify_job(self.scheduler_id, trigger='cron', minute=self.minute,day_of_week=self.day_of_week,hour=self.hour)

    def delete_job(self):
        scheduler.delete_job(self.scheduler_id)

    def delete_scheduler(self):
        scheduler = Scheduler.query.filter_by(scheduler_id=self.scheduler_id).first_or_404()
        with db.auto_commit():
            scheduler.delete()
