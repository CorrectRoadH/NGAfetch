import sys
import asyncio
import httpx

sys.path.append('../')
import utils.User
from config import random_sleep_very_short


async def get(url):  # 把get独立出来的问题就是访问出错之后不能跳过,等下次更新了,而是必须访问完..那怎么整.用while?
    user = utils.User.User()  # todo 每次get都要初始化一次 user 太慢了
    r = None
    while True:
        random_sleep_very_short()
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(url, cookies=user.cookies, headers=user.header)
                break
        except httpx.ConnectTimeout:
            print(f"{url} 访问超时,重新访问")
            continue  # 本来是出错是用异步的方法重新访问,但是这里没有办法了直接访问
        except httpx.ProxyError:
            print(f"{url} 访问 代理错误,重新访问")
            continue
        except httpx.ReadTimeout:
            print(f"{url} 读取超时,重新访问")
            continue  # 本来是出错是用异步的方法重新访问,但是这里没有办法了直接访问
    return r
