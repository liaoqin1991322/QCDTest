"""
coding:utf-8
@Software:项目审核测试类
@Time:2022/8/29 12:18
@Author:liaoqin
"""
import unittest, os, requests
from unittestreport import ddt, list_data
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.tools import replace_data
from common.handle_log import my_log
from common.handle_assert import AssertDef
from common.handle_mysql import  db
from testcases.fixture import BaseFixture

"""
审核项目功能
  ---1、管理员登录去审核项目  （登录一次就够了。 所以是类级别前置方法）
  ---2、普通用户登录去创建一个项目
        普通用户登录  （登录一次就够了。 所以是类级别前置方法）
        创建一个项目  （每执行用例前都应该创建一个项目。所以是用例级别前置方法）
"""


@ddt
class TestAudit(unittest.TestCase,BaseFixture):
    excel = HandleExcel(os.path.join(DATA_DIR, "QCD.xlsx"), "audit")
    datas = excel.read_excel_data()

    @classmethod
    def setUpClass(cls):
        """类前置"，管理员和普通用户都只执行一次登录方法"""
        #-----管理员登录---------
        cls.admin_login()
        #-----普通用户登录-------------
        cls.user_login()

    def setUp(self):
        """setUp会在每条用例执行之前都会执行--添加项目"""
        self.add_project()


    @list_data(datas)
    def test_audit(self, item):
        print("  loan_id：{}   ---   用户id为：{} ---管理员请求头为：{} ".format(self.loan_id,self.member_id,self.admin_headers))
        print("  普通用户请求头为：{} ".format(self.loan_id,self.member_id,self.headers))

        url = conf.get("server_info", "server_url") + "/loan/audit"
        method = item['method'].lower()

        item['data'] = replace_data(item['data'],TestAudit,'#(.+?)#')
        params = eval(item['data'])

        expected = eval(item['excepted'])
        print("预期结果：",expected)

        response = requests.request(method=method, url=url, json=params, headers=self.admin_headers)#用管理员的请求头
        res = response.json()
        print("实际结果：",res)
        try:
            asert = AssertDef()
            asert.assertDictIn(expected,res)

            #判断是否审核通过，如果审核通过，则保存loan_id为下一个测试用例使用
            if res['msg'] == 'OK':
                setattr(TestAudit,"pass_loan_id",getattr(TestAudit,"loan_id"))
                #验证数据库中这条数据是否为审核通过的
                item['check_sql'] = replace_data(item['check_sql'],TestAudit,'#(.+?)#')
                count = db.find_one(item['check_sql'])['count']
                self.assertEqual(1,int(count))


        except AssertionError as e:
            my_log.error("{}----用例执行失败".format(item['title']))
            my_log.exception(e)
            raise e
        else:
            my_log.info("{}----用例执行成功".format(item['title']))