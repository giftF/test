import random
import sys
import time
from random import randint
from threading import Thread
import deploy

from Script.lounge import lounge
from Script.wait_room import wait_room
import pygame
import socket  # 导入 socket 模块

from base import Protocol

# 连接服务器
deploy.ADDRESS = ('127.0.0.1', 8712)  # ('foxyball.cn', 8712)  # 如果服务端在本机，请使用('127.0.0.1', 8712)

deploy.WIDTH, deploy.HEIGHT = 640, 480  # 窗口大小

deploy.g_font = None

deploy.g_screen = None  # 窗口的surface

deploy.g_sur_role = None  # 人物的role

# deploy.g_users = None  # 玩家信息

deploy.g_layer = []  # 玩家信息

deploy.g_client = socket.socket()  # 创建 socket 对象


if __name__ == '__main__':
    # 初始化窗口
    pygame.init()
    # 输入名称
    lounge()
    # 进入等待室
    wait_room()