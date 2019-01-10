""" 
@Time    : 2018/9/1 17:14
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : record_report.py
@Desc    : 存放执行记录结果
"""
import datetime

from flask import current_app
from sqlalchemy import Column, Integer, String, ForeignKey,orm
from sqlalchemy.orm import relationship

from app.models.base import Base, db


class recordReport(Base):
    id = Column(Integer, primary_key=True)
    task = relationship('Task')
    task_id = Column(Integer, ForeignKey('task.id'), nullable=False)
    pass_num = Column(Integer, nullable=False)
    fail_num = Column(Integer, nullable=False)
    execute_num = Column(Integer, nullable=False)
    total = Column(Integer, nullable=False)
    pass_probability = Column(Integer, nullable=False)
    fail_probability= Column(Integer, nullable=False)
    execute_probability = Column(Integer, nullable=False)
    record_date = Column(String(20), nullable=False)
    cicle = False

    @orm.reconstructor
    def __init__(self):
        self.__return_json = ['id','task_id','pass_num','fail_num','execute_num','total','pass_probability','fail_probability','execute_probability','record_date','cicle']

    def keys(self):
        return self.__return_json

    def set_keys(self, *args):
        return_json = [str(arg) for arg in args]
        self.__return_json = return_json

    def add(self,task_id,pass_num,fail_num,execute_num,total,pass_probability,fail_probability,execute_probability,record_date):
        self.task_id = task_id
        self.pass_num = pass_num
        self.fail_num = fail_num
        self.total =total
        self.execute_num = execute_num
        self.pass_probability = pass_probability
        self.fail_probability = fail_probability
        self.execute_probability = execute_probability
        self.record_date = record_date
        with db.auto_commit():
            db.session.add(self)

    def update(self,task_id,pass_num,fail_num,execute_num,total,pass_probability,fail_probability,execute_probability,record_date):
        self = recordReport.query.filter_by(task_id=task_id,record_date=record_date).first_or_404()
        self.pass_num = pass_num
        self.fail_num = fail_num
        self.total = total
        self.execute_num = execute_num
        self.pass_probability = pass_probability
        self.fail_probability = fail_probability
        self.execute_probability = execute_probability

        with db.auto_commit():
            db.session.add(self)

    #判断记录应该是新增还是更新，新增TRUE 更新False
    def add_or_update(self):
        record_report = recordReport.query.filter_by(record_date=self.record_date,task_id=self.task_id).first()
        if record_report:
            return False
        else:
            return True

    @staticmethod
    def week_get(vdate_str):
        vdate = datetime.datetime.strptime(vdate_str, '%Y-%m-%d').date()
        current_app.logger.debug(vdate)
        dayscount = datetime.timedelta(days=vdate.isoweekday())
        dayfrom = vdate - dayscount + datetime.timedelta(days=1)
        dayto = vdate - dayscount + datetime.timedelta(days=7)
        week7 = []
        i = 0
        while (i <= 6):
            week7.append(str(dayfrom + datetime.timedelta(days=i)))
            i += 1
        return week7

    #获取报告数据
    def report_date(self):
        week_list = recordReport.week_get(self.record_date)
        record_dict = {}
        record_report = recordReport()
        for date in week_list:
            date_report = recordReport.query.filter_by(record_date=date,task_id=self.task_id).first()
            if date_report:
                if date_report.record_date == self.record_date:
                    date_report.cicle = True
                record_dict[date] = date_report
            else:
                record_dict[date] = record_report
        return record_dict