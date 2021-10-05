from httpx import AsyncClient
from src.utils.config import config as baseconfig
from src.utils.log import logger

config = baseconfig.get('weather')
apikey = config.get('api-key')
url_weather_api = config.get('url-weather')
url_geoapi = config.get('url-geoapi')


# 获取城市ID
async def get_Location(city_kw: str, api_type: str = "lookup") -> dict:
    async with AsyncClient() as client:
        res = await client.get(
            url_geoapi + api_type, params={"location": city_kw, "key": apikey}
        )
        return res.json()


# 获取天气信息
async def get_WeatherInfo(api_type: str, city_id: str) -> dict:
    async with AsyncClient() as client:
        res = await client.get(
            url_weather_api + api_type, params={"location": city_id, "key": apikey}
        )
        return res.json()


async def get_City_Weather(city: str):
    # global city_id
    city_info = await get_Location(city)
    logger.debug(city_info)
    city_id = city_info["location"][0]["id"]
    city_name = city_info["location"][0]["name"]

    # 3天天气
    daily_info = await get_WeatherInfo("3d", city_id)
    daily = daily_info["daily"]
    day1 = daily[0]
    day2 = daily[1]
    day3 = daily[2]

    # 实时天气
    now_info = await get_WeatherInfo("now", city_id)
    now = now_info["now"]

    return {"city": city_name, "now": now, "day1": day1, "day2": day2, "day3": day3}
