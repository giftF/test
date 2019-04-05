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




# 设置背景颜色和线条颜色
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
messages = []

# 设置直线的坐标
points = [(200, 75), (300, 25), (400, 75)]

isreaddict = {
    'N': '未准备',
    'Y': '已准备'
}

def readying():
    """
    告诉服务端有新玩家加入
    """
    # 构建数据包
    p = Protocol()
    # 请求名称，用来区分该请求执行的操作
    p.add_str("ready")
    # 传入角色的名字
    p.add_str(deploy.user_name)
    p.add_str(deploy.isready)
    data = p.get_pck_has_head()
    # 发送数据包
    deploy.g_client.sendall(data)


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

def pck_handler(pck):
    p = Protocol(pck)
    try:
        pck_type = p.get_str()
        if pck_type == "games":
            try:
                return eval(p.get_str())
                # print(time.time())
                # print(messages[0])
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

isnew = True

def msg_handler():
    """
    处理服务端返回的消息
    """
    global messages
    while True:
        bytes = deploy.g_client.recv(1024)
        text = []
        # 以包长度切割封包
        while True:
            # 读取包长度
            length_pck = int.from_bytes(bytes[:4], byteorder='little')
            # 截取封包
            pck = bytes[4:4 + length_pck]
            # 删除已经读取的字节
            bytes = bytes[4 + length_pck:]
            # 把封包交给处理函数
            text.append(pck_handler(pck))
            # 如果bytes没数据了，就跳出循环
            if len(bytes) == 0:
                break
        if len(text) > 0:
            messages = text

def wait_room(loungetext):
    global isnew
    window_size = (800, 600)
    deploy.screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('房间001')
    while True:
        print(messages)
        time.sleep(1)
        if isnew:
            # 处理服务器返回信息
            thead = Thread(target=msg_handler)
            thead.setDaemon(True)
            thead.start()
            send_new_role(loungetext)
            isnew = False

        for event in pygame.event.get():
            # 查找关闭窗口事件
            if event.type == QUIT:
                sys.exit()
            sx, sy = pygame.mouse.get_pos()
            if deploy.i != False:
                if event.type == MOUSEBUTTONDOWN and 460 < sx < 560 and 40 + (100 * deploy.i) < sy < 40 + (
                        100 * (deploy.i + 1)):
                    readying()
            # 填充背景色
            deploy.screen.fill((255, 255, 255))

            # 画不抗锯齿的一条直线
            pygame.draw.line(deploy.screen, (0, 0, 0), (0, 40), (560, 40), 3)
            pygame.draw.line(deploy.screen, (0, 0, 0), (0, 80), (460, 80), 1)
            pygame.draw.line(deploy.screen, (0, 0, 0), (0, 140), (560, 140), 3)
            pygame.draw.line(deploy.screen, (0, 0, 0), (0, 180), (460, 180), 1)
            pygame.draw.line(deploy.screen, (0, 0, 0), (0, 240), (560, 240), 3)
            pygame.draw.line(deploy.screen, (0, 0, 0), (0, 280), (460, 280), 1)
            pygame.draw.line(deploy.screen, (0, 0, 0), (0, 340), (560, 340), 3)
            pygame.draw.line(deploy.screen, (0, 0, 0), (0, 380), (460, 380), 1)
            pygame.draw.line(deploy.screen, (0, 0, 0), (0, 440), (560, 440), 3)
            pygame.draw.line(deploy.screen, (0, 0, 0), (0, 600), (800, 600), 3)
            pygame.draw.line(deploy.screen, (0, 0, 0), (160, 40), (160, 440), 1)
            pygame.draw.line(deploy.screen, (0, 0, 0), (460, 40), (460, 440), 1)
            pygame.draw.line(deploy.screen, (0, 0, 0), (560, 0), (560, 600), 3)
            pygame.font.Font('bb2117/HWKT.ttf', 26)
            x = 45
            try:
                users = messages[0]['users']
                talk = messages[0]['talk']
                for i in range(len(users)):
                    WJ = deploy.g_font.render('玩家%s' % (i+1), True, (0, 0, 0))
                    WJ1 = WJ.get_rect()
                    WJ1.midtop = (70, x + (i * 100))
                    deploy.screen.blit(WJ, WJ1)
                    ZZ = deploy.g_font.render('种族', True, (0, 0, 0))
                    ZZ1 = ZZ.get_rect()
                    ZZ1.midtop = (290, x + (i * 100))
                    deploy.screen.blit(ZZ, ZZ1)
                    WJMZ = deploy.g_font.render('%s' % users[i]['name'][:-1], True, (0, 0, 0))
                    WJMZ1 = WJMZ.get_rect()
                    WJMZ1.midtop = (20, x + 50 + (i * 100))
                    deploy.screen.blit(WJMZ, WJMZ1)
                    WJZZ = deploy.g_font.render('%s' % users[i]['race'], True, (0, 0, 0))
                    WJZZ1 = WJZZ.get_rect()
                    WJZZ1.midtop = (290, x + 50 + (i * 100))
                    deploy.screen.blit(WJZZ, WJZZ1)
                    IR = deploy.g_font.render('%s' % isreaddict[users[i]['isready']], True, (0, 0, 0))
                    IR1 = IR.get_rect()
                    IR1.midtop = (510, x + 25 + (i * 100))
                    deploy.screen.blit(IR, IR1)
                    if users[i]['my'] == 'Y':
                        deploy.user_name = users[i]['name']
                        deploy.i = i
                        deploy.isready = users[i]['isready']
            except Exception as e:
                print(e)
            # 刷新图s
            pygame.display.flip()
            clock.tick(60)