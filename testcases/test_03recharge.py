"""
coding:utf-8
@Software:充值测试类
@Time:2022/8/21 11:31
@Author:liaoqin
"""
import unittest,os,requests
from unittestreport import ddt,list_data
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_log import my_log
from common.handle_assert import AssertDef
from common.handle_mysql import db
from common.tools import replace_data
from testcases.fixture import BaseFixture

@ddt
class TestRecharge(unittest.TestCase,BaseFixture):
    #读取测试数据
    excel = HandleExcel(os.path.join(DATA_DIR, 'QCD.xlsx'), 'recharge')
    datas_excl = excel.read_excel_data()

    @classmethod
    def setUpClass(cls):
        """"用于类执行前执行一次登录"""
        cls.user_login()  # 继承BaseTest，就继承了父类的所有属性和方法


    @list_data(datas_excl)
    def test_recharge(self,item):
        """充值"""
        #pass
        #1、准备用例数据

        # 去数据库查询充值前的余额----
        sql = str(item['check_sql']).format(conf.get("test_login", "mobile_phone"))
        if sql != '1':
            print("sql=", sql)
            # db = HandleDB(conf.get("mysql", "host"), int(conf.get("mysql", "port")), conf.get("mysql", "user"),
            #               conf.get("mysql", "password"), conf.get("mysql", "database"))
            start_money = db.find_one(sql)['leave_amount']
            print("充值前的金额为：", start_money)


        # 获取请求方法，并转换为小写
        method = item['method'].lower()
        url = conf.get("server_info","server_url") + item['url']
        excepted = eval(item['excepted'])

        params = eval(item['data'])
        # 判断有需要替换动态参数的数据
        # if "#member_id#" in item['data']:
        #2、动态替换excel中的参数
        # params = eval(item['data'].replace("#member_id#",str(self.id)))

        item['data'] = replace_data(item['data'], TestRecharge, '#(.+?)#')
        params = eval(item['data'])

        #3、发送接口请求
        response = requests.request(method=method,url=url,json=params,headers=self.headers)
        res = response.json()
        print("###预期结果：", excepted)
        print("###实际结果：", res)

        if sql != '1':
            # 去数据库查询充值后的余额-----
            # db = HandleDB(conf.get("mysql", "host"), int(conf.get("mysql", "port")), conf.get("mysql", "user"),
            #               conf.get("mysql", "password"), conf.get("mysql", "database"))
            end_money = db.find_one(sql)['leave_amount']
            print("充值后的金额为：", end_money)

        #4、断言
        try:
            assert_def = AssertDef()
            assert_def.assertDictIn(excepted,res)

            if sql != '1':
                #断言充值后的金额-充值前的金额是否等于充值金额
                acount = float(end_money-start_money)
                if res['msg'] == 'OK':
                    self.assertEqual(acount,params['amount'])
                else:
                    self.assertEqual(acount,0)

        except AssertionError as e:
            #写日志
            my_log.error("用例：{}----执行失败！".format(item['title']))
            # 打印详细的用例失败信息
            my_log.exception(e)
            # 主动抛出异常 【因为unittest执行断言加了try，所有就不会有异常，而执行的用例报告就是通过的。所以需要加上主动抛出异常让unittest误别到这个用例是失败的】
            raise e
        else:
            my_log.info("用例：{} ----执行成功".format(item['title']))



