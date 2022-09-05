"""
coding:utf-8
@Software:所有用例执行的入口类
@Time:2022/8/16 18:02
@Author:liaoqin
"""
import unittest,time,os


from unittestreport import TestRunner
from common.handle_path import CASE_DIR,REPORT_DIR


class RunTest:

    @staticmethod
    def main():
        # 1、加载用例到测试套件
        suite = unittest.defaultTestLoader.discover(CASE_DIR)
        # 2、创建测试运行程序
        filename = time.strftime("%Y%m%d%H%M%S")+"_report.html"
        runner = TestRunner(suite,
                            filename=filename,
                            tester='liaoqin',
                            report_dir=REPORT_DIR,
                            title='QCD测试项目--测试生成的报告',
                            desc="测试项目--测试生成的报告")
        # 3、运行用例，生成测试报告
        runner.run()

        #4、将测试结果发送到邮件
        # runner.send_email(host='smtp.qq.com',
        #                   port=465,
        #                   user='403483118@qq.com',
        #                   password='zffoxmpoqghhbiig',
        #                   to_addrs=['975801281@qq.com','403483118@qq.com'],
        #                   is_file=True)

        # #4、将测试结果发送到钉钉
        # webhook = 'https://oapi.dingtalk.com/robot/send?access_token=700050cd7d0d8d4f5adafbf1e23066fa249c432d766e700a4f8c57c7d9eae3d0'
        # runner.dingtalk_notice(url=webhook,
        #                        key='测试',
        #                        atMobiles=[18974229479],
        #                        secret='SECa47ca8a0748f0f7778b4476195553c6e0e8c3e55a3bcfc68a14f53f782ba4475')

if __name__ == '__main__':
    test = RunTest()
    test.main()