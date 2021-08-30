from nonebot import on_command
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import GROUP, GroupMessageEvent, Message, MessageSegment
from nonebot.typing import T_State

from modules.user_info import UserInfo
from utils.log import logger
from .accident import random_accident
from .data_source import *
from .sentence import *

from nonebot.plugin import export

from ..sign_in.config import LUCKY_MAX

export = export()
export.plugin_name = '俄罗斯轮盘'
export.plugin_usage = '''俄罗斯轮盘帮助：
    开启游戏：装弹[金额][at](指定决斗对象，为空则所有群友都可接受决斗)
        示例：装弹10
    接受对决：接受对决/拒绝决斗
    开始对决：开枪（轮流开枪，60秒未开枪另一方可通过该命令进行结算）
'''

russian_roulette = on_command('俄罗斯轮盘', aliases={'装弹', '俄罗斯转盘'}, permission=GROUP, priority=5, block=True)
_accept = on_command('接受', aliases={'接受决斗', '接受挑战'}, permission=GROUP, priority=5, block=True)
_refuse = on_command('拒绝', aliases={'拒绝决斗', '拒绝挑战'}, permission=GROUP, priority=5, block=True)
_shot = on_command('开枪', aliases={'咔', '嘭', '嘣'}, permission=GROUP, priority=5, block=True)


@russian_roulette.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id
    player1_id = event.sender.user_id
    # 获取最近一场决斗
    latest_duel = get_latest_duel(group_id)
    if latest_duel is not None and latest_duel.can_be_handle():
        # 超时后终止上一个决斗
        if latest_duel.expired():
            logger.debug(f'终止超时的决斗: {latest_duel}')
            duel_end(latest_duel)
            del latest_duel
        # 若决斗未超时，则发送通知并跳过后续步骤
        elif latest_duel.player1_id == player1_id:
            await russian_roulette.finish('请先完成当前决斗')
            return
        else:
            await russian_roulette.finish('请勿打扰别人神圣的决斗，丨')
            return

    message = event.message
    if len(message) < 1:
        await russian_roulette.finish(f'请按照格式: {export.plugin_usage}')
        return
    # 命令后第一个参数必须为数字，作为赌注
    gold = 0
    gold_message = message[0]
    if gold_message.is_text:
        message_text = str(gold_message).strip()
        try:
            gold = int(message_text)
        except Exception:
            pass

    if gold == 0:
        await russian_roulette.finish('请输入赌注，子弹也是要钱的')
        return
    elif gold < 0:
        await russian_roulette.finish('咋地，决斗完还想倒吸钱啊?')
        return

    # 获取第一个被@的人作为被挑战者
    player2_id = -1
    for item in message:
        if item.type == 'at':
            player2_id = int(item.data.get('qq', -1))
            break

    # 不能和自己决斗
    if player2_id == player1_id:
        await russian_roulette.finish('珍爱生命，不要自残', at_sender=True)
        return

    # 检测决斗发起人是否有足够的金币
    player1_gold = await UserInfo.get_gold(player1_id, group_id)
    logger.debug(f'开始一场新的决斗:\n'
                 f'挑战者: {player1_id}\n'
                 f'挑战者拥有金币: {player1_gold}\n'
                 f'赌注: {gold}')
    if player1_gold < gold:
        await russian_roulette.finish('请出门左转打工挣够钱再来')
        return
    # 若指定了被决斗者，则检测其金币是否足够
    if player2_id != -1:
        player2_gold = await UserInfo.get_gold(player2_id, group_id)
        if player2_gold < gold:
            logger.debug(f'被挑战者{player2_id}所拥有金币不足以支付决斗')
            await russian_roulette.finish('你的对手太穷了，他不配和你对战')
            return
        logger.debug(f'被挑战者: {player2_id}\n'
                     f'被挑战者拥有金币: {player2_gold}')
    else:
        logger.debug('未指定被挑战者')

    # 若无指定被决斗者，则所有群员都可响应这场决斗
    if player2_id == -1:
        # 插入新的决斗记录
        insert_duel(group_id, player1_id, player2_id, gold)
        await russian_roulette.finish(random_sentence(group_challenge))
    else:
        # 插入新的决斗记录
        insert_duel(group_id, player1_id, player2_id, gold)
        # 向被决斗者发送at消息
        message = Message(f'{MessageSegment.at(player2_id)}{random_sentence(challenge)}')
        await russian_roulette.finish(message)


