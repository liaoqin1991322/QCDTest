"""
coding:utf-8
@Software:连接mysql操作类
@Time:2022/8/25 11:01
@Author:liaoqin
"""
import pymysql
from common.handle_conf import conf


class HandleDB:

    def __init__(self, host, port, user, password, database, *args, **kwargs):
        self.con = pymysql.connect(host=host,
                                   port=port,
                                   user=user,
                                   password=password,
                                   database=database,
                                   charset='utf8',
                                   cursorclass=pymysql.cursors.DictCursor,  # 设置游标对象返回的数据类型字典，默认是元组
                                   *args, **kwargs
                                   )

    def find_one(self, sql):
        """查询一条数据"""
        #只支持0.9.3以前的pymsql
        # with self.con.cursor() as cur:
        #     cur.execute(sql)
        #     res = cur.fetchone()
        # cur.close()
        # return res


        #只支持0.9.3之后的pymysql
        cur = self.con.cursor()
        cur.execute(sql)
        res = cur.fetchone()
        self.con.commit()
        cur.close()
        return res

    def find_all(self, sql):
        """查询所有数据"""
        # with self.con.cursor() as cur:
        #     cur.execute(sql)
        #     res = cur.fetchall()
        # cur.close()

        # 只支持0.9.3以前的pymsql
        cur = self.con.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        self.con.commit()
        cur.close()
        return res

    def find_count(self, sql):
        """查询查询到的条数"""
        # with self.con.cursor() as cur:
        #     res = cur.execute(sql)
        # cur.close()

        # 只支持0.9.3以前的pymsql
        cur = self.con.cursor()
        res = cur.execute(sql)
        self.con.commit()
        cur.close()
        return res

    def __del__(self):
        """对象销毁时自动执行"""
        self.con.close()

db = HandleDB(conf.get("mysql", "host"),
              conf.getint("mysql", "port"),
              conf.get("mysql", "user"),
              conf.get("mysql", "password"),
              conf.get("mysql", "database")
              )

# if __name__ == '__main__':
#     py_sql = "select leave_amount from member t  where t.mobile_phone=13888887788"
#     db = HandleDB(conf.get("mysql", "host"), int(conf.get("mysql", "port")), conf.get("mysql", "user"),
#                   conf.get("mysql", "password"), conf.get("mysql", "database"))
#     res1 = db.find_one(py_sql)
#     # # res1 = db.find_all(py_sql)
#     # #res1 = db.find_count(py_sql)
#     print(res1['leave_amount'],type(res1))

