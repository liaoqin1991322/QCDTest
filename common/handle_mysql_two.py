import pymysql
from common.handle_conf import conf


class HandleDB:
    def __init__(self):
        self.con = pymysql.connect(host=conf.get('mysql', 'host'),
                                   port=conf.getint('mysql', 'port'),
                                   user=conf.get('mysql', 'user'),
                                   password=conf.get('mysql', 'password'),
                                   charset='utf8',
                                   # cursorclass=pymysql.cursors.DictCursor
                                   )

    def find_all(self, sql):
        """查询查询到的所有数据"""
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        return res

    def find_one(self, sql):
        """查询一条数据"""
        cur = self.con.cursor()
        cur.execute(sql)
        res = cur.fetchone()
        cur.close()
        return res

    def find_count(self, sql):
        """sql执行完之后，返回的数据条数"""
        with self.con as cur:
            res = cur.execute(sql)
        cur.close()
        return res

    def __del__(self):
        self.con.close()
