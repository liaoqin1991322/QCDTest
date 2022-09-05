"""
coding:utf-8
@Software:项目投资测试类
@Time:2022/8/29 12:18
@Author:liaoqin
"""
import unittest,requests

import os
from unittestreport import ddt,list_data
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import my_log
from common.tools import replace_data
from common.handle_assert import AssertDef
from common.handle_mysql import db
from testcases.fixture import BaseFixture
"""
    投资项目：
        1、管理员登录  （类级别前置），用于审核项目
        2、创建项目  （用例级别前置）
            #创建项目前需要用普通用户登录
        3、对项目进行审核  （用例级别前置） 因需求只有审核通过的项目才可进行投资
"""
@ddt
class TestInvest(unittest.TestCase,BaseFixture):
    # 1、从excel中读取数据
    excel = HandleExcel(os.path.join(DATA_DIR, "QCD.xlsx"), "invest")
    datas = excel.read_excel_data()

    # 2、进行登录
    @classmethod
    def setUpClass(cls):
        """类前置用例，类读取一次"""
        cls.admin_login()
        cls.user_login()

    def setUp(self):
        """setUp会在每条用例执行之前都会执行--添加项目"""

        #-------------添加项目---------------
        self.add_project()
        #---------审核项目----------
        self.audit_project()

    @list_data(datas)
    def test_invest(self,item):
        print("  loan_id：{}   ---   用户id为：{} ---管理员请求头为：{} ".format(self.loan_id,self.member_id,self.headers))


        # 3、对excel里的用例逐条进行测试
        # 获取接口请求链接
        url = conf.get("server_info", "server_url") + item['url']
        # 获取请求方法
        method = item['method'].lower()
        # 预期结果
        expected = eval(item['excepted'])
        print("预期结果：", expected)
        # 对参数进行替换
        item['data'] = replace_data(item['data'], TestInvest, '#(.+?)#')
        # 获取参数
        params = eval(item['data'])

        # 发送请求，得到返回结果
        response = requests.request(method=method, url=url, headers=self.headers, json=params)
        res = response.json()
        print("实际结果：", res)


        # 4、断言
        try:
            asert = AssertDef()
            asert.assertDictIn(expected, res)

            if res['msg'] == 'OK' and item['check_sql'] == 1:
                # 请求之前的数据库值，去数据库校投资的项目有没有成功
                sql = " select count(*) from invest i where i.member_id={} and i.loan_id={}".format(self.member_id, self.loan_id)
                start_count = db.find_count(sql)
                self.assertEqual(start_count,1)

        except  AssertionError as e:
            # 5、写日志
            my_log.error("{}-----用例执行失败".format(item['title']))
            my_log.exception(e)
            raise e
        else:
            # 5、写日志
            my_log.info("{}-----用例执行成功".format(item['title']))
