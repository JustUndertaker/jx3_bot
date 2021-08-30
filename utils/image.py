from PIL import Image, ImageDraw, ImageFont


def img_square_to_circle(img: Image, radius: int, border: int = 0, border_color: tuple = (0, 0, 0)) -> Image:
    '''
    :说明
        将方形图片裁剪成圆形，可附加边框

    :参数
        * img：要裁剪的图片
        * radius：保存半径
        * border：边框像素大小
        * border_color：边框颜色

    :返回
        * Image类
    '''
    # 计算边长
    side_len = radius+border
    size = (side_len, side_len)

    # 创建bg
    bg = Image.new('RGBA', size, color=(0, 0, 0, 0))

    # 绘制边框背景
    border_bg = Image.new('RGBA', size, color=(0, 0, 0, 0))
    # 绘制边框
    border_img = ImageDraw.Draw(border_bg)
    border_img.ellipse((0, 0, side_len, side_len), fill=border_color)
    bg.paste(border_bg, (0, 0), border_bg)

    # 绘制图片
    mask = Image.new('RGBA', (radius, radius), color=(0, 0, 0, 0))
    # 画一个圆
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, radius, radius), fill=(159, 159, 160))
    loc = int(border/2)
    bg.paste(img, (loc, loc), mask)

    return bg


def draw_border_text(text: str, font: ImageFont, bp: int, color: tuple, bp_color: tuple = (0, 0, 0)) -> Image:
    '''
    :说明
        生成带描边的文字图片

    :参数
        * text：文字内容
        * font：字体对象
        * bp：描边长度
        * color：文字颜色
        * bp_color：描边颜色

    :返回
        * Image对象
    '''
    # 计算大小
    w, h = font.getsize(text)
    w += bp*2
    h += bp*2
    x = bp
    y = bp

    # 创建背景
    img = Image.new('RGBA', (w, h), color=(0, 0, 0, 0))
    # 创建画板
    img_draw = ImageDraw.Draw(img)

    # 绘制描边
    img_draw.text((x-bp, y), text, font=font, fill=bp_color)
    img_draw.text((x+bp, y), text, font=font, fill=bp_color)
    img_draw.text((x, y-bp), text, font=font, fill=bp_color)
    img_draw.text((x, y+bp), text, font=font, fill=bp_color)

    img_draw.text((x-bp, y-bp), text, font=font, fill=bp_color)
    img_draw.text((x+bp, y-bp), text, font=font, fill=bp_color)
    img_draw.text((x-bp, y+bp), text, font=font, fill=bp_color)
    img_draw.text((x+bp, y+bp), text, font=font, fill=bp_color)
    # 绘制文字
    img_draw.text((x, y), text, font=font, fill=color)

    return img
