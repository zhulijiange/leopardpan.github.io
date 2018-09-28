'''
name: Tedu
date: 2018-09-28
email: xxx
modules: pymysql
This is a dict project for AID
'''

from socket import *
import pymysql
import os
import sys
import signal
import time

# 定义需要的全局变量
DICT_TXT = './dict.txt'
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)


# 流程控制
def main():
    # 创建数据库连接
    db = pymysql.connect('localhost', 'root', '123456', 'Dictionary')

    # 创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(ADDR)
    s.listen(5)

    # 忽略子进程信号(处理僵尸进程)
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)

    while True:
        try:
            c, addr = s.accept()
            print('已连接客户端', addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print('服务器异常', e)
            continue

        # 创建子进程
        pid = os.fork()
        if pid == 0:
            s.close()
            s_child(c, db)
        else:
            c.close()
            continue


def s_child(c, db):
    # 循环接收客户端发来的请求
    while True:
        data = c.recv(128).decode()
        print(c.getpeername(), ':', data)
        if not data:
            c.close()
            sys.exit('客户端退出')
        elif data[0] == 'R':
            s_register(c, db, data)
        elif data[0] == 'L':
            s_login(c, db, data)
        elif data[0] == 'Q':
            s_query(c, db, data)
        elif data[0] == 'H':
            s_history(c, db, data)


def s_login(c, db, data):
    print('登录操作')
    L = data.split(' ')
    account = L[1]
    password = L[2]
    cursor = db.cursor()
    # 查询是否存在该用户
    sql = 'select password from user where account = "%s"' % account
    cursor.execute(sql)
    r = cursor.fetchone()
    if r is None:
        c.send(b'ERRORA')
        return
    elif r != (password,):
        c.send(b'ERRORP')
        return
    else:
        c.send(b'OK')
    print('%s登陆成功' % account)


def s_register(c, db, data):
    print('注册操作')
    L = data.split(' ')
    account = L[1]
    password = L[2]
    cursor = db.cursor()
    # 查询是否已存在该用户
    sql = "select * from user where account = '%s'" % account
    cursor.execute(sql)
    r = cursor.fetchone()
    if r is not None:
        c.send(b'EXISTS')
        return
    # 插入该用户
    sql = "insert into user(account, password) values\
           ('%s', '%s')" % (account, password)
    try:
        cursor.execute(sql)
        db.commit()
        c.send(b'OK')
    except Exception:
        db.rollback()
        c.send(b'FALL')
    else:
        print('%s注册成功' % account)


def s_query(c, db, data):
    print('查询操作')
    L = data.split(' ')
    account = L[1]
    word = L[2]
    cursor = db.cursor()

    def insert_history():
        tm = time.ctime()
        sql = "insert into history(account,word,time)\
               values('%s','%s','%s')" % (account, word, tm)
        try:
            cursor.execute(sql)
            db.commit()
        except Exception:
            db.rollback()

    # 文本查询
    try:
        f = open(DICT_TXT)
    except Exception:
        c.send(b'FALL')
        return
    for line in f:
        tmp = line.split(' ')[0]
        if tmp > word:
            c.send(b'FALL')
            f.close()
            return
        elif tmp == word:
            c.send(b'OK')
            time.sleep(0.01)
            c.send(line.encode())
            f.close()
            insert_history()
            return
    c.send(b'FALL')
    f.close()


def s_history(c, db, data):
    print('历史记录')
    L = data.split(' ')
    account = L[1]
    cursor = db.cursor()

    sql = "select * from history where account='%s' limit 10" % account
    cursor.execute(sql)
    h = cursor.fetchall()
    if not h:
        c.send(b'FALL')
        return
    else:
        c.send(b'OK')

    for i in h:
        time.sleep(0.01)
        msg = "%s    %s    %s" % (i[1], i[2], i[3])
        c.send(msg.encode())
    time.sleep(0.01)
    c.send(b'##')


if __name__ == '__main__':
    main()
