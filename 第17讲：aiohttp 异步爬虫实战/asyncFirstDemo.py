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
#     ����session����url ��ȡhtml code
#     :param session:
#     :param url:�����url
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
#     with as ǰ����� async ��������һ��֧���첽�������Ĺ�����
#     ���ص��� coroutine ������ôǰ���Ҫ�� await
#     :return:
#     """
#     async with aiohttp.ClientSession() as session:
#         params = {'name': 'James', 'age': 27}
#         async with session.get("https://httpbin.org/get", params=params) as response:
#             print('text', await response.text())
#             print('status:', response.status)
#             print('headers:', response.headers)

CONCURRENCY = 5
semaphore = asyncio.Semaphore(CONCURRENCY)  # ��Ӳ����������ź�
URL = 'https://www.baidu.com/'
session = None


async def scrape_api():
    async with semaphore:
        async with session.get(URL) as response:
            print('��������:', URL)
            await asyncio.sleep(1)
            return await response.text()


async def main():
    global session
    session = aiohttp.ClientSession()
    tasks = [asyncio.ensure_future(scrape_api()) for _ in range(100)]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())  # ��������
    # asyncio.run(main())  # ������3.7������



