""" 
@Time    : 2018/8/5 11:05
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : task.py
@Desc    : 任务相关 视图函数
"""
from flask import jsonify, url_for

from app import app
from app.libs.error_code import RepeatFailed, Success
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.record_report import recordReport
from app.models.scheduler import Scheduler
from app.models.task import Task
from app.models.task_case import TaskCase
from app.validators.case_forms import CaseDetailForm
from app.validators.task_forms import TaskForm, TaskCaseForm, UpdateTaskCaseForm, TaskCaseFormBase, DeleteTaskCaseForm, \
    ReportForm, SchedulerAddForm, SchedulerUpdateForm, SchedulerPauseForm

api = Redprint('task')

#添加task
@api.route('/addTask',methods=['POST'])
def add_Task():
    form = TaskForm().validate_for_api()
    if Task.is_name_exist(form.name.data):
        raise RepeatFailed()
    else:
        task = Task()
        task.add_task(form.name.data,form.description.data,form.request_header.data)

    return Success()

@api.route('/updateTask',methods=['POST'])
def update_task():
    form = TaskForm().validate_for_api()
    task = Task.query.filter_by(name=form.name.data).first_or_404()
    with db.auto_commit():
        task.description = form.description.data
        task.request_header = form.request_header.data

    return Success()

@api.route('/allTask',methods=['GET'])
def get_all_task():
    tasks = Task.query.all()

    return jsonify(tasks)

@api.route('/addTaskCase',methods=['POST'])
def add_task_case():
    form = TaskCaseForm().validate_for_api()
    task_case = TaskCase()
    task_case.add_task_case(form.case_name.data,form.is_run.data,form.method.data,form.url.data,form.header.data,form.deal_method.data,
                            form.dependent_case.data,form.need_position.data,form.submission.data,form.data.data,form.expect_result.data,form.task_id.data)

    return Success()

@api.route('/updateTaskCase',methods=['POST'])
def update_task_case():
    form = UpdateTaskCaseForm().validate_for_api()
    task_case = TaskCase.query.filter_by(case_id=form.case_id.data).first_or_404()
    task_case.update_task_case(form.case_name.data,form.is_run.data,form.method.data,form.url.data,form.header.data,form.deal_method.data,
                            form.dependent_case.data,form.need_position.data,form.submission.data,form.data.data,form.expect_result.data,form.task_id.data)

    return Success()

#根据task_id和case_id等条件获取task_case
@api.route('/getTaskCase',methods=['GET'])
def get_task_case():
    form = TaskCaseFormBase().validate_for_api()
    if form.case_id.data:
        task_cases = TaskCase.paginate_query(form.task_id.data,1,form.case_id.data)
    else:
        task_cases = TaskCase.paginate_query(form.task_id.data,form.page.data,form.case_id.data,form.case_name.data,form.url.data)

    return jsonify(task_cases)

@api.route('/deleteTaskCase',methods=['GET'])
def delete_task_case():
    form = DeleteTaskCaseForm().validate_for_api()
    task_case = TaskCase()
    task_case.case_id = form.case_id.data
    task_case.delete_task_case()

    return Success()

#传入task_id 获取该任务下的case_id列表
@api.route('/getCaseIdByTaskId',methods=['GET'])
def get_case_id_by_task_id():
    form = TaskCaseFormBase().validate_for_api()
    task_case = TaskCase()
    task_case.task_id = form.task_id.data
    case_id_list = task_case.get_case_id_list()

    return jsonify(case_id_list)

@api.route('/getReportDate',methods=['GET'])
def get_report_date():
    form = ReportForm().validate_for_api()
    record_report = recordReport()
    record_report.task_id = form.task_id.data
    record_report.record_date = form.report_date.data
    report = record_report.report_date()

    return jsonify(report)


@api.route('/addJob',methods=['POST'])
def add_job():
    url = url_for('v1.interface+spider_batch', _external=True)
    form = SchedulerAddForm().validate_for_api()
    scheduler = Scheduler()
    scheduler.task_id = form.task_id.data
    scheduler.day_of_week = form.day_of_week.data
    scheduler.hour = form.hour.data
    scheduler.minute = form.minute.data
    scheduler.user_id = form.user_id.data
    scheduler.copy_person = form.copy_person.data
    scheduler.add_scheduler()
    scheduler.add_job(url)

    return Success()

@api.route('/startJob')
def start_job():
    form = SchedulerPauseForm().validate_for_api()
    scheduler = Scheduler()
    scheduler.scheduler_id = form.scheduler_id.data
    scheduler.resume_job()

    return Success()

@api.route('/deleteJob')
def delete_job():
    form = SchedulerPauseForm().validate_for_api()
    scheduler = Scheduler()
    scheduler.scheduler_id = form.scheduler_id.data
    scheduler.delete_job()
    scheduler.delete_scheduler()

    return Success()

@api.route('/getJobs')
def get_job():
    scheduler = Scheduler()
    jobs = scheduler.all_jobs()

    return  jsonify(jobs)

@api.route('/updateJob',methods=['POST'])
def update_job():
    form = SchedulerUpdateForm().validate_for_api()
    scheduler = Scheduler()
    scheduler.update_scheduler(form.scheduler_id.data,form.user_id.data,form.day_of_week.data,form.hour.data,form.minute.data,form.copy_person.data)
    scheduler.scheduler_id = form.scheduler_id.data
    scheduler.hour = form.hour.data
    scheduler.minute = form.minute.data
    scheduler.day_of_week = form.day_of_week.data
    scheduler.modify_job()

    return Success()

@api.route('/pauseJob')
def pause_job():
    form = SchedulerPauseForm().validate_for_api()
    scheduler = Scheduler()
    scheduler.scheduler_id = form.scheduler_id.data
    scheduler.pause_job()

    return Success()

@api.route('/TaskCaseItemsMini')
def task_case_items():
    task_case = TaskCase()
    items = task_case.task_case_items()

    return jsonify(items)

@api.route('/getCaseById')
def get_case_by_id():
    form = CaseDetailForm().validate_for_api()
    if form.id.data == -1:
        case = TaskCase.query.filter_by(case_id=form.case_id.data).first_or_404()
    else:
        case = TaskCase.query.filter_by(id=form.id.data).first_or_404()

    return jsonify(case)





