#!/usr/bin/env python3
# coding=utf-8
'''
http server v2.0
1. 多线程并发
2. 可以请求简单数据
3. 能进行简单请求解析
4. 结构使用类进行封装
'''
from socket import *
from threading import Thread
import sys
import traceback


# httpserver类 封装具体的服务器功能
class HTTPServer(object):
    def __init__(self, server_addr, static_dir):
        # 增添服务器对象属性
        self.server_address = server_addr
        self.static_dir = static_dir
        self.ip = server_addr[0]
        self.port = server_addr[1]
        # 创建套接字
        self.create_socket()

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(self.server_address)

    def serve_forever(self):
        self.sockfd.listen(5)
        print('Listen the port %d' % self.port)
        while True:
            try:
                connfd, addr = self.sockfd.accept()
            except KeyboardInterrupt:
                self.sockfd.close()
                sys.exit("服务器退出")
            except Exception:
                traceback.print_exc()
                continue
            # 创建新的线程处理请求
            clientThread = Thread(target=self.handlerRequest,
                                  args=(connfd,))
            clientThread.setDaemon(True)
            clientThread.start()

    # 具体的客户端请求函数
    def handlerRequest(self, connfd):
        # 接收客户端请求
        request = connfd.recv(4096)
        # 解析请求内容
        requestHeaders = request.splitlines()
        print(connfd.getpeername(), ":", requestHeaders[0])
        # 获取具体请求内容
        getRequest = str(requestHeaders[0]).split(' ')[1]
        # 请求静态页面
        if getRequest == '/' or getRequest[-5:] == '.html':
            self.get_html(connfd, getRequest)
        # 请求数据
        else:
            self.get_data(connfd, getRequest)
        connfd.close()

    # 请求静态页面
    def get_html(self, connfd, getRequest):
        if getRequest == '/':
            filename = self.static_dir + '/index.html'
        else:
            filename = self.static_dir + getRequest
        try:
            f = open(filename)
        except IOError:
            # 没有找到页面
            responseHeaders = "HTTP/1.1 404 NOT FOUND\r\n"
            responseHeaders += "\r\n"  # 空行
            responseBody = "===SORRY NOT FOUND==="
        else:
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += "\r\n"  # 空行
            responseBody = f.read()
        finally:
            # 发送给浏览器
            response = responseHeaders + responseBody
            connfd.send(response.encode())

    # 请求数据
    def get_data(self, connfd, getRequest):
        urls = ['/time', '/tedu', '/python']

        if getRequest in urls:
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += "\r\n"  # 空行
            if getRequest == '/time':
                import time
                responseBody = time.ctime()
            elif getRequest == '/tedu':
                responseBody = 'Welcome to tedu'
            elif getRequest == '/python':
                responseBody = '人生苦短我用python'
        else:
            responseHeaders = "HTTP/1.1 404 NOT FOUND\r\n"
            responseHeaders += "\r\n"  # 空行
            responseBody = "===SORRY NOT FOUND==="
        response = responseHeaders + responseBody
        connfd.send(response.encode())


if __name__ == "__main__":
    # 服务器IP
    server_addr = ("0.0.0.0", 8080)
    # 我的静态页面存储目录static
    static_dir = './static'

    # 生成对象
    httpd = HTTPServer(server_addr, static_dir)
    # 启动服务器
    httpd.serve_forever()
