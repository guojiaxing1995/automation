""" 
@Time    : 2018/7/26 20:44
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : task.py
@Desc    : 任务模型
"""

from sqlalchemy import Column, Integer, ForeignKey, String, orm
from app.models.base import Base, db


class Task(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    description = Column(String(300))
    request_header = Column(String(40))
    #依赖数据字典 存放被处理过的接口返回数据，供所需接口使用
    depend_data_dict = {}

    @orm.reconstructor
    def __init__(self):
        self.__return_json = ['id','name','description','request_header']

    def keys(self):
        return self.__return_json

    def set_keys(self, *args):
        return_json = [str(arg) for arg in args]
        self.__return_json = return_json

    @classmethod
    def is_name_exist(cls,name):
        task = Task.query.filter_by(name=name).first()
        if task:
            return True
        else:
            return False

    def add_task(self,name,description,request_header):
        with db.auto_commit():
            self.name = name
            self.description = description
            self.request_header = request_header
            db.session.add(self)

    #判断任务是否允许被删除
    def allow_delete(self):
        pass


    def get_all_task(self):
        tasks = Task.query.all()

        return tasks





