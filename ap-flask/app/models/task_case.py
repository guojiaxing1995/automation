""" 
@Time    : 2018/7/26 20:47
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : task_case.py
@Desc    : 任务用例模型
"""
from flask import current_app
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, orm
from sqlalchemy.orm import relationship

from app.libs.error_code import CaseIsDepend
from app.models.base import Base, db
from app.models.task import Task


class TaskCase(Base):
    id = Column(Integer, primary_key=True)
    case_id = Column(String(25),default="")
    case_name = Column(String(50), nullable=False)
    is_run = Column(Boolean, nullable=False)
    method = Column(String(4), nullable=False)
    url = Column(String(500), nullable=False)
    header = Column(String(500))
    deal_method = Column(String(200))
    dependent_case = Column(String(200),default="")
    need_position = Column(String(100))
    # 0 表单提交 1 json提交
    submission = Column(String(2))
    data = Column(String(2000))
    expect_result = Column(String(2000))
    task = relationship('Task')
    task_id = Column(Integer, ForeignKey('task.id'))

    @orm.reconstructor
    def __init__(self):
        self.__return_json = ['id', 'case_id', 'case_name','is_run','method','url','header','deal_method','dependent_case','need_position','submission','data','expect_result','task_id']

    def keys(self):
        return self.__return_json

    def set_keys(self, *args):
        return_json = [str(arg) for arg in args]
        self.__return_json = return_json

    def add_task_case(self,case_name,is_run,method,url,header,deal_method,dependent_case,need_position,submission,data,expect_result,task_id):
        with db.auto_commit():
            self.case_name = case_name
            self.method = method
            self.is_run = is_run
            self.url = url
            self.header = header
            self.deal_method = deal_method
            self.dependent_case = dependent_case
            self.need_position = need_position
            self.submission = submission
            self.data = data
            self.expect_result = expect_result
            self.task_id = task_id
            task_cases = db.session.query(TaskCase).filter(TaskCase.status.in_(('0','1')),TaskCase.task_id==task_id).all()
            task = Task.query.filter_by(id=task_id).first_or_404()
            self.case_id = task.name + '_' + str(len(task_cases)+1)
            db.session.add(self)


    def update_task_case(self, case_name, is_run, method, url, header, deal_method, dependent_case, need_position,submission, data, expect_result, task_id):
        with db.auto_commit():
            self.case_name = case_name
            self.method = method
            self.is_run = is_run
            self.url = url
            self.header = header
            self.deal_method = deal_method
            self.dependent_case = dependent_case
            self.need_position = need_position
            self.submission = submission
            self.data = data
            self.expect_result = expect_result
            self.task_id = task_id

    # 传入task_id 获取该任务下的case_id列表
    def get_case_id_list(self):
        case_id_list = []
        task_cases = TaskCase.query.filter_by(task_id=self.task_id).all()
        if task_cases:
            for case in task_cases:
                case_id_list.append(case.case_id)

        return case_id_list

    #获取依赖用例列表
    def get_dependent_case_list(self):
        dependent_case_list = []
        #status 为0 表示已被删除
        dependent_case = db.session.query(TaskCase.dependent_case).filter(TaskCase.status=='1').all()
        for i in dependent_case:
            dependent_case_list = dependent_case_list + i[0].split(',')

        return dependent_case_list

    #判断用例是否允许被删除
    def allow_delete(self):
        dependent_case_list = self.get_dependent_case_list()
        if self.case_id in dependent_case_list:
            return False
        else:
            return True

    def task_case_items(self):
        task = Task()
        task_case = TaskCase()
        tasks = task.get_all_task()
        items = []
        for i in tasks:
            task = {}
            task['text'] = i.name
            cases = task_case.query.filter_by(task_id=i.id).all()
            children = []
            for c in cases:
                case = {}
                case['id'] = c.id
                case['text'] = c.case_name
                children.append(case)
            task['children'] = children
            items.append(task)
        return items


    def delete_task_case(self):
        if self.allow_delete():
            with db.auto_commit():
                TaskCase.query.filter_by(case_id=self.case_id).first_or_404().delete()
                from app.models.case import Case
                cases = Case.query.filter_by(case_id=self.case_id).all()
                for case in cases:
                    case.delete()
        else:
            raise CaseIsDepend()

    #根据task_id和case_id获取task_case
    @classmethod
    def paginate_query(cls, task_id,page,case_id,case_name=None,url=None):
        task_id = task_id.strip() if task_id else task_id
        case_id = case_id.strip() if case_id else case_id
        case_name = case_name.strip() if case_name else case_name
        url = url.strip() if url else url

        if case_id:
            task_case = TaskCase.query.filter_by(task_id=task_id, case_id=case_id).first_or_404()
            return task_case
        else:
            pagination = TaskCase.query.filter(TaskCase.task_id==task_id,TaskCase.status==1,TaskCase.case_name.like("%"+case_name+"%") if case_name is not None else ""
                                               ,TaskCase.url.like("%"+url+"%") if url is not None else "").paginate(int(page), current_app.config['PAGE_NUM'],
                                                                                     error_out=False)
            cases = pagination.items
            pages = pagination.pages
            total = pagination.total
            page = pagination.page

            return cls.paginate(cases, page, pages, total)






