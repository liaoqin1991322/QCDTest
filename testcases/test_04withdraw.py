"""
coding:utf-8
@Software:提现测试用例类
@Time:2022/8/22 9:53
@Author:liaoqin
"""
import unittest, os, requests
from unittestreport import ddt, list_data
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_assert import AssertDef
from common.handle_log import my_log
from common.tools import replace_data
from testcases.fixture import BaseFixture

@ddt
class TestWithDraw(unittest.TestCase,BaseFixture):
    # 1、读取测试用例数据
    excel = HandleExcel(os.path.join(DATA_DIR, "QCD.xlsx"), "withdraw")
    datas = excel.read_excel_data()

    # 2、先进行登录后获取token和用户id,以便于提现接口用例使用
    @classmethod
    def setUpClass(cls):
        """用于类执行前执行一次登录"""
        cls.user_login()  # 继承BaseTest，就继承了父类的所有属性和方法

    @list_data(datas)
    def test_with_draw(self, item):
        # 3、准备测试用例数据
        url = conf.get("server_info", "server_url") + item['url']
        method = item['method'].lower()
        excepted = eval(item['excepted'])
        #params = eval(item['data'])
        # if "#member_id#" in item['data']:
            # 3.1、动态设置excel中参数属性
            # params = eval(item['data'].replace("#member_id#", str(self.member_id)))

        item['data'] = replace_data(item['data'], TestWithDraw, '#(.+?)#')
        params = eval(item['data'])

        # 4、准备发送请求
        response = requests.request(method=method, url=url, json=params, headers=self.headers)
        res = response.json()
        print("###预期结果：", excepted)
        print("###实际结果：", res)
        # 5、断言
        try:
            assert_def = AssertDef()
            assert_def.assertDictIn(excepted,res)
        except AssertionError as e:
            my_log.info("用例：{} ----执行失败".format(item['title']))
            my_log.exception(e)
            raise e
        else:
            # 6、写入日志
            my_log.info("用例：{} ----执行成功".format(item['title']))
