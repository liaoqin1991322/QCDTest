"""
coding:utf-8
@Software:日志收集器
为避免程序中创建多个日志收集器而导致日志重复记录，使用时就只需导入 这个日志收集器
@Time:2022/8/15 17:20
@Author:liaoqin
"""
import logging,os
from common.handle_path import LOG_DIR
from common.handle_conf import conf

class Log:

    def create_log(self,name,fh_level,sh_level,level,filename):
        # 1、创建日志收集器
        log = logging.getLogger(name)
        # 2、设置日志收集器收集日志的等级
        log.setLevel(level)
        # 3、设置日志输出渠道
        # 3.1、创建一个日志输出的渠道（输出到文件）
        fh = logging.FileHandler(filename, encoding='utf-8')
        fh.setLevel(fh_level)  # 设置输出等级
        log.addHandler(fh)  # 将输出渠道绑定到日志收集器上

        """输出到控制台"""
        # 3.2、创建一个日志输出的渠道（输出到控制台）
        sh = logging.StreamHandler()
        sh.setLevel(sh_level)  # 设置输出等级
        log.addHandler(sh)  # 将输出渠道绑定到日志收集器上

        # 4、设置日志输出的等级,格式     【时间，文件，行号，等级，信息】
        formats = '%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s :%(message)s'
        # 创建格式对象
        log_format = logging.Formatter(formats)
        # 为输出渠道设置输出格式
        sh.setFormatter(log_format)
        fh.setFormatter(log_format)
        # 返回一个日志收集器
        return log

my_log = Log().create_log(
    name = conf.get("logging","name"),
    fh_level = conf.get("logging","fh_level"),
    sh_level = conf.get("logging","sh_level"),
    level = conf.get("logging","level"),
    filename = os.path.join(LOG_DIR,conf.get("logging","filename"))
)
# if __name__ == '__main__':
#     log = create_log('login_case', 'DEBUG', 'DEBUG', level="DEBUG", filename='20220815_log.log')
#     log.debug('---1111')