# coding=gbk
# coding=utf-8
"""
@Time : 2020/6/5 14:22
@Author: zhangqian
"""

import aiohttp
import asyncio


# async def fetch(session, url):
#     """
#     根据session请求url 获取html code
#     :param session:
#     :param url:请求的url
#     :return:
#     """
#     async with session.get(url) as resp:
#         return await resp.text(), resp.status
#
#
# async def main():
#     async with aiohttp.ClientSession() as session:
#         html, status = await fetch(session, "https://www.baidu.com/")
#         print(f'html:{html[:100]}')
#         print(f'status:{status}')


# async def main():
#     """
#     with as 前面加上 async 代表声明一个支持异步的上下文管理器
#     返回的是 coroutine 对象，那么前面就要加 await
#     :return:
#     """
#     async with aiohttp.ClientSession() as session:
#         params = {'name': 'James', 'age': 27}
#         async with session.get("https://httpbin.org/get", params=params) as response:
#             print('text', await response.text())
#             print('status:', response.status)
#             print('headers:', response.headers)

CONCURRENCY = 5
semaphore = asyncio.Semaphore(CONCURRENCY)  # 添加并发数量的信号
URL = 'https://www.baidu.com/'
session = None


async def scrape_api():
    async with semaphore:
        async with session.get(URL) as response:
            print('正在请求:', URL)
            await asyncio.sleep(1)
            return await response.text()


async def main():
    global session
    session = aiohttp.ClientSession()
    tasks = [asyncio.ensure_future(scrape_api()) for _ in range(100)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())  # 适用所有
    # asyncio.run(main())  # 适用于3.7及以上



