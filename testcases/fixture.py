"""
coding:utf-8
@Software:封装测试用例所需前置（类级别前置、用例级别前置）的方法
@Time:2022/8/30 14:36
@Author:liaoqin
"""
import requests

from jsonpath import jsonpath
from common.handle_conf import conf



class BaseFixture:

    @classmethod
    def admin_login(cls):
        """管理员登录"""
        url = conf.get("server_info", "server_url") + "/member/login"
        admin_params = {
            "mobile_phone": conf.get("test_login", "admin_mobile"),
            "pwd": conf.get("test_login", "admin_pwd")
        }
        admin_header = eval(conf.get("server_info", "headers"))
        admin_response = requests.request(method="post", url=url, json=admin_params, headers=admin_header)
        admin_res = admin_response.json()

        admin_token = jsonpath(admin_res, "$..token")[0]
        admin_header.update({'Authorization': "Bearer " + admin_token})
        cls.admin_member_id = jsonpath(admin_res, "$..id")[0]
        cls.admin_headers = admin_header

    @classmethod
    def user_login(cls):
        """普通用户登录"""
        # 1、准备登录账号和密码
        head = eval(conf.get("server_info", "headers"))
        params = {
            "mobile_phone": conf.get("test_login", "mobile_phone"),
            "pwd": conf.get("test_login", "pwd")
        }
        url = conf.get("server_info", "server_url") + "/member/login"
        # 2、发送请求
        response = requests.request(method="post", url=url, headers=head, json=params)
        res = response.json()
        # 3、提取token和用户id
        token = jsonpath(res, "$..token")[0]  # jsonpath取出来是list，所以取里面的元素

        # ********更新字典方法一*************************************************
        # head['Authorization'] = "Bear " + token
        # *******更新字典方法二**************************************************
        head.update({'Authorization': "Bearer " + token})

        # 4、设置为类属性，方法一
        cls.headers = head
        cls.member_id = jsonpath(res, "$..id")[0]


    @classmethod
    def add_project(cls):
        """添加项目"""
        url = conf.get("server_info", "server_url") + "/loan/add"
        params = {
            "member_id": cls.member_id,
            "title": "测试数据--接口自动化",
            "amount": 200.00,
            "loan_rate": 12.0,
            "loan_term": 12,
            "loan_date_type": 1,
            "bidding_days": 5
        }
        response = requests.request(method="post", url=url, headers=cls.headers, json=params)
        res = response.json()
        cls.loan_id = jsonpath(res, "$..id")[0]

    @classmethod
    def audit_project(cls):
        """审核项目"""
        audit_url = conf.get("server_info", "server_url") + "/loan/audit"
        audit_params = {
            "loan_id": cls.loan_id,
            "approved_or_not": "true"
        }
        audit_response = requests.request(method="patch", url=audit_url, json=audit_params,
                                          headers=cls.admin_headers)  # 用管理员的请求头
        audit_res = audit_response.json()
        print("实际结果：", audit_res)