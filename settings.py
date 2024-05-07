
class Settings:
    #存储游戏中所有设置
    def __init__(self):
        #初始化游戏设置
        #屏幕
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (173, 216, 230)
        #飞船设置
        self.ship_speed = 5.5
        self.ship_limit = 3
        #子弹设置
        self.bullet_speed = 8.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (0, 0, 0)
        #外星人设置
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        #1向左移动， -1向右移动
        self.fleet_direction = 1
