"""
coding:utf-8
@Software:注册测试类
@Time:2022/8/16 18:03
@Author:liaoqin
"""
import unittest,os,requests


from unittestreport import ddt,list_data
from common.handle_excel import HandleExcel
from common.handle_log import my_log
from common.handle_path import DATA_DIR
from common.handle_conf import conf
from common.handle_mysql import db
from common.tools import replace_data,random_phone

@ddt
class TestRegister(unittest.TestCase):

    #从excel读数据
    excel = HandleExcel(os.path.join(DATA_DIR,'QCD.xlsx'),'register')
    datas = excel.read_excel_data()

    headers = eval(conf.get("server_info","headers"))# 请求头,定义的是字典，采用get获取得到的是字符串，所以需要通过eval转
    base_url  = conf.get("server_info","server_url")

    @list_data(datas)
    def test_register(self,item):
        # 1、准备测试用例数据
        #case_id = item['case_id'] +1  #行号
        excepted = eval(item['excepted']) #因从excel里取出来的数据都是字符串，要转类型需加eval()

        method = item['method'].lower()
        url = self.base_url+item['url']

        params = eval(item['data'])
        #判断有需要替换动态参数的数据
        # if "#mobile_phone#" in item['data']:
            #动态替换excel中的参数 #mobile_phone#
            # m_phone = self.randomPhone()
            # params = eval(item['data'].replace("#mobile_phone#",m_phone))

        setattr(TestRegister,'mobile_phone',random_phone())
        item['data'] = replace_data(item['data'], TestRegister, '#(.+?)#')
        params = eval(item['data'])

        #调用接口请求
        response = requests.request(method=method,headers=self.headers,json=params,url=url)
        res = response.json()
        print(params,"预期结果：",excepted)
        print("实际结果：",res)

        #数据库校验有没有插入
        if item['check_sql']:
            sql = "select count(1) from member t where t.mobile_phone='{}'".format(getattr(TestRegister,"mobile_phone"))
            count = db.find_count(sql)

        try:
            # 3、断言
            self.assertEqual(excepted['code'],res['code'])#断言有可能会有错，所以加try...except
            self.assertEqual(excepted['msg'],res['msg'])#断言有可能会有错，所以加try...except
            if item['check_sql']:
                print("{}数据库为：{}".format(getattr(TestRegister,"mobile_phone"),count))
                self.assertEqual(1,count)

        except AssertionError as e:
            # 4、往excel里写结果
            #self.excel.write_excel_data(row=case_id, column=5, value="用例失败")
            # 5、写日志
            my_log.error("用例：{} ----用例失败".format(item['title']))
            #打印详细的用例失败信息
            my_log.exception(e)
            # 主动抛出异常 【因为unittest执行断言加了try，所有就不会有异常，而执行的用例报告就是通过的。所以需要加上主动抛出异常让unittest误别到这个用例是失败的】
            raise  e
        else:
            # 4、往excel里写结果
            #self.excel.write_excel_data(row=case_id, column=5, value="用例成功")
            # 5、写日志
            my_log.info("用例：{} ----用例成功".format(item['title']))

