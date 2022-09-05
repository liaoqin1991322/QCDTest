"""
coding:utf-8
@Software:新增项目测试类
@Time:2022/8/29 10:16
@Author:liaoqin
"""
import unittest,os,requests
from unittestreport import ddt,list_data
from common.handle_excel import HandleExcel
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.tools import replace_data
from common.handle_assert import AssertDef
from common.handle_log import my_log
from common.handle_mysql import db
from testcases.fixture import BaseFixture

"""
添加项目的前提是需要先登录，所以定义了一个类前置方法
"""

@ddt
class TestAddAudit(unittest.TestCase,BaseFixture):
    #1、从excel中读取数据
    excel = HandleExcel(os.path.join(DATA_DIR,"QCD.xlsx"),"add")
    datas = excel.read_excel_data()

    #2、进行登录
    @classmethod
    def setUpClass(cls):
        """"用于类执行前执行一次登录"""
        cls.user_login()  # 继承BaseTest，就继承了父类的所有属性和方法

    @list_data(datas)
    def test_add(self,item):
        print("member_id：{}".format(self.member_id))
        print("headers：{}".format(self.headers))

        #3、对excel里的用例逐条进行测试
        #获取接口请求链接
        url = conf.get("server_info","server_url")+item['url']
        #获取请求方法
        method = item['method'].lower()
        #预期结果
        expected = eval(item['excepted'])
        print("预期结果：",expected)
        #对参数进行替换
        item['data'] = replace_data(item['data'],TestAddAudit,'#(.+?)#')
        # 获取参数
        params = eval(item['data'])

        if item['check_sql']:
            #请求之前的数据库值，去数据库校验新增的项目有没有成功
            sql = " select count(1) as count from loan t where t.member_id={}".format(self.member_id)
            start_count = db.find_one(sql)['count']
            print("新增项目前的总数为：", start_count)

        #发送请求，得到返回结果
        response = requests.request(method=method,url=url,headers=self.headers,json=params)
        res = response.json()
        print("实际结果：",res)

        if item['check_sql']:
            #去数据库校验新增的项目有没有成功
            end_count = db.find_one(sql)['count']
            print("新增项目后的总数为：",end_count)

        #4、断言
        try:
            asert = AssertDef()
            asert.assertDictIn(expected,res)

            #只对添加项目是否成功来做校验
            if item['check_sql'] and res['msg'] =='OK':
                #断言新增后的总数-新增前的总数相差值为1
                self.assertEqual(float(end_count-start_count),1)

        except  AssertionError as e:
            # 5、写日志
            my_log.error("{}-----用例执行失败".format(item['title']))
            my_log.exception(e)
            raise e
        else:
            #5、写日志
            my_log.info("{}-----用例执行成功".format(item['title']))

