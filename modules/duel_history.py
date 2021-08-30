import datetime

from peewee import Model, IntegerField, CharField, DateTimeField, SqliteDatabase

from configs.pathConfig import DATABASE_PATH

_TIMEOUT = 60


class DuelHistory(Model):
    """
    记录俄罗斯轮盘的决斗历史，由于每个群同一时间只能有一个决斗存在，因此只需要通过group_id定位即可
    state取值:
    0 -> 决斗邀请阶段
    1 -> 对决开始
    -1 -> 对决被拒绝
    2 -> 决斗结束(无论超时还是被结算)

    in_turn为当前开枪的id
    bullet为8位数，首位为当前第几颗子弹，后7位为弹闸的数字化，1代表有子弹，0代表无子弹
    """
    # 表的结构
    group_id = IntegerField(verbose_name='QQ群号', null=False)
    player1_id = IntegerField(verbose_name='挑战者', default=-1)
    player2_id = IntegerField(verbose_name='被挑战者', default=-1)
    wager = IntegerField(verbose_name='赌注', default=0)
    state = IntegerField(verbose_name='状态', default=0)
    in_turn = IntegerField(verbose_name='裁决者')
    # 为啥要用字符串来记录，因为python的二进制处理实在太蛋疼了
    bullet = CharField(verbose_name='弹闸', default=0)
    order = IntegerField(verbose_name='子弹', default=0)
    probability = IntegerField(verbose_name='中枪概率', default=0)
    last_shot_time = DateTimeField(verbose_name='上次开枪时间', default=0)
    start_time = DateTimeField(verbose_name='累计签到次数')
    end_time = DateTimeField(verbose_name='上次签到日期', null=True)

    class Meta:
        table_name = 'duel_history'
        database = SqliteDatabase(DATABASE_PATH)

    def can_be_handle(self):
        """
        决斗是否可以被接受
        """
        return self.state == 0

    def in_duel(self):
        """
        是否在决斗过程中
        """
        return self.state == 1

    @property
    def current_bullet(self) -> bool:
        """
        获取当前弹闸中子弹，True为有子弹，False为空枪
        """
        order = self.order
        bullet_str = str(self.bullet).split(',')
        return bullet_str[order] == '1'

    @property
    def visual_bullet(self) -> str:
        return str(self.bullet).replace('0', '_ ').replace('1', '| ').replace(',', '')

    def clearing(self):
        """
        结算，根据当前状态返回最后(胜者, 败者)id
        """
        temp_order = self.order
        temp_shot_id = self.in_turn
        bullet_str = str(self.bullet).split(',')[temp_order:]
        for bullet in bullet_str:
            if bullet == '1':
                loser = temp_shot_id
                winner = self.player2_id if loser == self.player1_id else self.player1_id
                return winner, loser
            temp_shot_id = self.player1_id if temp_shot_id == self.player1_id else self.player2_id
        return None, None

    def can_be_shot(self):
        return self.order < 7

    def expired(self) -> bool:
        current_time = datetime.datetime.now().timestamp()
        if self.state == 0:
            return (current_time - self.start_time.timestamp()) > _TIMEOUT
        elif self.state == 1:
            return (current_time - self.last_shot_time.timestamp()) > _TIMEOUT
        else:
            return True

    @property
    def another(self):
        """
        返回当前开枪的另一位玩家id，如当前轮到player1开枪，则返回player2的id
        """
        return self.player1_id if self.in_turn == self.player2_id else self.player2_id

    def switch(self):
        self.in_turn = self.player1_id if self.in_turn == self.player2_id else self.player2_id

    def _state_to_string(self):
        if self.state == 0:
            return '决斗邀请'
        elif self.state == 1:
            return '决斗开始'
        elif self.state == 2:
            return '决斗结束'
        elif self.state == -1:
            return '决斗被拒绝'
        else:
            return '非法状态'

    def __str__(self):
        return f'groupId: {self.group_id}\n' \
               f'player1Id: {self.player1_id}\n' \
               f'player2Id: {self.player2_id}\n' \
               f'赌注: {self.wager}\n' \
               f'决斗状态: {self._state_to_string()}\n' \
               f'当前开枪用户: {self.in_turn}\n' \
               f'子弹可视图: {self.visual_bullet}\n' \
               f'第几颗子弹: {self.order}\n' \
               f'中枪概率: {self.probability}\n' \
               f'上次开枪时间: {self.last_shot_time}\n' \
               f'开始时间: {self.start_time}\n' \
               f'结束时间: {self.end_time}\n'