@_accept.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id
    # 获取最近一场决斗
    latest_duel = get_latest_can_handle_duel(group_id)
    # 决斗可能因超时被取消(或根本无发生过任何决斗)
    if latest_duel is None:
        logger.debug(f'当前无可被接受挑战的决斗: {latest_duel}')
        await _accept.finish('当前无任何决斗，你接受个什么劲儿')
        return
    # 若决斗超时则跳过后续步骤(更新其状态)
    if latest_duel.expired():
        logger.debug(f'决斗已超时，不能被接受了: {latest_duel}')
        duel_end(latest_duel)
        await _accept.finish('决斗已经超时，请重新发起')
        return
    accept_id = event.user_id
    player1_id = latest_duel.player1_id
    if player1_id == accept_id:
        await _accept.finish('珍爱生命，不要自残', at_sender=True)
        return
    player2_id = latest_duel.player2_id
    logger.debug('[接受]当前决斗: {latest_duel}')
    # 用户是否有资格接受决斗(当前决斗未指定任何人，或接受用户是被决斗者)
    if player2_id == -1 or player2_id == accept_id:
        player2_id = accept_id
        latest_duel.player2_id = player2_id
        player2_gold = await UserInfo.get_gold(player2_id, group_id)
        if player2_gold < latest_duel.wager:
            logger.debug(f'接受决斗者无足够金币: {player2_gold}')
            await _accept.finish('你的金币不足以支付决斗费用，请去打工再来')
            return
        # 进入下一阶段
        duel_accept(latest_duel)
        logger.debug(f'当前决斗被接受，进入下一阶段: {latest_duel}')
        random_s = random_sentence(accept)
        message = Message(f'{MessageSegment.at(player2_id)}{random_s}{MessageSegment.at(player1_id)}。'
                          f'{MessageSegment.at(player1_id)}请通过[开枪]来把握自己的命运')
        await _accept.finish(message)
    else:
        await _accept.finish('和你无关，一边玩泥巴去!')


@_refuse.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id
    # 获取最近一场决斗
    latest_duel = get_latest_can_handle_duel(group_id)
    # 决斗可能因超时被取消(或根本无发生过任何决斗)
    if latest_duel is None:
        logger.debug(f'当前无可被拒绝挑战的决斗: {latest_duel}')
        await _refuse.finish('当前无任何决斗，你怂个啥哦')
        return
    # 若决斗超时则跳过后续步骤(更新其状态)
    if latest_duel.expired():
        logger.debug(f'决斗已超时，不能被拒绝了: {latest_duel}')
        duel_end(latest_duel)
        await _refuse.finish('决斗已经超时了，挺起腰板吧')
        return
    refuse_id = event.user_id
    player1_id = latest_duel.player1_id
    if player1_id == refuse_id:
        await _accept.finish('你不能拒绝自己的决斗', at_sender=True)
        return
    player2_id = latest_duel.player2_id
    logger.debug(f'[拒绝]当前决斗: {latest_duel}')
    if player2_id == -1:
        await _refuse.finish('这场决斗面向所有人，不用站出来认怂')
        return
    if player2_id == refuse_id:
        logger.debug(f'用户{player2_id}拒绝了决斗，更新其状态')
        # 更新决斗状态
        duel_denied(latest_duel)
        message = Message(f'卑微的{MessageSegment.at(player2_id)}拒绝了应用的{MessageSegment.at(player1_id)}')
        await _refuse.finish(message)
    else:
        await _refuse.finish('吃瓜群众一边去')


