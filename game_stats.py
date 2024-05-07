
class GameStats:
    #跟踪游戏统计信息

    def __init__(self, ai_game):
        #初始化信息
        self.settings = ai_game.settings
        self.reset_stats()
        #最高分
        self.high_score = 0

    def reset_stats(self):
        #初始化游戏运行时可能变化的信息
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

