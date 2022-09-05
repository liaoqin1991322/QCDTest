"""
coding:utf-8
@Software:登录类
@Time:2022/8/16 18:02
@Author:liaoqin
"""
import unittest,os
from unittestreport import ddt,list_data
from common.handle_excel import HandleExcel
from login_func import login_check
from common.handle_log import my_log
from common.handle_path import DATA_DIR

@ddt
class TestLogin(unittest.TestCase):

    #从excel读数据
    excel = HandleExcel(os.path.join(DATA_DIR,'test_case03.xlsx'),'login')
    datas = excel.read_excel_data()

    @list_data(datas)
    def test_login(self,item):
        # 1、准备测试用例数据
        case_id = item['case_id'] +1  #行号
        excepted = eval(item['excepted']) #因从excel里取出来的数据都是字符串，要转类型需加eval()
        param = eval(item['param'])
        # 2、调用方法（请求接口）
        result = login_check(**param)
        try:
            # 3、断言
            self.assertEqual(excepted,result)#断言有可能会有错，所以加try...except
        except AssertionError as e:
            # 4、往excel里写结果
            self.excel.write_excel_data(row=case_id, column=5, value="用例失败")
            # 5、写日志
            my_log.error("用例：{} ----用例失败".format(item['title']))
            #打印详细的用例失败信息
            my_log.exception(e)
            # 主动抛出异常 【因为unittest执行断言加了try，所有就不会有异常，而执行的用例报告就是通过的。所以需要加上主动抛出异常让unittest误别到这个用例是失败的】
            raise  e
        else:
            # 4、往excel里写结果
            self.excel.write_excel_data(row=case_id, column=5, value="用例成功")
            # 5、写日志
            my_log.error("用例：{} ----用例成功".format(item['title']))