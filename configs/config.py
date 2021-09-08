'''
全局配置文件
'''

CHAT_NLP = {
    "secretId": "",  # 腾讯云API的secretId，开通地址：https://console.cloud.tencent.com/cam/capi
    "secretKey": ""  # 腾讯云API的secretKey，NLP申请：https://console.cloud.tencent.com/nlp
}
'''聊天配置-自动聊天'''


CHAT_VOICE = {
    "appkey": "",  # 阿里云的语音接口，开通地址：https://usercenter.console.aliyun.com/
    "access": "",  # 阿里云的语音接口，NLP申请：https://nls-portal.console.aliyun.com/overview
    "secret": "",  # 阿里云的语音接口
    "voice": "Aitong",  # 发言人，文档：https://help.aliyun.com/knowledge_detail/84435.html?spm=a2c4g.11186631.2.1.67045663WlpL4n
    "format": "mp3",  # 编码格式，支持 PCM WAV MP3
    "sample_rate": 16000,  # 采样率
    "volume": 50,  # 音量，取值范围：0～100
    "speech_rate": 0,  # 语速，取值范围：-500～500
    "pitch_rate": 0,  # 音调，取值范围：-500～500
}
'''聊天配置-语音合成'''

MAX_RECON_TIMES = 100
'''ws链接最大重连次数'''

DEFAULT_SERVER: str = "幽月轮"
'''每个群默认绑定服务器'''


DEFAULT_FIREND_ADD:bool=True
'''默认是否接收添加好友请求'''

DEFAULT_GROUP_ADD:bool= True
'''默认是否接收加群请求'''

DEFAULT_STATUS: bool = True
'''机器人在每个群默认开启状态'''


ROBOT_ACTIVE: int = 10
'''机器人自动插话活跃度，1-100'''

LOGGER_DEBUG: bool = True
'''插件日志的debug信息是否显示在控制台'''

DEFAULT_WELCOME: str = "欢迎新同学来到这里。"
'''默认群欢迎语'''

DEFAULT_LEFT: str = "默默地离开了我们……"
'''默认成员离开说辞'''

DEFAULT_LEFT_KICK: str = "被管理员狠狠地踢走了……"
'''默认成员被踢说辞'''

PRIVATE_CHAT:bool=True
'''是否开启智能私聊，开启后私聊会自动回复'''

IMG_CACHE: bool = True
'''截图是否缓存，缓存会下载图标到本地'''
