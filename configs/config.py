'''
全局配置文件
'''

LOGGER_DEBUG: bool = True
'''插件日志的debug信息是否显示在控制台'''


DEFAULT_SERVER: str = "幽月轮"
'''默认绑定服务器'''


DEFAULT_STATUS: bool = True
'''群默认开启状态'''


ROBOT_ACTIVE: int = 20
'''机器人自动插话活跃度，1-100'''


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
