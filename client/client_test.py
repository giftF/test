#coding=utf-8
__author__ = '药师Aric'
'''
client端
长连接，短连接，心跳
'''
import socket
import time
host = 'localhost'
port = 8083
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1) #在客户端开启心跳维护
client.connect((host, port))
while True:
    b = str(time.time())
    client.send('hello world\r\n'.encode())
    print('send data')
    a = client.recv(1024)
    c = str(time.time())
    print(a.decode())
    print(b)
    print(float(a) - float(b))
    time.sleep(1) #如果想验证长时间没发数据，SOCKET连接会不会断开，则可以设置时间长一点