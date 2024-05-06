import sys

import pygame

from settings import Settings
from ship import Ship


class AlienIncasion:
    #管理游戏资源的行为的类

    def __init__(self):
        #初始化游戏并创建资源
        pygame.init()
        self.clock = pygame.time.Clock()
        #引入settings
        self.settings = Settings()
        self.screen = pygame.display.set_mode((
           self.settings.screen_width,
           self.settings.screen_height
        ))
        pygame.display.set_caption("Alien Invasion")
        self.ship = Ship(self)


    def run_game(self):
        #开始游戏的住循环
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(60)


            #让最近绘制的屏幕可见
            pygame.display.flip()
            self.clock.tick(60)

    def _check_events(self):
        #响应按键和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_screen(self):
        # 每次循环都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        pygame.display.flip()



if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienIncasion()
    ai.run_game()
