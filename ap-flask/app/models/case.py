""" 
@Time    : 2018/7/26 19:51
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : case.py
@Desc    : Case 模型
"""
import datetime
import json
import re

import requests
from flask import current_app
from sqlalchemy.orm import relationship

from app.libs.spider import deal_default
from app.libs.token_auth import User
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, SmallInteger, orm, DateTime, Boolean, ForeignKey

from app.models.task import Task
from app.models.task_case import TaskCase
from app.models.user import User as USER


class Case(Base):
    id = Column(Integer, primary_key=True)
    case_id = Column(String(30),nullable=False)
    case_name = Column(String(50),nullable=False)
    is_run = Column(Boolean,nullable=False)
    method = Column(String(4),nullable=False)
    url = Column(String(500),nullable=False)
    header = Column(String(500))
    deal_method = Column(String(20))
    dependent_case = Column(String(30))
    need_position = Column(String(200))
    # 0 表单提交 1 json提交
    submission = Column(String(2))
    data = Column(String(2000))
    expect_result = Column(String(2000))
    actual_result = Column(String(5),nullable=False)
    interface_return = Column(String(5000))
    task_case = relationship('TaskCase')
    task_case_id = Column(Integer,ForeignKey('task_case.id'))
    task = relationship('Task')
    task_id = Column(Integer,ForeignKey('task.id'))
    user = relationship('User')
    user_id = Column(Integer,ForeignKey('user.id'))
    #是否是最新的意思执行记录
    is_new = Column(Boolean,nullable=False)

    @orm.reconstructor
    def __init__(self):
        self.__return_json = ['id','case_id','case_name','is_run','method','url','header','deal_method','dependent_case',
                              'need_position','submission','data','expect_result','actual_result','interface_return','task_case_id','task_id','user_id','is_new']

    def keys(self):
        return self.__return_json

    def set_keys(self, *args):
        return_json = [str(arg) for arg in args]
        self.__return_json = return_json

    #封装requests库
    def spider(self):
        res = None
        if self.method == 'get' or self.method == 'GET':
            res = self.get_main()
        elif self.method =='post' or self.method == 'POST':
            res = self.post_main()
        elif self.method == 'put' or self.method == 'PUT':
            res = self.put_main()
        elif self.method == 'delete' or self.method == 'DELETE':
            res = self.delete_main()

        #return json.dumps(res,ensure_ascii=False,sort_keys=True,indent=2)
        return res

    #批量执行 一条case的请求
    def spider_batch(self):
        self.stitch_request_header()
        self.str_to_dict()
        self.deal_data_and_header()
        res = self.spider()
        self.interface_return = res.json()
        self.deal_interface_return()
        self.dict_to_str()
        self.split_interface_return()
        self.fail_or_pass()
        self.is_new = True
        self.user_id = 2
        with db.auto_commit():
            db.session.add(self)

    def split_interface_return(self):
        if len(self.interface_return) > 5000:
            self.interface_return = self.interface_return[0:4999]


    #批量执行的一条是否通过
    def fail_or_pass(self):
        if self.expect_result in self.interface_return and self.expect_result != '':
            self.actual_result = True
        else:
            self.actual_result = False

    def get_main(self):
        if self.header:
           res = requests.get(url=self.url,params=self.data,headers=self.header)
        else:
            res = requests.get(url=self.url,params=self.data)
        return res

    def post_main(self):
        if self.header:
            if self.submission == '0':
                res = requests.post(url=self.url,data=self.data,headers=self.header)
            elif self.submission == '1':
                res = requests.post(url=self.url, json=self.data, headers=self.header)
        else:
            if self.submission == '0':
                res = requests.post(url=self.url,data=self.data)
            elif self.submission == '1':
                res = requests.post(url=self.url, json=self.data)

        return res

    def put_main(self):
        if self.header:
            if self.submission == '0':
                res = requests.put(url=self.url,data=self.data,headers=self.header)
            elif self.submission == '1':
                res = requests.put(url=self.url, json=self.data, headers=self.header)
        else:
            if self.submission == '0':
                res = requests.put(url=self.url,data=self.data)
            elif self.submission == '1':
                res = requests.put(url=self.url, json=self.data)

        return res

    def delete_main(self):
        if self.header:
            if self.submission == '0':
                res = requests.delete(url=self.url,data=self.data,headers=self.header)
            elif self.submission == '1':
                res = requests.delete(url=self.url, json=self.data, headers=self.header)
        else:
            if self.submission == '0':
                res = requests.delete(url=self.url,data=self.data)
            elif self.submission == '1':
                res = requests.delete(url=self.url, json=self.data)

        return res

    #判断用例是否通过
    def pass_or_fail(self):
        self.str_to_dict()
        res = self.spider()
        interface_return = json.dumps(res.json(),ensure_ascii=False) if res.json() else 1
        if self.expect_result in interface_return and self.expect_result != '':
            self.actual_result = True
        else:
            self.actual_result = False
        self.interface_return = res.text

    #入参 字符串转字典
    def str_to_dict(self):
        self.data = json.loads(self.data) if self.data  else self.data
        self.header = json.loads(self.header) if self.header else  self.header

    #字典转字符串存入数据库
    def dict_to_str(self):
        self.data = json.dumps(self.data,ensure_ascii=False) if self.data  else self.data
        self.header = json.dumps(self.header,ensure_ascii=False) if self.header else  self.header
        self.interface_return = json.dumps(self.interface_return, ensure_ascii=False) if self.interface_return else self.interface_return

    #判断当前case的url是否有域名，没有则拼接
    def stitch_request_header(self):
        if 'http' not in self.url:
            task = Task.query.filter_by(id=self.task_id).first_or_404()
            self.url = task.request_header + self.url

    #替换请求参数data和header中的形参为依赖数据字段中的值
    def deal_data_and_header(self):
        task = Task.query.filter_by(id=self.task_id).first_or_404()
        if self.data:
            for key,value in self.data.items():
                if type(value) == str:
                    if re.search('\$(.*)\$',value):
                        v = task.depend_data_dict[re.search('\$(.*)\$',value).group(0)[1:-1]]
                        self.data[key] = v
        if self.header:
            for key,value in self.header.items():
                if type(value) == str:
                    if re.search('\$(.*)\$',value):
                        v = task.depend_data_dict[re.search('\$(.*)\$',value).group(0)[1:-1]]
                        self.header[key] = v

    #接口返回数据处理 将需要的字段存在task的字典中
    def deal_interface_return(self):
        task = Task.query.filter_by(id=self.task_id).first_or_404()
        #默认处理 将返回数据全部存入字典中
        if self.deal_method == '1':
            task.depend_data_dict = deal_default(task.depend_data_dict,self.interface_return)
        #通过key找到value 再给value赋一个新key 存到task的字典中
        elif self.deal_method == '2':
            l = self.need_position.split(')')
            for i in l:
                if i:
                    key = i[1:].split(',')
                    task.depend_data_dict = deal_default(task.depend_data_dict, self.interface_return,key[0],key[1])
        #传入正则表达式 为其指定key
        elif self.deal_method == '3':
            l = self.need_position.split(')')
            for i in l:
                if i:
                    key = i[1:].split(',')
                    p = self.interface_return
                    task.depend_data_dict[key[0]] = re.findall(key[1],json.dumps(self.interface_return, ensure_ascii=False))[0]

        return task.depend_data_dict

    #获取当前任务的依赖用例列表
    def get_dependent_case_list(self):
        dependent_case_list = []
        dependent_case = db.session.query(TaskCase.dependent_case).filter_by(task_id=self.task_id).all()
        for i in dependent_case:
            dependent_case_list = dependent_case_list + i[0].split(',')

        return dependent_case_list

    #判断当前的一条任务是否需要执行
    def run_or_not(self,has_run_list):
        if self.case_id in has_run_list:
            return False
        else:
            if self.is_run == True:
                return True
            elif self.is_run == False:
                #判断case_id是否在被依赖列表中，如果在则强制执行
                dependent_case_list = self.get_dependent_case_list()
                if self.case_id in dependent_case_list:
                    return True
                else:
                    return False

    #将一个task 的case记录中is_new字段置为False
    @classmethod
    def set_is_new_false(cls,task_id):
        cases = Case.query.filter_by(task_id=task_id,is_new=True).all()
        for c in cases:
            c.is_new = False
            with db.auto_commit():
                db.session.add(c)

    #分页查询一个任务最新的执行记录
    @classmethod
    def paginate_query_new(cls,task_id,page=1):
        pagination = Case.query.filter_by(is_new=True,task_id=task_id).paginate(page,current_app.config['PAGE_NUM'],error_out=False)
        cases = pagination.items
        pages = pagination.pages
        total = pagination.total

        return cls.paginate(cases,page,pages,total)

    #分页条件模糊查询
    @classmethod
    def paginate_query(cls,page,task_id,case_name,url,is_new,user_name,task_name,result,startDate,endDate):
        case_name = case_name.strip() if case_name else case_name
        url = url.strip() if url else url
        if startDate:
            startDate = datetime.datetime.strptime(startDate, "%Y-%m-%d %H:%M:%S")
        if startDate:
            endDate = datetime.datetime.strptime(endDate, "%Y-%m-%d %H:%M:%S")
        if int(is_new) == 1:
            is_new = True
        elif int(is_new) == 0:
            is_new = False
        if int(result) == 1:
            result = True
        elif int(result) == 0:
            result = False
        user_name = user_name.strip() if user_name else user_name
        users = USER.query.filter(USER.nickname.like("%" + user_name + "%") if user_name is not None else "").all()
        user_list=[]
        if users:
            for user in users:
                user_list.append(user.id)
        tasks = Task.query.filter(Task.name.like("%" + task_name + "%") if task_name is not None else "").all()
        task_list=[]
        if tasks:
            for task in tasks:
                task_list.append(task.id)
        pagination = Case.query.filter(Case.status == 1,
                                       Case.is_new == is_new if (is_new==True or is_new==False) else "",
                                       Case.actual_result == result if (result==True or result==False) else "",
                                       Case.user_id.in_(user_list) if users is not [] else "",
                                       Case.task_id.in_(task_list) if tasks is not [] else "",
                                       Case.case_name.like("%" + case_name + "%") if case_name is not None else "",
                                       Case.url.like("%" + url + "%") if url is not None else "",
                                       Case.task_id == task_id if task_id is not None else "",
                                       Case.create_time.between(startDate,endDate) if startDate else ""
                                       ).\
            paginate(int(page), current_app.config['PAGE_NUM'],error_out=False)

        cases = pagination.items
        pages = pagination.pages
        total = pagination.total
        page = pagination.page

        return cls.paginate(cases, page, pages, total)

    #该方法用于查询一条用例的详情
    def get_case_detail(self):
        case = Case.query.filter_by(id=self.id).first_or_404()
        if case.user_id:
            user=USER.query.filter_by(id=case.user_id).first_or_404()
            case.user_name = user.nickname
        else:
            case.user_name = '郭家兴'
        task = Task.query.filter_by(id=case.task_id).first_or_404()
        case.task_name = task.name

        return case







