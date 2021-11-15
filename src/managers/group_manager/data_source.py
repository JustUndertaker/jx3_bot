import os
from typing import Optional

import httpx
from nonebot.adapters.cqhttp import Bot, Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment
from nonebot.rule import Rule
from nonebot.typing import T_State
from src.modules.bot_info import BotInfo
from src.modules.group_info import GroupInfo
from src.modules.plugin_info import PluginInfo
from src.modules.user_info import UserInfo
from src.utils.config import config
from src.utils.user_agent import get_user_agent


async def group_init(bot_id: int, group_id: int, group_name: str) -> None:
    '''
    注册群信息
    '''
    await GroupInfo.append_or_update(bot_id, group_id, group_name)


async def get_group_name(bot_id: int, group_id: int) -> str:
    '''获取群名'''
    return await GroupInfo.get_group_name(bot_id, group_id)


async def group_detel(bot_id: int, group_id: int) -> None:
    '''删除群数据'''
    await GroupInfo.delete_one(bot_id, group_id)
    await UserInfo.delete_group(bot_id, group_id)
    await PluginInfo.deltele_group(bot_id, group_id)


async def user_init(bot_id: int, user_id: int, group_id: int, user_name: str) -> None:
    '''
        :说明
            注册一条用户信息

        :参数
            * bot_id：机器人QQ
            * user_id：用户QQ
            * group_id：QQ群号
            * user_name：用户昵称
    '''
    await UserInfo.append_or_update(bot_id, user_id, group_id, user_name)


async def user_detele(bot_id: int, user_id: int, group_id: int) -> None:
    '''
    删除成员信息
    '''
    await UserInfo.delete_one(bot_id, user_id, group_id)


async def get_user_name(bot_id: int, user_id: int, group_id: int) -> str:
    '''
    获取用户名称
    '''
    name = await UserInfo.get_user_name(bot_id, user_id, group_id)
    return name


async def change_server(bot_id: int, group_id: int, server: str) -> None:
    '''
    :说明
        更换绑定服务器

    :参数
        * group_id：QQ群号
        * server：服务器
    '''
    await GroupInfo.set_server(bot_id, group_id, server)


async def get_server_name(name: str) -> Optional[str]:
    '''
    根据服务器获取主服务器名
    '''
    url_head: str = config.get('jx3-api').get('jx3-url')
    url = f"{url_head}/app/server"
    params = {"name": name}
    async with httpx.AsyncClient(headers=get_user_agent()) as client:
        try:
            req_url = await client.get(url=url, params=params)
            req = req_url.json()
            code = req.get('code')
            if code == 200:
                data = req['data']
                return data['server']
            else:
                return None
        except Exception:
            return None


async def change_active(bot_id: int, group_id: int, active: int) -> None:
    '''
    设置活跃值
    '''
    await GroupInfo.set_active(bot_id, group_id, active)


def check_event(event_list: str):
    '''
    检查事件
    '''

    async def _check_event(bot: "Bot", event: "Event", state: T_State) -> bool:
        return event.get_event_name() in event_list

    return Rule(_check_event)


async def check_robot_status(bot_id: int, group_id: int) -> Optional[bool]:
    '''
    :说明
        检查机器人状态

    :参数
        * bot_id：机器人QQ
        * group_id：QQ群号

    :返回
        * bool：开关状态
        * None：未注册群
    '''
    return await GroupInfo.get_robot_status(bot_id, group_id)


async def set_robot_status(bot_id: int, group_id: int, status: bool) -> bool:
    '''设置机器人开关'''
    return await GroupInfo.set_robot_status(bot_id, group_id, status)


async def get_bot_owner(bot_id: int) -> Optional[int]:
    '''获取机器人管理员账号'''
    owner = await BotInfo.get_owner(bot_id)
    return owner


async def sign_reset(bot_id: int) -> list[int]:
    '''
    :说明
        重置签到人数，返回所有开启机器人的群号list
    '''
    await GroupInfo.reset_sign(bot_id)
    group_list = await GroupInfo.get_group_list(bot_id)
    return group_list


async def get_welcome_status(bot_id: int, group_id: int) -> Optional[bool]:
    '''获取进群通知开关'''
    return await GroupInfo.get_welcome_status(bot_id, group_id)


async def set_welcome_status(bot_id: int, group_id: int, status: bool):
    '''设置进群通知'''
    await GroupInfo.set_welcome_status(bot_id, group_id, status)


async def get_someoneleft_status(bot_id: int, group_id: int) -> Optional[bool]:
    '''获取离群通知开关'''
    return await GroupInfo.get_someoneleft_status(bot_id, group_id)


async def set_someoneleft_status(bot_id: int, group_id: int, status: bool):
    '''设置离群通知'''
    await GroupInfo.set_someoneleft_status(bot_id, group_id, status)