@_shot.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    group_id = event.group_id
    latest_duel = get_latest_can_shot_duel(group_id)
    # 当前没有决斗或不在决斗状态，直接向用户发出通知消息
    if latest_duel is None:
        logger.debug(f'[开枪]当前无进行中的决斗: {latest_duel}')
        await _shot.finish('射射射，你射个啥呢，现在没有任何决斗!')
        return
    # 子弹已经打完了但没人死亡，结算
    if not latest_duel.can_be_shot():
        duel_end(latest_duel)
        await _shot.finish('竟然忘记装子弹了，这一次无人获胜!')
        return

    shot_player_id = event.user_id
    another_player_id = latest_duel.another
    logger.debug(f'[开枪{shot_player_id}]当前决斗: {latest_duel}')
    # 决斗超时进入结算(由另一方发送开枪才允许触发结算)
    if shot_player_id == another_player_id and latest_duel.expired():
        duel_end(latest_duel)
        # 进入结算状态
        winner, loser = latest_duel.clearing()
        if winner is None or loser is None:
            # 无人获胜
            message = MessageSegment.text('竟然忘记装子弹了，这一次无人获胜!')
        else:
            message = await _end_of_game(event, latest_duel, winner, loser)
        logger.debug(f'决斗超时，由另一方发起结算: {another_player_id}')
        await _shot.finish(message)
        return

    # 检测命令发送者id是否和当前记录的开枪人一致
    if shot_player_id != latest_duel.in_turn:
        await _shot.finish('枪不在你手上，别捣乱')
        return
    # 根据开枪用户当天运气，触发额外事件
    user_fortune = await UserInfo.get_lucky(shot_player_id, group_id)
    if user_fortune is None:
        user_fortune = 0
    # 总概率为用户最大运气值的7%(这里强关联了用户的最大运气值)
    real_fortune = (LUCKY_MAX - user_fortune) * 7
    r = random.uniform(0, 1) * real_fortune
    t = random.randint(0, LUCKY_MAX * 100)
    if t < r:
        # 触发意外事件，当前子弹直接换人
        message, shot, end, winner, loser = random_accident(shot_player_id, another_player_id)
        logger.debug(f'用户触发意外事件:\n'
                     f'终结消息: {message}\n,'
                     f'子弹是否射出: {shot}\n,'
                     f'是否结束事件: {end}\n'
                     f'胜者: {winner}\n'
                     f'败者: {loser}')
        # 是否需要结束决斗
        if end:
            end_message = await _end_of_game(event, latest_duel, winner, loser)
            duel_end(latest_duel)
            await _shot.send(message)
            await _shot.finish(end_message)
            return
        # 当前子弹是否已发射
        if shot:
            duel_shot(latest_duel)
        else:
            duel_switch(latest_duel)
        await _shot.finish(message)
        return
    get_shot = duel_shot(latest_duel)
    if get_shot:
        logger.debug(f'用户{shot_player_id}中弹，进入结算')
        duel_end(latest_duel)
        # 中枪后进入结算
        await _shot.send(random_sentence(died))
        message = await _end_of_game(event, latest_duel, another_player_id, shot_player_id)
        await _shot.finish(message)
    else:
        message = Message(f'{random_sentence(miss)}。枪交到了{MessageSegment.at(another_player_id)}手上')
        await _shot.finish(message)


async def _end_of_game(event: GroupMessageEvent, duel: DuelHistory, winner: int, loser: int) -> Message:
    group_id = event.group_id
    wager = duel.wager
    await UserInfo.change_gold(winner, group_id, wager)
    await UserInfo.change_gold(loser, group_id, -wager)
    return Message(
        f'胜者{MessageSegment.at(winner)}赢得了{wager}枚金币\n'
        f'败者{MessageSegment.at(loser)}被丢进了海里喂鱼\n'
        f'子弹: {duel.visual_bullet}')
