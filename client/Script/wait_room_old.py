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

# 设置直线的坐标
points = [(200, 75), (300, 25), (400, 75)]

def wait_room():
    # pygame.init()
    window_size = (800, 600)
    # screen = pygame.display.set_mode(window_size, 0, 32)
    deploy.screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()
    pygame.display.set_caption('房间001')

    xx = 0
    while True:
        for event in pygame.event.get():
            # 查找关闭窗口事件
            if event.type == QUIT:
                sys.exit()

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
        for i in range(1,5):
            WJ = deploy.g_font.render('玩家%s' % i, True, (0, 0, 0))
            WJ1 = WJ.get_rect()
            WJ1.midtop = (70, x + ((i - 1) * 100))
            deploy.screen.blit(WJ, WJ1)

            ZZ = deploy.g_font.render('种族', True, (0, 0, 0))
            ZZ1 = ZZ.get_rect()
            ZZ1.midtop = (290, x + ((i - 1) * 100))
            deploy.screen.blit(ZZ, ZZ1)

        if xx == 0:
            xx += 1
            for i in deploy.g_other_player:
                print('x : %s ' % i.x)
                print('y : %s ' % i.y)
                print('name : %s ' % i.name)
                print('number : %s ' % i.number)
                print('my : %s ' % i.my)
                print('reca : %s ' % i.reca)
                print('troops : %s ' % i.troops)

        for i in deploy.g_other_player:
            WJMZ = deploy.g_font.render('%s' % i.name, True, (0, 0, 0))
            WJMZ1 = WJMZ.get_rect()
            WJMZ1.midtop = (20, x + 50 + ((int(i.number) - 1) * 100))
            deploy.screen.blit(WJMZ, WJMZ1)

            WJZZ = deploy.g_font.render('%s' % i.reca, True, (0, 0, 0))
            WJZZ1 = WJZZ.get_rect()
            WJZZ1.midtop = (290, x + 50 + ((int(i.number) - 1) * 100))
            deploy.screen.blit(WJZZ, WJZZ1)



        # 刷新图s
        pygame.display.flip()

        clock.tick(60)