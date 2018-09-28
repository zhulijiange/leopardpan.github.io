#!/usr/bin/python3
# coding=utf-8
from socket import *
from getpass import getpass
import sys


# 创建网络连接
def main():
    if len(sys.argv) < 3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    ADDR = (HOST, PORT)
    s = socket()
    try:
        s.connect(ADDR)
    except Exception as e:
        print('连接错误', e)
        return

    while True:
        print('''
            ==========欢迎界面===========
            -- 1.注册  2.登录  3.退出 --
            =============================
            ''')
        cmd = input('输入选项:')
        if cmd == '1':
            r = c_register(s)
            if r == 0:
                print('注册成功')
            elif r == 1:
                print('用户名已存在')
            else:
                print('注册失败')

        elif cmd == '2':
            account = c_login(s)
            if type(account) is str:
                print('登录成功')
                c_second(s, account)
            elif account == 1:
                print('账户不存在')
            elif account == 2:
                print('密码错误')

        elif cmd == '3':
            s.close()
            sys.exit('bye')
            break
        else:
            print('输入的选项不存在, 请重新输入')
            sys.stdin.flush()  # 清除标准输入
            continue


def c_register(s):
    while True:
        account = input('账号:')
        password = getpass('密码:')
        rpassword = getpass('重复密码:')
        if (' ' in account) or (' ' in password):
            print('账号和密码不允许有空格')
            continue
        if password != rpassword:
            print('两次密码不一致')
            continue
        msg = 'R {} {}'.format(account, password)
        # 发送请求
        s.send(msg.encode())
        # 等待回复
        data = s.recv(128).decode()
        if data == 'OK':
            return 0
        elif data == 'EXISTS':
            return 1
        elif data == 'FALL':
            return 2


def c_login(s):
    while True:
        account = input('账号:')
        password = getpass('密码:')
        if (' ' in account) or (' ' in password):
            print('账号密码错误')
            continue
        msg = 'L {} {}'.format(account, password)
        # 发送请求
        s.send(msg.encode())
        # 等待回复
        data = s.recv(128).decode()
        if data == "OK":
            return account
        elif data == 'ERRORA':
            return 1
        elif data == 'ERRORP':
            return 2


def c_query(s, account):
    while True:
        word = input('单词:')
        if word == '##':
            break
        msg = 'Q {} {}'.format(account, word)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == "OK":
            data = s.recv(2048).decode()
            print(data)
        elif data == 'FALL':
            print('没有查到该单词')


def c_history(s, account):
    msg = 'H {}'.format(account)
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                break
            print(data)
    elif data == 'FALL':
        print('没有历史记录')


def c_second(s, account):
    while True:
        print('''
            ==========查询界面===========
            -- 1.查词  2.历史  3.注销 --
            =============================
            ''')
        cmd = input('输入选项:')
        if cmd == '1':
            c_query(s, account)
        elif cmd == '2':
            c_history(s, account)
        elif cmd == '3':
            return
        else:
            print('输入的选项不存在, 请重新输入')
            sys.stdin.flush()  # 清除标准输入
            continue


if __name__ == '__main__':
    main()
