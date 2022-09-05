"""
coding:utf-8
@Software:
@Time:2022/8/17 14:33
@Author:liaoqin
"""
import os
from configparser import ConfigParser
from common.handle_path import CONF_DIR

class Config(ConfigParser):
    """在创建对象时直接加载配置文件的内容"""

    def __init__(self,conf_file):
        super().__init__() #继承ConfigParser父类的方法
        self.read(conf_file,encoding="utf-8")

conf = Config(os.path.join(CONF_DIR,'config.ini'))