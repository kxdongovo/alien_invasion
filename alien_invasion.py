import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import  Scoreboard
from button import  Button
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
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        #游戏活动状态
        self.game_active = False
        #创建按钮
        self.play_button = Button(self, "Play")


    def run_game(self):
        #开始游戏的住循环
        while True:
            self._check_events()
            if self.game_active:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        #单击按钮开始新游戏
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #还原游戏设置
            self.settings.initialize_dynamic_settings()
            #重置游戏统计信息
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.game_active = True
            #清空外星人和子弹
            self.bullets.empty()
            self.aliens.empty()
            #创建一个新的
            self._create_fleet()
            self.ship.center_ship()
            #隐藏光标
            pygame.mouse.set_visible(False)


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
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # 检查是否有子弹击中了外星人，若击中删除对应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            # 删除子弹创建新外星人
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        #更新外星人位置
        self._check_fleet_edges()
        self.aliens.update()
        #检测外星人和飞船碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #外星人到达飞船边缘
        self._check_aliens_bottom()



    def _update_screen(self):
        # 每次循环都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        #显示得分
        self.sb.show_score()
        #如果游戏处于非活动状态就创建按钮
        if not self.game_active:
            self.play_button.draw_button()
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

    def _ship_hit(self):
        #响应飞船和外星人碰撞
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            #清空外星人和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            #创建新舰队，并将飞船放在屏幕底部中央
            self._create_fleet()
            self.ship.center_ship()
            #暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)


    def _check_aliens_bottom(self):
        #检查是否外星人到达底部边缘
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #像飞船被撞到一样处理
                self._ship_hit()
                break


if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai = AlienIncasion()
    ai.run_game()
