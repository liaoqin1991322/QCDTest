"""
coding:utf-8
@Software:工具类
@Time:2022/8/27 15:33
@Author:liaoqin
"""
import re, random
from common.handle_conf import conf


def replace_data(data, cls, re_ex):
    """
    动态替换字符串中多个参数的数据
    :param data: 要进行替换的用例数据（字符串）
    :param cls: 测试类
    :param re_ex:正则表达式(字符串)
    :return:
    """
    while re.search(re_ex, data):
        res2 = re.search(re_ex, data)  # search匹配到返回对象，没有匹配到返回None
        item = res2.group()  # 获取被替换的内容
        attr = res2.group(1)  # 获取用于类属性
        try:
            value = getattr(cls, attr)  # 从类属性里获取属性
        except AttributeError:
            value = conf.get("test_login", "mobile_phone")  # 如果类属性没有报错，则从配置文件里获取
        # 替换
        data = data.replace(item, str(value))  # 将类属性的值替换给item

    return data


def random_phone():
    """随机生成一个手机号,11位"""
    return str(random.randint(13300000000, 13399999999))

# 测试如下
# class TestCase:
#     id = 123
#     name = '张三'
#     data = '1111'
#     title = '用正则和类属性替换字符串的的参数'

# if __name__ == '__main__':
#     s = '{"id":"#id#","name":"#name#","data":"#data#","title":"#title#"}'
#     s = replace_data(s,TestCase,'#(.+?)#')
#     print(s)
