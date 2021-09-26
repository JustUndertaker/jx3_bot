from typing import Optional, Union

import yaml

config: Optional[dict[str, dict[str, Union[str, int, bool]]]] = None
'''全局配置字典'''


def config_init():
    '''
    初始化读取配置文件，需要在所有项目之前启动
    '''
    global config
    with open('config.yml', 'r', encoding='utf-8') as f:
        cfg = f.read()
        config = yaml.load(cfg, Loader=yaml.FullLoader)
