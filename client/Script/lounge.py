import random
import sys
import time
from random import randint
from threading import Thread
import deploy

from pygame.locals import *
from sys import exit

import pygame
import socket  # 导入 socket 模块

from base import Protocol

def pck_handler(pck):
    p = Protocol(pck)
    try:
        pck_type = p.get_str()
        if pck_type == "games":
            try:
                deploy.games = eval(p.get_str())
                # print(time.time())
                # print(deploy.games)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

def msg_handler():
    """
    处理服务端返回的消息
    """
    while True:
        bytes = deploy.g_client.recv(1024)
        # 以包长度切割封包
        while True:
            # 读取包长度
            length_pck = int.from_bytes(bytes[:4], byteorder='little')
            # 截取封包
            pck = bytes[4:4 + length_pck]
            # 删除已经读取的字节
            bytes = bytes[4 + length_pck:]
            # 把封包交给处理函数
            pck_handler(pck)
            # 如果bytes没数据了，就跳出循环
            if len(bytes) == 0:
                break

def send_new_role(name):
    """
    告诉服务端有新玩家加入
    """
    # 构建数据包
    p = Protocol()
    # 请求名称，用来区分该请求执行的操作
    p.add_str("newuser")
    # 传入角色的名字
    p.add_str(name)
    data = p.get_pck_has_head()
    # 发送数据包
    deploy.g_client.sendall(data)

def lounge():
    window_size = (800, 600)
    deploy.screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('房间')
    message_box = []  # Create a message box
    while True:
        break_switch = False
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            deploy.screen.fill((255, 255, 255))  # background color
            deploy.screen.set_clip(270, 300, 300, 50)  # message box's location
            deploy.screen.fill((47, 79, 79))  # message box's color
            x, y = pygame.mouse.get_pos()
            if 200 < x < 500 and 300 < y < 350:
                if event.type == KEYDOWN:
                    key_num = event.key
                    if key_num == 8 and len(message_box) is not 0:
                        message_box.pop()  # delete the last value
                    elif key_num in deploy.keyCode.keys():
                        message_box.append(deploy.keyCode[key_num])
            text = ''.join(message_box)  # join the list value to a string
            deploy.g_font = pygame.font.Font('bb2117/HWKT.ttf', 26)
            gameOverSurf = deploy.g_font.render('昵称：', True, (255, 255, 255))
            gameOverRect = gameOverSurf.get_rect()
            gameOverRect.midtop = (320, 305)
            deploy.screen.blit(gameOverSurf, gameOverRect)
            deploy.screen.blit(deploy.g_font.render(text, True, (255, 255, 255)), (360, 315))
            deploy.screen.set_clip(270, 370, 300, 50)  # submit button's location
            deploy.screen.fill((47, 79, 79))  # submit button's color
            gameOverSurf = deploy.g_font.render('开始', True, (255, 255, 255))
            gameOverRect = gameOverSurf.get_rect()
            gameOverRect.midtop = (400, 380)
            deploy.screen.blit(gameOverSurf, gameOverRect)
            if 270 < x < 570 and 370 < y < 420 and event.type == MOUSEBUTTONDOWN:
                deploy.screen.set_clip(270, 370, 300, 50)  # submit button's location
                deploy.screen.fill((84, 255, 159))  # change the submit button color
                break_switch = True
        pygame.display.update()
        if break_switch:
            '''
            输入名字后，点击开始按钮，关闭当前窗口，创建一个新窗口，并向服务器发送新玩家加入信息
            '''
            break_switch = False
            deploy.g_client.connect(deploy.ADDRESS)
            # 开始接受服务端消息
            thead = Thread(target=msg_handler)
            thead.setDaemon(True)
            thead.start()
            # 告诉服务端有新玩家
            send_new_role(text)
            break