async def get_goodnight_status(bot_id: int, group_id: int) -> Optional[bool]:
    '''获取晚安通知开关'''
    return await GroupInfo.get_goodnight_status(bot_id, group_id)


async def set_goodnight_status(bot_id: int, group_id: int, status: bool):
    '''设置晚安通知'''
    await GroupInfo.set_goodnight_status(bot_id, group_id, status)


def Message_command_handler(message: Message, command: str) -> Message:
    '''
    剔除message命令内容
    '''
    length = len(command)
    text = message[0].data['text']
    if len(text) == length+1:
        message = message[1:]
    else:
        new_text = text[length+1:]
        message[0].data['text'] = new_text
    return message


async def _Message_encoder(bot_id: int, group_id: int, msg_type: str, message: Message) -> list:
    '''
    :说明
        message消息编码器，将message消息序列化，保存本地

    :参数
        * bot_id：机器人id
        * group_id：QQ群号
        * msg_type：消息类型，welcome，someoneleft，goodninght
        * message：消息内容
    '''
    # 处理目录
    _path = config.get('path').get(msg_type)
    path = f"{_path}{str(bot_id)}/{str(group_id)}/"

    if os.path.exists(path):
        file_list = os.listdir(path)
        for one_file in file_list:
            filepath = os.path.join(path, one_file)
            os.remove(filepath)
    else:
        os.makedirs(path)

    count = 1
    req_message = []
    for one_message in message:
        one_req_message = {}
        if one_message.type == 'image':
            # 图片处理
            url = one_message.data['url']
            file_name = f"{path}{count}.jpg"
            async with httpx.AsyncClient(headers=get_user_agent()) as client:
                req = await client.get(url=url)
                with open(file_name, mode='wb') as f:
                    f.write(req.read())
            count += 1
            one_req_message['type'] = "image"
            one_req_message['data'] = file_name
            req_message.append(one_req_message)
            continue

        if one_message.type == 'text':
            # 文字处理
            one_req_message = {}
            one_req_message['type'] = one_message.type
            one_req_message['data'] = one_message.data.get('text')
            req_message.append(one_req_message)
            continue

        if one_message.type == 'face':
            one_req_message = {}
            one_req_message['type'] = one_message.type
            one_req_message['data'] = one_message.data.get('id')
            req_message.append(one_req_message)
            continue

    return req_message


def _Message_decoder(message_list: list) -> Message:
    '''
    message消息解码器
    '''
    req_message = Message()
    for one_message in message_list:
        msg_type = one_message['type']
        if msg_type == 'text':
            text = one_message['data']
            msg = MessageSegment.text(text)

        if msg_type == 'face':
            face_id = one_message['data']
            msg = MessageSegment.face(face_id)

        if msg_type == 'image':
            url = one_message['data']
            with open(url, 'rb') as f:
                img_byte = f.read()
            msg = MessageSegment.image(img_byte)

        req_message.append(msg)
    return req_message


async def set_welcome_text(bot_id: int, group_id: int, msg_type: str, message: Message):
    '''
    :说明
        设置群欢迎语

    :参数
        * bot_id：机器人QQ
        * group_id：QQ群号
        * msg_type：消息类型，welcome，someoneleft，goodninght
        * message：消息内容
    '''
    message_list = await _Message_encoder(bot_id=bot_id, group_id=group_id, msg_type=msg_type, message=message)
    await GroupInfo.set_welcome_text(bot_id, group_id, message_list)


async def get_welcome_text(bot_id: int, group_id: int) -> Message:
    '''
    :说明
        获取群欢迎语

    :参数
        * bot_id：机器人QQ
        * group_id：QQ群号
    '''
    message_list = await GroupInfo.get_welcome_text(bot_id, group_id)
    message = _Message_decoder(message_list)
    return message


async def get_someoneleft_text(bot_id: int, group_id: int) -> Message:
    '''
    : 说明
        获取群离开语

    : 参数
        * bot_id：机器人QQ
        * group_id：QQ群号
    '''
    message_list = await GroupInfo.get_someoneleft_text(bot_id, group_id)
    message = _Message_decoder(message_list)
    return message


async def get_goodnight_text(bot_id: int, group_id: int) -> Message:
    '''
    : 说明
        获取晚安语

    : 参数
        * bot_id：机器人QQ
        * group_id：QQ群号
    '''
    message_list = await GroupInfo.get_goodnight_text(bot_id, group_id)
    message = _Message_decoder(message_list)
    return message


def handle_didi_message(one_message: MessageSegment) -> MessageSegment:
    '''处理滴滴消息头部'''
    text: str = one_message.data['text']
    req_text = text[3:]
    req_msg = MessageSegment.text(req_text)
    return req_msg
