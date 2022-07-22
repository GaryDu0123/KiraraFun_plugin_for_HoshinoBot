import random

from hoshino import util
from .chara import roster


class Gacha(object):

    def __init__(self, pool_name: str = "MIX"):
        super().__init__()
        self.pool_name = pool_name
        self.tenjou_line = 250
        # self.tenjou_rate = '24.54%'
        # self.memo_pieces = 200 if (pool_name == 'JP' or pool_name == 'MIX') else 100
        self.load_pool(pool_name)

    def load_pool(self, pool_name: str):
        config = util.load_config(__file__)
        pool = config[pool_name]
        self.up_prob = pool["up_prob"]
        self.s5_prob = pool["s5_prob"]
        self.s4_prob = pool["s4_prob"]
        self.s1_prob = 1000 - self.s4_prob - self.s5_prob
        self.up = pool["up"]
        self.star5 = pool["star5"]
        self.star4 = pool["star4"]
        self.star3 = pool["star3"]

    def gacha_one(self, up_prob: int, s5_prob: int, s4_prob: int, s3_prob: int = None):
        '''
        sx_prob: x星概率，要求和为1000
        up_prob: UP角色概率（从5星划出）
        up_chara: UP角色名列表

        return: (单抽结果:Chara, 抽到5星的数量:int)
        ---------------------------
        |up|      |  20  |   78   |
        |   ***   |  **  |    *   |
        ---------------------------
        '''
        if s3_prob is None:
            s3_prob = 1000 - s5_prob - s4_prob
        total_ = s5_prob + s4_prob + s3_prob
        pick = random.randint(1, total_)
        if pick <= up_prob:
            return roster.chara_list["5"][random.choice(self.up)], 5, True
        elif pick <= s5_prob:
            return roster.chara_list["5"][random.choice(self.star5)], 5, False
        elif pick <= s4_prob + s5_prob:
            return roster.chara_list["4"][random.choice(self.star4)], 4, False
        else:
            return roster.chara_list["3"][random.choice(self.star3)], 3, False

    def gacha_ten(self):
        result = []
        number_of_star_5 = 0
        up = self.up_prob
        s3 = self.s5_prob
        s2 = self.s4_prob
        s1 = 1000 - s3 - s2
        for _ in range(9):  # 前9连
            c, y, is_up = self.gacha_one(up, s3, s2, s1)
            result.append(c)
            if y == 5:
                number_of_star_5 += 1
        c, y, is_up = self.gacha_one(up, s3, s2 + s1, 0)  # 保底第10抽
        result.append(c)
        if y == 5:
            number_of_star_5 += 1
        return result, number_of_star_5

    def gacha_tenjou(self):
        total_div_10 = self.tenjou_line // 10
        result = {'up': [], 's5': [], 's4': [], 's3': []}
        first_up_pos = 999999
        up = self.up_prob
        s5 = self.s5_prob
        s4 = self.s4_prob
        s3 = 1000 - s5 - s4
        for i in range(9 * total_div_10):
            c, y, is_up = self.gacha_one(up, s5, s4, s3)
            if is_up:
                result['up'].append(c)
                first_up_pos = min(first_up_pos, 10 * ((i + 1) // 9) + ((i + 1) % 9))
            elif 5 == y:
                result['s5'].append(c)
            elif 4 == y:
                result['s4'].append(c)
            elif 3 == y:
                result['s3'].append(c)
            else:
                pass  # should never reach here
        for i in range(total_div_10):
            c, y, is_up = self.gacha_one(up, s5, s4 + s3, 0)
            if is_up:
                result['up'].append(c)
                first_up_pos = min(first_up_pos, 10 * (i + 1))
            elif 5 == y:
                result['s5'].append(c)
            elif 4 == y:
                result['s4'].append(c)
            else:
                pass  # should never reach here
        result['first_up_pos'] = first_up_pos
        return result
