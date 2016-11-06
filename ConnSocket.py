#!/usr/bin/env python
#-*- coding:utf-8 -*-

from socket import *
import struct
import sys


reload(sys)
sys.setdefaultencoding("utf-8")

str_log = ""
log_in = []


class doSocket:
    def __init__(self, ADDR=()):  # __init__(self) 相当于类的构造方法
        self.addr = ADDR
        # 建立socket对象
        # AF_INET 服务器之间网络通信
        # SOCK_STREAM 流式socket , for TCP
        self.tcpClientSocket = socket(AF_INET, SOCK_STREAM)
        # 连接到ADDR     ADDR=(HOST,PORT) 是一个元组(('1.1.1.1',123)
        self.tcpClientSocket.connect(self.addr)

    def ourSendMsg(self, msg):
        # 系统报文头两个字节是长度
        HEADSIZE = 2

        msgLen = len(msg)
        # 定义struct的fmt
        fmt = '!cc' + str(msgLen) + 's'

        # 字符串打包成我们系统的格式
        some = struct.pack(fmt, chr(msgLen / 256), chr(msgLen % 256), msg)
        # 将字符串发送到后台
        self.tcpClientSocket.sendall(some)

        # 接收反回报文头，解析字符串返回长度
        recvlen = self.tcpClientSocket.recv(HEADSIZE)
        print 'recvlen = ' + recvlen

        li = struct.unpack('!BB', recvlen)  # 返回一个元组，含两个个元素BB表示两个无符号字符

        # 计算报文长度
        recvlen = li[1] + 256 * li[0]

        # 获取报文长度的返回字符串
        data = self.tcpClientSocket.recv(recvlen)
        # print data
        # 关闭socket
        self.tcpClientSocket.close()

        # 返回报文返回结果
        return data

    def otherSendMsg(self, msg):
        HEADSIZE = 4
        # 建立socket对象
        tcpClientSocket = socket(AF_INET, SOCK_STREAM)
        # 连接到ADDR     ADDR=(HOST,PORT) 是一个元组
        tcpClientSocket.connect(self.addr)

        msgLen = len(msg)

        fmt = '!cc' + str(msgLen) + 's'
        # 字符串打包成我们系统的格式
        some = struct.pack(fmt, chr(msgLen / 256), chr(msgLen % 256), msg)
        # 将字符串发送到后台
        tcpClientSocket.sendall(some)

        # 接收反回报文头，解析字符串返回长度
        recvlen = tcpClientSocket.recv(HEADSIZE)
        print 'recvlen=', recvlen
        li, = struct.unpack('!BB', recvlen)  # 返回一个元组，含两个个元素BB表示两个无符号字符
        print 'li', li
        recvlen = li[1] + 256 * li[0]

        # 获取返回字符串
        reply = tcpClientSocket.recv(recvlen)
        # 关闭socket
        tcpClientSocket.close()

        return reply
