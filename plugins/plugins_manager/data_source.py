from typing import Union
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO
import base64
from nonebot.adapters.cqhttp import MessageSegment

from utils.log import logger
from configs.pathConfig import PATH_FONT, MEAU_IMG_OPEN, MEAU_IMG_CLOSE
from .base import PluginManager
from modules.plugin_info import PluginInfo
from modules.group_info import GroupInfo


async def check_group_init(group_id: int) -> bool:
    '''
    :说明
        检查群是否注册

    :参数
        * group_id：QQ群号

    :返回
        * bool：是否注册
    '''
    return await GroupInfo.check_group_init(group_id)


async def check_plugin_status(module_name: str, group_id: int) -> Union[bool, None]:
    '''
    :说明
        查看插件状态

    :参数
        * module_name：插件模块名
        * group_id：QQ群号

    :返回
        * bool:插件状态
    '''
    # 判断机器人开关
    status = await GroupInfo.get_robot_status(group_id)
    if status is None or status == False:
        return False
    # 返回插件开关
    return await PluginInfo.get_status(module_name, group_id)


async def plugin_init(group_id: int) -> None:
    '''
    :说明
        注册一个群的所有插件
    '''
    for plugin in PluginManager:
        module_name = plugin.module_name
        await PluginInfo.append_or_update(module_name, group_id)


async def change_plugin_status(plugin_name: str, group_id: int, status: bool) -> MessageSegment:
    '''
    :说明
        设置插件状态

    :参数
        * plugin_name：插件名
        * group_id：QQ群号
        * status：状态

    :返回
        * MessageSegment消息
    '''
    # 获取module_name
    module_name = None
    for plugin in PluginManager:
        if plugin.plugin_name == plugin_name:
            module_name = plugin.module_name
            break

    if module_name is not None:
        await PluginInfo.change_status(module_name, group_id, status)
        if status:
            msg = MessageSegment.text(f'插件[{plugin_name}]当前状态为：开启')
        else:
            msg = MessageSegment.text(f'插件[{plugin_name}]当前状态为：关闭')
    else:
        msg = MessageSegment.text(f'未找到插件[{plugin_name}]。')

    return msg


async def get_meau_card(group_id: int) -> MessageSegment:
    '''
    :说明
        获取菜单小卡片

    :参数
        * group_id：QQ群号

    :返回
        * MessageSegment
    '''
    plugin_list_db = await PluginInfo.get_all_status_from_group(group_id)

    # 构造字典列表
    plugin_list: list[dict] = []
    for plugin_db in plugin_list_db:
        data = {}
        for plugin_manager in PluginManager:
            if plugin_manager.module_name == plugin_db['module_name']:
                data['plugin_name'] = plugin_manager.plugin_name
                data['status'] = plugin_db['status']
                break
        if data is not None:
            plugin_list.append(data)

    try:
        img = await _draw_card(plugin_list)
        msg = MessageSegment.image(img)
        log = '菜单画图成功。'
        logger.debug(log)

    except Exception as e:
        msg = MessageSegment.text('画图失败惹……')
        log = f'菜单画图失败：{e}'
        logger.error(log)

    return msg


def _calculate_img_hight(plugin_list: list[dict], font: ImageFont, line_space: int) -> int:
    '''
    :说明
        根据字体计算图片的高度

    :参数
        * plugin_list：列表，字典字段为"name","status"
        * font：字体实例
        * line_space：行距

    :返回
        * int：高度
    '''
    hight = 0
    for plugin in plugin_list:
        _, one_hight = font.getsize(plugin['plugin_name'])
        hight += one_hight+line_space
    return hight


async def _draw_card(plugin_list: list[dict]) -> str:
    '''
    用于画卡片
    '''
    # 计算图片大小
    # 标题
    bg_width = 300
    bg_hight = 0
    font_tittle = ImageFont.truetype(PATH_FONT, size=30)
    tittle = '功能菜单'
    _, hight_tittle = font_tittle.getsize(tittle)
    line_space = 2  # 行距
    bg_hight += hight_tittle+line_space*3
    # 计算插件列表图片高度
    font_plugin = ImageFont.truetype(PATH_FONT, size=25)
    hight_plugin = _calculate_img_hight(plugin_list, font_plugin, line_space)
    bg_hight += hight_plugin+line_space*len(plugin_list)
    # 计算页脚
    footer = '输入：帮助 XXX 获取帮助'
    font_footer = ImageFont.truetype(PATH_FONT, size=20)
    _, hight_footer = font_footer.getsize(footer)
    bg_hight += hight_footer+50

    # 创建图片
    bg_size = (bg_width, bg_hight)
    bg_color = (255, 255, 255)
    img = Image.new('RGBA', bg_size, bg_color)
    drawBoard = ImageDraw.Draw(img)

    # 获取开关图像
    img_open = Image.open(MEAU_IMG_OPEN)
    img_close = Image.open(MEAU_IMG_CLOSE)

    point = 0  # 位置指针

    # ============================开始绘制====================================
    # 绘制标题
    w, h = font_tittle.getsize(tittle)
    loc = (int((bg_width-w)/2), point)
    color_tittle = (0, 0, 0)
    drawBoard.text(loc, tittle, color_tittle, font_tittle)
    point += h+line_space
    # 下划线
    xy = [(0, point), (bg_width, point)]
    color_line = (0, 0, 0)
    drawBoard.line(xy, fill=color_line, width=2, joint=None)
    point += line_space
    # 插件列表
    count = 1
    for plugin in plugin_list:
        text = f"{count}.{plugin['plugin_name']}"
        _, h = font_tittle.getsize(text)
        # 颜色
        if plugin['status']:
            color_plugin = (0, 0, 0)
            img_status = img_open
        else:
            color_plugin = (140, 140, 140)
            img_status = img_close
        loc = (0, point)
        drawBoard.text(loc, text, color_plugin, font_plugin)
        # 开关
        loc = (250, point+10)
        img.paste(img_status, box=loc, mask=img_status)
        count += 1
        point += h+line_space
    # 页脚

    color_footer = (52, 152, 219)
    w, _ = font_footer.getsize(footer)
    loc = (int((bg_width-w)/2), point)
    drawBoard.text(loc, footer, color_footer, font_footer)
    # 边框
    border = 50
    img = ImageOps.expand(img, border, bg_color)

    # 返回
    output_buffer = BytesIO()
    img.save(output_buffer, format='PNG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    req_str = 'base64://'+base64_str.decode()

    return req_str
