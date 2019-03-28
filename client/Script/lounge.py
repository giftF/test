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

# a = pygame.font.get_fonts()
# for i in a:
#     print(i)
class Role:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        self.sur_name = deploy.g_font.render(self.name, True, (255, 255, 255))


def pck_handler(pck):
    p = Protocol(pck)
    pck_type = p.get_str()

    if pck_type == 'playermove':  # 玩家移动的数据包
        x = p.get_int32()
        y = p.get_int32()
        name = p.get_str()
        for r in deploy.g_other_player:
            if r.name == name:
                r.x = x
                r.y = y
                break
    elif pck_type == 'newplayer':  # 新玩家数据包
        x = p.get_int32()
        y = p.get_int32()
        name = p.get_str()
        r = Role(x, y, name)
        deploy.g_other_player.append(r)
    elif pck_type == 'logout':  # 玩家掉线
        name = p.get_str()
        for r in deploy.g_other_player:
            if r.name == name:
                deploy.g_other_player.remove(r)
                break


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

def send_new_role():
    """
    告诉服务端有新玩家加入
    """
    # 构建数据包
    p = Protocol()
    p.add_str("newrole")
    p.add_int32(0)
    p.add_int32(0)
    p.add_str(deploy.g_player.name)
    data = p.get_pck_has_head()
    # 发送数据包
    deploy.g_client.sendall(data)

def lounge():
    pygame.init()
    # Configuration file
    window_size = (800, 600)
    # screen = pygame.display.set_mode(window_size, 0, 32)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('取个名字吧！')

    message_box = []  # Create a message box
    # back_image = pygame.image.load('test.jpg').convert()
    while True:
        break_switch = False
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            screen.fill((255, 255, 255))  # background color
            # screen.blit(back_image, (400, 100))
            # message box .....................................................................
            screen.set_clip(270, 300, 300, 50)  # message box's location
            screen.fill((47, 79, 79))  # message box's color
            x, y = pygame.mouse.get_pos()
            if 200 < x < 500 and 300 < y < 350:
                # print('mouse in the box')
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
            screen.blit(gameOverSurf, gameOverRect)
            deploy.g_player = Role(randint(100, 500), randint(100, 300), text)
            screen.blit(deploy.g_font.render(text, True, (255, 255, 255)), (360, 315))




            # screen.blit(font_family.render(IP_name, True, (255, 255, 255)), (280, 310))
            # screen.blit(font_family.render(text, True, (255, 255, 255)), (360, 310))
            # submit button ...................................................................
            screen.set_clip(270, 370, 300, 50)  # submit button's location
            screen.fill((47, 79, 79))  # submit button's color

            gameOverSurf = deploy.g_font.render('开始', True, (255, 255, 255))
            gameOverRect = gameOverSurf.get_rect()
            gameOverRect.midtop = (400, 380)
            screen.blit(gameOverSurf, gameOverRect)

            # Login_name = '开始'
            # screen.blit(font_family.render(Login_name, True, (255, 0, 0)), (380, 380))
            if 270 < x < 570 and 370 < y < 420 and event.type == MOUSEBUTTONDOWN:
                screen.set_clip(270, 370, 300, 50)  # submit button's location
                screen.fill((84, 255, 159))  # change the submit button color
                break_switch = True
        pygame.display.update()
        if break_switch:
            '''
            输入名字后，点击开始按钮，关闭当前窗口，创建一个新窗口，并向服务器发送新玩家加入信息
            '''
            deploy.g_client.connect(deploy.ADDRESS)
            # 开始接受服务端消息
            thead = Thread(target=msg_handler)
            thead.setDaemon(True)
            thead.start()
            # 告诉服务端有新玩家
            send_new_role()
            break

def update_view():
    """
    视图更新
    """
    deploy.g_screen.fill((0, 0, 0))
    # 画角色
    deploy.g_screen.blit(deploy.g_player.sur_name, (deploy.g_player.x, deploy.g_player.y - 20))
    deploy.g_screen.blit(deploy.g_sur_role, (deploy.g_player.x, deploy.g_player.y))
    # 画其他角色
    for r in deploy.g_other_player:
        deploy.g_screen.blit(r.sur_name, (r.x, r.y - 20))
        deploy.g_screen.blit(deploy.g_sur_role, (r.x, r.y))
    # 刷新
    pygame.display.flip()

def send_role_move():
    """
    发送角色的坐标给服务端
    """
    # 构建数据包
    p = Protocol()
    p.add_str("move")
    p.add_int32(g_player.x)
    p.add_int32(g_player.y)
    data = p.get_pck_has_head()
    # 发送数据包
    g_client.sendall(data)

def handler_event():
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                g_player.y -= 5
            elif event.key == pygame.K_s:
                g_player.y += 5
            elif event.key == pygame.K_a:
                g_player.x -= 5
            elif event.key == pygame.K_d:
                g_player.x += 5
            send_role_move()  # 告诉服务器，自己移动了

def update_logic():
    """
    逻辑更新
    """
    # 事件处理
    handler_event()

def main_loop():
    """
    游戏主循环
    """
    while True:
        # FPS=60
        pygame.time.delay(32)
        # 逻辑更新
        update_logic()
        # 视图更新
        update_view()

if __name__ == '__main__':
    deploy.ADDRESS = ('127.0.0.1', 8712)  # ('foxyball.cn', 8712)  # 如果服务端在本机，请使用('127.0.0.1', 8712)

    deploy.WIDTH, deploy.HEIGHT = 640, 480  # 窗口大小

    deploy.g_font = None

    deploy.g_screen = None  # 窗口的surface

    deploy.g_sur_role = None  # 人物的role

    deploy.g_player = None  # 玩家操作的角色

    deploy.g_other_player = []  # 其他玩家

    deploy.g_client = socket.socket()  # 创建 socket 对象
    lounge()