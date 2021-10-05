from PIL import Image, ImageDraw, ImageFont
from src.utils.config import config as baseconfig

config = baseconfig.get('weather')
font = config.get('font')
icon_dir = config.get('icon-dir')
background_img = config.get('background')


def size(size: int) -> ImageFont:
    return ImageFont.truetype(font, size)


def load_icon(id: str, size: float = 1.0) -> Image:
    im = Image.open(icon_dir + id + ".png")
    resize = (int(im.width * size), int(im.height * size))
    icon = im.thumbnail(resize, Image.ANTIALIAS)
    icon = im.convert("RGBA")
    return icon


def draw(data: dict) -> Image:
    # load backgroud picture
    im = Image.new("RGB", (1000, 1600), "white")
    d = ImageDraw.Draw(im)
    bg = Image.open(background_img)
    im.paste(bg, (0, 0), bg)

    # city
    city = ""
    for i in data["city"]:
        city += i + "\n"
    d.multiline_text(
        (94, 113), city, fill="white", font=size(144), align="center", spacing=30
    )

    # now
    icon = load_icon(data["now"]["icon"])
    im.paste(icon, (600, 100), icon)
    d.text(
        (721, 362),
        data["now"]["text"],
        fill="white",
        font=size(80),
        align="center",
        anchor="mt",
    )
    d.text(
        (721, 455),
        data["now"]["temp"] + "°C",
        fill="white",
        font=size(100),
        align="center",
        anchor="mt",
    )
    d.text((721, 600), "(实时)", fill="white", font=size(50), align="center", anchor="mt")

    # mid box
    icon = load_icon(data["day1"]["iconDay"], size=0.5)
    im.paste(icon, (320, 870), icon)
    icon = load_icon(data["day1"]["iconNight"], size=0.5)
    im.paste(icon, (420, 970), icon)

    item = ["uvIndex", "hum", "precip", "vis"]
    y = [893, 935, 977, 1018]
    for i in range(0, 4):
        icon = load_icon(item[i], 0.125)
        im.paste(icon, (567, y[i]), icon)

    text = "紫外线指数：\n相对湿度：\n降水量：\n能见度："
    d.multiline_text(
        (605, 890), text, fill="black", font=size(30), align="left", spacing=10
    )
    text = (
        f"{data['day1']['uvIndex']}"
        + f"\n{data['day1']['humidity']} %"
        + f"\n{data['day1']['precip']} mm"
        + f"\n{data['day1']['vis']} km"
    )
    d.multiline_text(
        (770, 890), text, fill="black", font=size(30), align="right", spacing=10
    )

    # button box
    icon = load_icon(data["day2"]["iconDay"], size=0.5)
    im.paste(icon, (105, 1253), icon)
    icon = load_icon(data["day2"]["iconNight"], size=0.5)
    im.paste(icon, (199, 1344), icon)

    d.text(
        (430, 1269),
        data["day2"]["tempMax"],
        fill="black",
        font=size(60),
        anchor="rt",
        align="left",
    )
    d.text((490, 1269), "°C", fill="black", font=size(60), anchor="mt")

    d.text(
        (430, 1424),
        data["day2"]["tempMin"],
        fill="black",
        font=size(60),
        anchor="rs",
        align="left",
    )
    d.text((490, 1424), "°C", fill="black", font=size(60), anchor="ms")

    y = [1265, 1307, 1349, 1390]
    for i in range(0, 4):
        icon = load_icon(item[i], 0.125)
        im.paste(icon, (567, y[i]), icon)

    text = "紫外线指数：\n相对湿度：\n降水量：\n能见度："
    d.multiline_text(
        (605, 1262), text, fill="black", font=size(30), align="left", spacing=10
    )
    text = (
        f"{data['day2']['uvIndex']}"
        + f"\n{data['day2']['humidity']} %"
        + f"\n{data['day2']['precip']} mm"
        + f"\n{data['day2']['vis']} km"
    )
    d.multiline_text(
        (770, 1262), text, fill="black", font=size(30), align="right", spacing=10
    )

    obsTime = data["now"]["obsTime"][5:10] + " " + data["now"]["obsTime"][11:16]
    d.text(
        (500, 1533), obsTime, fill="white", font=size(35), align="center", anchor="mt"
    )

    return im
