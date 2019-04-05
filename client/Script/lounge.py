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
from Script.wait_room import wait_room

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
            deploy.g_client.connect(deploy.ADDRESS)
            # 开始接受服务端消息
            wait_room(text)
