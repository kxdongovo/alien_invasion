import sys

import pygame
from settings import Settings


class AlienIncasion:
    #管理游戏资源的行为的类

    def __init__(self):
        #初始化游戏并创建资源
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height
        ))
        pygame.display.set_caption("Alien Invasion")

        #设置背景色
        self.bg_color = (230, 230, 230)

    def run_game(self):
        #开始游戏的住循环
        while True:
            pygame.display.flip()
            self.clock.tick(60)
            # 监听键盘和鼠标事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #每次循环都重绘屏幕
            self.screen.fill(self.bg_color)

            #让最近绘制的屏幕可见
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienIncasion()
    ai.run_game()
