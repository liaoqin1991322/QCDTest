"""
coding:utf-8
@Software:自定义断言类
@Time:2022/8/22 8:39
@Author:liaoqin
"""
class AssertDef:

    def assertDictIn(self,expected,res):
        """自定义断言来判断：预期结果是否包含在返回的结果中"""
        #例如预期结果：{'code': 0, 'msg': 'OK'}
        #实际结果为: {'code': 0, 'msg': 'OK', 'data': None, 'copyright': 'C'}
        for k, v in expected.items():
            if res.get(k) == v:
                pass
            else:
                raise AssertionError("{} not in {}".format(expected,res))