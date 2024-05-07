import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


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
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()


    def run_game(self):
        #开始游戏的住循环
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        #响应按键和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
         #响应按下
         if event.key == pygame.K_RIGHT:
             self.ship.moving_right = True
         elif event.key == pygame.K_LEFT:
             self.ship.moving_left = True
         elif event.key == pygame.K_q:
             sys.exit()
         elif event.key == pygame.K_SPACE:
             self._fire_bullet()


    def _check_keyup_events(self, event):
        #响应释放
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        #创建一个子弹
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        #更新子弹位置并删除已经消失的子弹
        #更新子弹位置
        self.bullets.update()
        #删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))

    def _update_aliens(self):
        #更新外星人位置
        self._check_fleet_edges()
        self.aliens.update()



    def _update_screen(self):
        # 每次循环都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def _create_fleet(self):
        #创建外星人
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            #添加一行外星人后，重置x并递增y
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        #创建一个外星人将其放在当前行
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        #外星人达到边缘采取措施
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        #改变外星人的移动方向
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1


if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienIncasion()
    ai.run_game()
