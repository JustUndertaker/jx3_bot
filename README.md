<div align="center">

# JX3_ROBOT

_✨基于[nonebot2](https://github.com/nonebot/nonebot2)的剑网三群聊机器人，采用[jx3api](https://jx3api.com)作为数据源。✨_

</div>

<p align="center">
<a href="https://www.python.org/">
<img src="https://img.shields.io/badge/python-3.9%2B-blue" alt="license"></a>
<a href="https://github.com/nonebot/nonebot2">
<img src="https://img.shields.io/badge/nonebot-2.0.0a15-yellow"></a>
<a href="https://github.com/Mrs4s/go-cqhttp">
<img src="https://img.shields.io/badge/go--cqhttp-v1.0.0--beta6-red"></a>
</p>

## 通知
项目是初学python写的，所以东西很乱很杂，维护起来异常困难，最终决定放弃这个项目的维护了。新开了个更加简单的坑：[mini_jx3_bot](https://github.com/JustUndertaker/mini_jx3_bot)，同样的味道，但是单用户，代码更好看了，欢迎使用。
### 有什么问题也可加QQ群：776825118

## 简介
基于nonebot2的剑网三的QQ群聊机器人，采用jx3api为数据接口，提供剑网三的一些查询，娱乐功能。

- 兼容windows，linux平台
- 使用websockets连接jx3api
- 使用sqlite数据库，轻量便携
- 全异步处理，支持多个群操作
- 适配nonebot2风格代码，自定义事件
- 支持多个bot链接，可以当作后台服务

## 声明
此项目使用所有游戏数据来自：[jx3api](https://www.jx3api.com)，本项目只是数据搬运工。
## 部署机器人
### 安装环境
**项目需要python环境，且需要[python3.9+](https://www.python.org/downloads/)。**
```
apt-get install python3.9
```

**QQ协议端采用[go-cqhttp](https://github.com/Mrs4s/go-cqhttp)。**

- go-cqhttp需要下载ffmpeg环境，否则无法发送语音消息，具体安装请参考[文档](https://docs.go-cqhttp.org/guide/quick_start.html#%E5%AE%89%E8%A3%85-ffmpeg)。

### 安装依赖
```
pip install -r requirements.txt
```
### 安装playwright
页面截图需要采用playwright，第一次启动需要安装，可以参考[文档](https://playwright.dev/python/docs/intro)。
```
playwright install
```
### 配置设置
#### config.yml
```
chat_nlp:
  # 腾讯云API的secretId
  secretId: ~
  # 腾讯云API的secretKey
  secretKey: ~

# 自动插话-语音合成配置
chat_voice:
  # 阿里云的语音接口
  appkey: ~
  access: ~
  secret: ~

# 和风天气
weather:
  # 和风天气api-key，申请地址：https://id.qweather.com/#/login，选择网页api
  api-key: ~


# 其他设置参考打开文件自行修改
```
**使用腾讯云API进行闲聊操作，如果没有将使用[青云客API](http://api.qingyunke.com/)返回聊天**

- 申请地址：[点击申请](https://console.cloud.tencent.com/cam/capi) NLP自然语言处理：[点击申请](https://console.cloud.tencent.com/nlp)

- 申请成功后，获取访问密钥流程请参考[这里](https://cloud.tencent.com/document/product/598/45511)

**阿里云API进行语音合成，如果没有将不会发送语音信息。**
- appkey和access申请地址：[点击申请](https://nls-portal.console.aliyun.com/overview)

- 获取secret地址：[点击这里](https://usercenter.console.aliyun.com/)
#### .env.pord
```
NICKNAME=["团子", "小团子"] # 这里设置机器人的昵称
access_token="your_token" # 这里设置你的服务器access_token，相应的gocq客户端同样需要设置
```

### 启动
```
python bot.py
```
### 日志
**日志保存路径在：/log/，分为3个等级：ERROR，INFO，DEBUG，日志默认保存10天，以日期命名。**

## 功能列表
### 通用功能
|**插件**|**命令** |**说明**|
| :----: | :----: | :----: |
|自动插话|-|机器人会自动插话，可以修改活跃度|
|推送消息|-|推送官方新闻，奇遇播报，开服情况|
|签到|签到|简单的签到系统|
|智能闲聊|@机器人+XXX|默认使用腾讯API，辅助青云客API|
|语音说|@机器人+说XXX|发送语音需要安装ffmepg|
|舔狗日记|舔狗/日记/舔狗日记|返回一条舔狗日记|
|查询功能|具体参考功能|提供查询消息接口，接口使用jx3api|
|天气查询|XX天气/天气XX|查询天气，数据使用和风天气|
|疫情查询|XX疫情/疫情 XX|查询疫情情况|

### 查询功能
|**功能**|**命令**|**说明**|
| :----: | :----: | :----: |
|骚话|骚话|返回一条剑网三骚话|
|日常查询|日常 [服务器]|查询服务器当天日常，服务器可省略|
|开服查询|开服 [服务器]|查询服务器开服情况，服务器可省略|
|更新公告|更新/公告/更新公告|查看最新更新公告|
|金价查询|金价 [服务器]|查询服务器金价，服务器可省略|
|前置查询|前置/条件 [奇遇名]|查询奇遇的前置条件和奖励|
|奇遇查询|奇遇 [服务器] [角色名]|查询角色奇遇记录，服务器可省略|
|奇遇列表查询|查询 [服务器] [奇遇名]|查询服务器的某个奇遇记录，服务器可省略|
|花价查询|花价 [服务器]|查询花价，服务器可省略|
|配装查询|配装 [职业]|查询职业配装，如“配装 冰心”或“冰心配装”|
|奇穴查询|奇穴 [职业]|查询职业奇穴，如“奇穴 冰心”或“冰心奇穴”|
|小药查询|小药 [职业]|查询职业小药，如“小药 冰心”或“冰心小药”|
|宏查询|宏 [职业]|查询职业的宏，如“宏 冰心”或“冰心宏”|
|物价查询|物价 [外观]|查询外观的物价|
|装饰查询|装饰 [装饰名]|查询装饰信息|
|考试查询|考试/科举 [题目]|查询题目答案，支持模糊搜索|
|攻略查询|攻略 [宠物]/[宠物]攻略|查询宠物攻略|
|沙盘查询|沙盘 [服务器]|查询沙盘信息，服务器可省略|
|资历排行|资历排行 [服务器] [门派]|查询资历排行，服务器可省略，可查询“全区服”，“全职业/全门派”|
|角色装备属性|装备/属性 [服务器] [角色]|查询角色的装备属性，服务器可省略|
|战绩查询|战绩 [服务器] [角色]|查询名剑大会战绩，服务器可省略|
|名剑排行|名剑排行 [22/33/55]|查询全服名剑排行，默认为22|
|副本记录|副本记录 [服务器] [角色]|查询主流副本记录，服务器可省略|

### 管理功能
**管理功能需要群管理，或者超级用户才能使用**
|**功能**|**命令**|**说明**|
| :----: | :----: | :----: |
|绑定服务器|绑定 [服务器名]|更换群绑定的服务器|
|插件开关|打开/关闭 [插件名]|开关某一个插件|
|活跃值|活跃值 [1-99]|设置机器人活跃值|
|更新信息|更新信息|手动更新群成员信息|

### 机器人管理员
**每个gocq客户端的机器人可以设置一个管理员，默认为空，好友私聊指令可以设置**
|**指令**|**说明**|
| :----: | :----: |
|设置管理员|设置当前私聊账号为机器人管理员，需要机器人无管理时|
|清除管理员|当前管理员发送，可清除当前管理|

**机器人管理员可以在群里设置机器人开关状态**
>命令：机器人 [开/关]

**机器人管理员私聊机器人可以管理机器人**
|**指令**|**说明**|
| :----: | :----: |
|帮助|获取管理帮助|
|状态/运行状态|查看机器人运行状态|
|打开/关闭 [QQ群号]|设置某个群的机器人状态|
|打开/关闭所有|全局设置机器人状态|
|好友列表|获取机器人好友列表|
|退群 [QQ群号]|机器人主动退群|
|删除好友 [QQ号]|删除指定好友|
|广播 [QQ群号] [消息]|给指定群发送一条广播消息|
|全体广播 [消息]|给所有打开机器人的群发送一条广播消息|

## TODO
- [x] 将源码迁移至src文件夹下
- [x] 将所有配置使用yaml重写
- [x] 支持多个bot链接
- [ ] 使用fastapi作为后台服务，提供dashborad接口
- [ ] 创建dashborad文件夹，使用web进行管理

## 感谢
* [onebot](https://github.com/howmanybots/onebot)：聊天机器人应用接口标准。
* [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)：cqhttp的golang实现。
* [nonebot2](https://github.com/nonebot/nonebot2)：跨平台Python异步机器人框架。
* [jx3_api](https://jx3api.com/)：剑三API提供的数据支持。
