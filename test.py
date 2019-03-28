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
	pygame.display.set_caption(u'基础 pygame 程序')

	# Fill background
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	# Display some text
	#font = pygame.font.Font(None, 60)  #原始代码，使用默认字体，不能显示中文
	#font = pygame.font.Font('../FredGuo/simkai.ttf', 60)  #正确，文件名可以包含路径
	#font = pygame.font.Font('楷体', 60)  #错误，name参数应该是字体的文件名
	font = pygame.font.SysFont('华文楷体', 60)  #正确，name参数应该是字体名，并且字符集要与系统的相同
	text = font.render(u"Hello 我爱你", 1, (10, 10, 10))  #显示内容必须转换成Unicode，否则中文不能正常显示
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