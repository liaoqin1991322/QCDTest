"""
coding:utf-8
@Software:封装路径的模块
@Time:2022/8/17 20:11
@Author:liaoqin
"""
import os

#项目的根目录的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#用例数据所在目录
DATA_DIR = os.path.join(BASE_DIR,"datas")

#配置文件所在目录
CONF_DIR = os.path.join(BASE_DIR,"conf")

#日志文件所在目录
LOG_DIR = os.path.join(BASE_DIR,"logs")

#报告所在路径
REPORT_DIR = os.path.join(BASE_DIR,"reports")

#用例模块所在目录
CASE_DIR = os.path.join(BASE_DIR,"testcases")
