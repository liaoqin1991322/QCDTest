"""
coding:utf-8
@Software:登录测试类
@Time:2022/8/16 18:02
@Author:liaoqin
"""
import unittest,os,requests

from unittestreport import ddt,list_data
from common.handle_excel import HandleExcel
from common.handle_log import my_log
from common.handle_conf import conf
from common.handle_path import DATA_DIR
from common.handle_assert import AssertDef
from common.tools import replace_data

@ddt
class TestLogin(unittest.TestCase):

    #从excel读数据
    excel = HandleExcel(os.path.join(DATA_DIR,'QCD.xlsx'),'login')
    datas = excel.read_excel_data()
    #路径
    base_url = conf.get("server_info","server_url")
    # 请求头,定义的是字典，采用get获取得到的是字符串，所以需要通过eval转
    headers = eval(conf.get("server_info","headers"))

    @list_data(datas)
    def test_login(self,item):
        # 1、准备测试用例数据
        #接口地址
        login_url = self.base_url + item['url']
        # 行号
        case_id = item['case_id'] +1  #行号
        #预期结果
        excepted = eval(item['excepted']) #因从excel里取出来的数据都是字符串，要转类型需加eval()
        #参数
        #if "#mobile_phone#" in item['data']:
            #替换#mobile_phone#
        item['data'] = replace_data(item['data'],TestLogin,'#(.+?)#')
        params = eval(item['data'])

        #获取请求方法，并转换为小写
        method = item['method'].lower()

        # 2、调用接口请求
        #request可以送所有类型的请求，包括post、get、put等
        response = requests.request(method=method,url=login_url,json=params,headers=self.headers)
        res = response.json()
        print("###预期结果：",excepted)
        print("###实际结果：",res)
        # 实际结果
        try:
            # 3、断言有可能会有错，所以加try...except
            # self.assertEqual(excepted['code'],res['code'])
            # self.assertEqual(excepted['msg'],res['msg'])
            #self.assertDictIn(excepted,res)
            assert_def = AssertDef()
            assert_def.assertDictIn(excepted, res)
        except AssertionError as e:
            # 4、往excel里写结果   【注：根据实际项目需要，如果没有强制要求则不写，因为每条用例频繁写入消耗较大则会很慢】
            # self.excel.write_excel_data(row=case_id, column=8, value="用例失败")
            # 5、写日志
            my_log.error("用例：{} ----用例执行失败".format(item['title']))
            #打印详细的用例失败信息
            my_log.exception(e)
            # 主动抛出异常 【因为unittest执行断言加了try，所有就不会有异常，而执行的用例报告就是通过的。所以需要加上主动抛出异常让unittest误别到这个用例是失败的】
            raise  e
        else:
            # 4、往excel里写结果
            # self.excel.write_excel_data(row=case_id, column=8, value="用例成功")
            # 5、写日志
            my_log.info("用例：{} ----用例执行成功".format(item['title']))
