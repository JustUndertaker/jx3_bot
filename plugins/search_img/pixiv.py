import httpx
from bs4 import BeautifulSoup
from nonebot.adapters.cqhttp import MessageSegment

_base_url = 'https://ascii2d.net/'
_pixiv_api = f'{_base_url}search/url/'


class PixivImg:
    def __init__(self, thumbnail, title, author, url, author_url):
        self.thumbnail = thumbnail
        self.title = title
        self.author = author
        self.url = url
        self.author_url = author_url


def pixiv_search(url):
    color_r = httpx.get(f'{_pixiv_api}{url}')
    # 色合検索url
    color_url = str(color_r.request.url)
    # 替换其中关键字得到特徴検索url(关键字必须带/，避免替换掉路径中的color)
    bovw_url = color_url.replace('/color/', '/bovw/')
    bovw_r = httpx.get(bovw_url)
    color_detail = _detail(color_r.text)
    bovw_detail = _detail(bovw_r.text)
    result = []
    # 遍历结果生成信息列表(只取前3个识别结果)
    for item in color_detail[:3] + bovw_detail[:3]:
        img = MessageSegment.image(item.thumbnail)
        text = f'标题: {item.title}\n作者: {item.author}\n地址: {item.url}\n作者地址: {item.author_url}'
        result.append(text + img)
    return result


# 解析ascii2d接口返回网页结果
def _detail(html_text) -> list:
    result = []
    bs = BeautifulSoup(html_text, 'html.parser')
    item_boxes = bs('div', attrs={'class': 'item-box'})
    for item_box in item_boxes:
        detail_box = item_box.find('div', attrs={'class': 'detail-box'})
        if detail_box is None:
            continue
        detail = detail_box('a')
        if len(detail) != 2:
            continue
        img = item_box.find('div', attrs={'class': 'image-box'}).img
        thumbnail = f'{_base_url}{img["src"]}' if img is not None else ''
        title = detail[0]
        author = detail[1]
        obj = PixivImg(thumbnail, title.string, author.string, title['href'], author['href'])
        result.append(obj)
    return result
