from playwright.async_api import async_playwright
from playwright.async_api import BrowserContext, Playwright
from utils.log import logger
import os
import json
import base64
from configs.pathConfig import HTML_PATH
from typing import Optional


_browser: Playwright

browser: Optional[BrowserContext] = None
'''全局browser'''


async def browser_init():
    '''初始化playwright'''
    global _browser
    global browser
    log = '初始化无头浏览器……'
    logger.info(log)
    user_data_dir = "./database/"
    _browser = await async_playwright().start()
    browser = await _browser.chromium.launch_persistent_context(user_data_dir=user_data_dir, headless=True)
    log = "无头浏览器初始化完毕！"
    logger.info(log)


async def get_html_screenshots(pagename: str, data: dict) -> str:
    '''
    :说明
        获取页面截图

    :参数
        * page：需要截图的页面名称，在/resources/html/目录下
        * data：需要传输的数据

    :返回
        * str：截图数据base64编码数据
    '''
    global browser
    if browser is None:
        await browser_init()

    page = await browser.new_page()
    url = "file://"+os.getcwd()+HTML_PATH+pagename

    # 打开页面
    await page.goto(url)

    # 注入js
    data_str = json.dumps(data, ensure_ascii=False)
    js = f"data={data_str}\nhandle(data)"
    await page.evaluate(js)

    # 截图
    await page.wait_for_load_state("networkidle")
    element_handle = await page.query_selector("#jiaose")
    screenshot_bytes = await element_handle.screenshot(type="jpeg", quality=100)
    base64_str = base64.b64encode(screenshot_bytes)
    req_str = 'base64://'+base64_str.decode()
    await page.close()
    return req_str