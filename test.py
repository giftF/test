# -*- coding: gbk -*-

import pygame
from pygame.locals import *

a = pygame.font.get_fonts()
for i in a:
    print(i)

def main():
	# Initialise screen
	pygame.init()
	screen = pygame.display.set_mode((650, 150))
	pygame.display.set_caption(u'���� pygame ����')

	# Fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	# Display some text
	#font = pygame.font.Font(None, 60)  #ԭʼ���룬ʹ��Ĭ�����壬������ʾ����
	#font = pygame.font.Font('../FredGuo/simkai.ttf', 60)  #��ȷ���ļ������԰���·��
	#font = pygame.font.Font('����', 60)  #����name����Ӧ����������ļ���
	font = pygame.font.SysFont('���Ŀ���', 60)  #��ȷ��name����Ӧ�����������������ַ���Ҫ��ϵͳ����ͬ
	text = font.render(u"Hello �Ұ���", 1, (10, 10, 10))  #��ʾ���ݱ���ת����Unicode���������Ĳ���������ʾ
	textpos = text.get_rect()
	textpos.center = background.get_rect().center
	background.blit(text, textpos)

	# Blit everything to the screen
	screen.blit(background, (0, 0))
	pygame.display.flip()

	# Event loop
	while 1:
		for event in pygame.event.get():
			if event.type == QUIT:
				return

		screen.blit(background, (0, 0))
		pygame.display.flip()


if __name__ == '__main__':main()