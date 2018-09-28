from pymysql import connect


class MysqlHelp:
    def __init__(self, database, host="127.0.0.1",
                 user="root", password="123456",
                 charset="utf8", port=3306):
        self.database = database
        self.host = host
        self.user = user
        self.password = password
        self.charset = charset
        self.port = port

    # 连接数据库方法
    def open(self):
        # 创建连接对象conn
        self.conn = connect(host=self.host,
                            user=self.user,
                            password=self.password,
                            database=self.database,
                            charset=self.charset,
                            port=self.port)
        # 创建游标对象cur
        self.cur = self.conn.cursor()

    # 关闭数据库方法
    def close(self):
        self.cur.close()
        self.conn.close()

    # 执行sql语句方法
    def Exe(self, sql, L=[]):
        self.open()
        try:
            self.cur.execute(sql, L)
            self.conn.commit()
            # print("Ok")
        except Exception:
            self.conn.rollback()
            # print("Failed", e)
        self.close()

    # 查询方法
    def getAll(self, sql, L=[]):
        self.open()
        try:
            self.cur.execute(sql, L)
            # print("Ok")
            result = self.cur.fetchall()
        except Exception:
            self.conn.rollback()
            # print("Failed", e)
        self.close()
        return result


# if __name__ == "__main__":
#     # 测试
