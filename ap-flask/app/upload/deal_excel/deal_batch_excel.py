""" 
@Time    : 2018/8/29 19:34
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : deal_batch_excel.py
@Desc    :
"""
from http.client import HTTPException

from app.libs.error_code import DateNullError
from app.libs.opreation_excel import OperationExcel
from app.models.task_case import TaskCase
from app.upload.deal_excel.batch_excel_data import execelColumn


class dealBatchExcel():

    def __init__(self,path):
        self.opera_excel = OperationExcel(path)
        self.workbook = self.opera_excel.get_workbook(path)
        self.table = self.opera_excel.get_table(self.workbook)

    def get_task(self):
        task_name = self.opera_excel.get_cell_value(self.table,0,1)
        task_url = self.opera_excel.get_cell_value(self.table,0,3)
        task_description = self.opera_excel.get_cell_value(self.table, 0, 5)

        if task_name=='':
            raise DateNullError()

        return task_name,task_url,task_description

    def get_case_line(self):
        case_line = self.opera_excel.get_rows(self.table)
        return case_line

    def add_task_case(self,task_id):
        lines = self.get_case_line()
        for i in range(2, lines):
            case_name = self.opera_excel.get_cell_value(self.table,i,execelColumn.getcolumn_case_name())
            is_run = self.opera_excel.get_cell_value(self.table, i, execelColumn.getcolumn_isrun())
            method = self.opera_excel.get_cell_value(self.table, i, execelColumn.getcolumn_method())
            url = self.opera_excel.get_cell_value(self.table, i, execelColumn.getcolumn_URL())
            header = self.opera_excel.get_cell_value(self.table, i, execelColumn.getcolumn_header())
            deal_method = self.opera_excel.get_cell_value(self.table, i, execelColumn.getcolumn_deal_method())
            dependent_case = self.opera_excel.get_cell_value(self.table, i, execelColumn.getcolumn_depend_case())
            need_position = self.opera_excel.get_cell_value(self.table, i, execelColumn.getcolumn_need_postion())
            submission = self.opera_excel.get_cell_value(self.table, i, execelColumn.getcolumn_submission())
            expect_result = self.opera_excel.get_cell_value(self.table, i, execelColumn.getcolumn_expend_result())
            data = self.opera_excel.get_cell_value(self.table, i, execelColumn.getcolumn_data())
            if is_run=='是':
                is_run = True
            else:
                is_run = False
            task_case = TaskCase()
            task_case.add_task_case(case_name,is_run,method,url,header,deal_method,dependent_case,need_position,submission,data,expect_result,task_id)



