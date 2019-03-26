# #coding=utf-8
# import socket
# BUF_SIZE = 1024
# host = 'localhost'
# port = 8082
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((host, port))
# server.listen(10) #并发数
# while True:
#     client, address = server.accept()
#     data = client.recv(BUF_SIZE)
#     client.send(data)
#     print(data.decode()) #python3 要使用decode
#     client.close()


# coding=utf-8
'''
server端
长连接，短连接，心跳
'''
import socket
import time

BUF_SIZE = 1024
host = 'localhost'
port = 8083

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)  # 接收的连接数
client, address = server.accept()  # 因为设置了接收连接数为1，所以不需要放在循环中接收
while True:  # 循环收发数据包，长连接
    time.sleep(10)
    data = client.recv(BUF_SIZE)
    print(data.decode())  # python3 要使用decode
    a = str(time.time()).encode()
    client.send(a)
    # client.close() #连接不断开，长连接