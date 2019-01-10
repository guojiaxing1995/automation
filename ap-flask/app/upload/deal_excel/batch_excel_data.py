""" 
@Time    : 2018/8/29 20:04
@Author  : 郭家兴
@Email   : 302802003@qq.com
@File    : batch_excel_data.py
@Desc    :
"""
class execelColumn:

    #用例名称
    CASE_NAME = 0
    # 请求方法
    METHOD = 1
    #是否执行
    IS_RUN = 2
    #url
    URL = 3
    #header
    HEADER = 4
    #提交方式
    SUBMISSION = 5
    #data
    DATA = 6
    # 处理方法
    DEAL_METHOD = 7
    #处理语句
    NEED_POSITION = 8
    #依赖用例
    DEPEND_CASE = 9
    #预期结果
    EXPEND_RESULT = 10


    @classmethod
    def getcolumn_case_name(cls):
        return cls.CASE_NAME

    @classmethod
    def getcolumn_isrun(cls):
        return cls.IS_RUN

    @classmethod
    def getcolumn_method(cls):
        return cls.METHOD

    @classmethod
    def getcolumn_URL(cls):
        return cls.URL

    @classmethod
    def getcolumn_header(cls):
        return cls.HEADER

    @classmethod
    def getcolumn_deal_method(cls):
        return cls.DEAL_METHOD

    @classmethod
    def getcolumn_depend_case(cls):
        return cls.DEPEND_CASE

    @classmethod
    def getcolumn_need_postion(cls):
        return cls.NEED_POSITION

    @classmethod
    def getcolumn_submission(cls):
        return cls.SUBMISSION

    @classmethod
    def getcolumn_data(cls):
        return cls.DATA

    @classmethod
    def getcolumn_expend_result(cls):
        return cls.EXPEND_RESULT

