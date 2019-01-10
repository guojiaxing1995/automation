""" 
@Time    : 2018/7/26 21:11
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : interface.py
@Desc    :
"""
import datetime
import json
import os

from flask import jsonify, request, current_app, send_from_directory

from app.libs.error_code import FileTypeError
from app.libs.redprint import Redprint
from app.models.case import Case
from app.models.record_report import recordReport
from app.models.task import Task
from app.models.task_case import TaskCase
from app.upload.deal_excel.deal_batch_excel import dealBatchExcel
from app.validators.case_forms import CaseForm, CaseBatchForm, CaseSearchForm, CaseDetailForm

api = Redprint('interface')

#该视图函数用于简单的接口调用
@api.route('/spider',methods=['POST'])
def run_requests():
    form = CaseForm().validate_for_api()
    case = Case()
    case.case_name = form.case_name.data
    case.method = form.method.data
    case.url = form.url.data
    case.header = form.header.data
    case.data = form.data.data
    case.submission = form.submission.data
    case.expect_result = form.expect_result.data
    case.pass_or_fail()
    #将返回数据格式化为字符串
    if isinstance(case.data,dict):
        case.data = json.dumps(case.data, ensure_ascii=False)
    if isinstance(case.header, dict):
        case.header = json.dumps(case.header, ensure_ascii=False)

    case.set_keys('case_name','method','url','header','data','submission','expect_result','actual_result','interface_return')

    return jsonify(case)

@api.route('/downloadTemplet',methods=['GET'])
def download_templet():
    filename = 'spiderBatchTemple.xlsx'
    dirpath = os.path.join(current_app.root_path, 'download')
    dirpath = dirpath.replace('\\','/')
    return send_from_directory(dirpath, filename, as_attachment=True)

@api.route('/upload',methods=['POST'])
def upload():
    file = request.files['file']
    ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])
    if file:
        if '.' in file.filename and file.filename.rsplit('.', 1)[1] not in ALLOWED_EXTENSIONS:
            raise FileTypeError()
        else:
            dirpath = os.path.join(current_app.root_path, 'upload')
            dirpath = dirpath.replace('\\', '/')
            now = datetime.datetime.now().strftime('%Y-%m-%d')
            path = dirpath + r'/task' + now + '.xls'
            file.save(path)
            #解析excel
            deal_excel = dealBatchExcel(path)
            task_name, task_url, task_description = deal_excel.get_task()
            task = Task.query.filter_by(name=task_name).all()
            #如果上传文件中的task不存在，则新增一个task
            if not task:
                task = Task()
                task.add_task(task_name,task_description,task_url)
            task = Task.query.filter_by(name=task_name).first_or_404()
            deal_excel.add_task_case(task.id)

    return jsonify(task)

@api.route('/searchCase',methods=['POST'])
def search_case():
    form = CaseSearchForm().validate_for_api()
    search_result = Case.paginate_query(form.page.data,form.task_id.data,form.case_name.data,form.url.data,form.is_new.data,form.user_name.data,form.task_name.data,
                                        form.result.data,form.startDate.data,form.endDate.data)
    return jsonify(search_result)

@api.route('/getCaseDetail',methods=['Get'])
def case_detail():
    form = CaseDetailForm().validate_for_api()
    case = Case()
    case.id = form.id.data
    detail = case.get_case_detail()
    detail.set_keys('case_id','case_name','is_run','method','url','header','deal_method','dependent_case',
                              'need_position','submission','data','expect_result','actual_result','interface_return','task_name','user_name','is_new')
    return jsonify(detail)

@api.route('/spider/batch',methods=['POST'])
def spider_batch():
    form = CaseBatchForm().validate_for_api()
    #将之前的最后一次执行记录设置为非最后一次执行记录
    Case.set_is_new_false(form.task_id.data)
    task_cases = TaskCase.query.filter_by(task_id=form.task_id.data).all()
    #需要执行的case列表
    case_list = []
    for task_case in task_cases:
        case = Case()
        case.case_id = task_case.case_id
        case.case_name = task_case.case_name
        case.is_run = task_case.is_run
        case.method = task_case.method
        case.url = task_case.url
        case.header = task_case.header
        case.deal_method = task_case.deal_method
        case.dependent_case = task_case.dependent_case
        case.need_position = task_case.need_position
        case.submission = task_case.submission
        case.data = task_case.data
        case.expect_result = task_case.expect_result
        case.task = task_case.task
        case.task_id = task_case.task_id
        case.task_case_id = task_case.id
        case_list.append(case)
    #已经执行过的case列表
    has_run_list = []
    for case in case_list:
        has_run_list = execute_one_case(case,has_run_list,case_list)

    total = len(case_list)
    has_run = len(has_run_list)
    fail_num = 0
    for case in case_list:
        if case.actual_result=='0':
            fail_num += 1
    pass_num = has_run-fail_num
    pass_probability = format(float(pass_num)/float(has_run)*100,'.2f')
    fail_probability = format(float(fail_num)/float(has_run)*100,'.2f')
    execute_probability = format(float(has_run)/float(total)*100,'.2f')
    # pass_probability = ("%.2f" % pass_probability)
    # fail_probability = ("%.2f" % fail_probability)
    # execute_probability = ("%.2f" % execute_probability)

    record_report = recordReport()
    record_report.record_date = datetime.datetime.now().strftime('%Y-%m-%d')
    record_report.task_id = form.task_id.data
    if record_report.add_or_update():
        record_report.add(form.task_id.data,pass_num,fail_num,has_run,total,pass_probability,fail_probability,execute_probability,record_report.record_date)
    else:
        record_report.update(form.task_id.data,pass_num,fail_num,has_run,total,pass_probability,fail_probability,execute_probability,record_report.record_date)

    result = {
        "total":total,
        "has_run":has_run,
        "pass_num":pass_num,
        "fail_num":fail_num,
        "pass_probability":pass_probability,
        "fail_probability":fail_probability,
        "execute_probability":execute_probability
    }

    return jsonify(result)

def execute_one_case(case,has_run_list,case_list):
    # 判断用例是否需要执行
    if case.run_or_not(has_run_list):
        #has_run_list.append(case.case_id)
        #判断该用例的依赖用例是否执行
        if case.dependent_case:
            for depend in case.dependent_case.split(','):
                if depend not in has_run_list:
                    for c in case_list:
                        if depend == c.case_id:
                            dependent_case = c
                            execute_one_case(dependent_case,has_run_list,case_list)
        #执行
        case.spider_batch()

        has_run_list.append(case.case_id)
        current_app.logger.info(case.case_id)
        current_app.logger.info(has_run_list)


    return has_run_list

