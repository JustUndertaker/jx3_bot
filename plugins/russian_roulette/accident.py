import random

from nonebot.adapters.cqhttp import MessageSegment


def bullet_jammed(shot_player_id, another_player_id):
    return MessageSegment.text('你很幸运，子弹卡壳了'), False, False, None, None


def bullet_missed(shot_player_id, another_player_id):
    return MessageSegment.text('子弹擦过了你的脑壳，你活了下来'), True, False, None, None


_random_accident = [
    bullet_jammed,
    bullet_missed,
]


def random_accident(shot_player_id, another_player_id):
    """
    所有api必须以该方式返回(message: MessageSegment, shot: bool, end: bool)
    message: 事件发生后发送给用户的消息
    shot: 当前子弹是否射出，若False则当前子弹会直接换人
    end: 事件发生后决斗是否结束，True时会直接忽略shot
    winner: 决斗结束后的胜者(仅在end为True时有效)
    loser: 决斗结束后的败者(仅在end为True时有效)
    """
    api = _random_accident[random.randint(0, len(_random_accident) - 1)]
    return api(shot_player_id, another_player_id)
