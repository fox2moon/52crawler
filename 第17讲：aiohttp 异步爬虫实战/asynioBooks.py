# coding=utf-8
"""
1.使用 aiohttp 完成全站的书籍数据爬取。
2.将数据通过异步的方式保存到 MongoDB 中
@Time : 2020/6/5 16:20
@Author: zhangqian
"""

import aiohttp
import asyncio
import logging
import json

from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
INDEX_URL = 'https://dynamic5.scrape.cuiqingcai.com/api/book/?limit=18&offset={offset}'
DETAIL_URL = 'https://dynamic5.scrape.cuiqingcai.com/api/book/{id}'
MAX_PAGE = 100
PAGE_SIZE = 18
CONCURRENCY = 10
semaphore = asyncio.Semaphore(CONCURRENCY)
session = None

MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'books'
MONGO_COLLECTION_NAME = 'books'
client = AsyncIOMotorClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]


async def scrape_api(url):
    """
    通用请求方法
    :param url:
    :return:
    """
    async with semaphore:
        logging.info('scraping url %s:', url)
        try:
            async with session.get(url) as response:
                return await response.json()
        except aiohttp.ClientError:
            logging.error('current url download error %s:', url, exc_info=True)


async def index_scrape(page):
    """
    请求列表数据
    :param page:列表页数
    :return:
    """
    offset = PAGE_SIZE * (page - 1)
    url = INDEX_URL.format(offset=offset)
    return await scrape_api(url)


async def save_data(data):
    """
    保存数据到mongo
    :param data:
    :return:
    """
    # logging.info('save data: %s', data[:100])
    if data:
        return await collection.update_one({
            'id': data.get('id')
        }, {
            '$set': data
        }, upsert=True)


async def detail_scrape(id):
    """
    请求详情页数据
    :param id:详情页id
    :return:
    """
    url = DETAIL_URL.format(id=id)
    data = await scrape_api(url)
    return await save_data(data)


async def main():
    global session
    session = aiohttp.ClientSession()
    index_tasks = [asyncio.ensure_future(index_scrape(page)) for page in range(1, 3)]
    results = await asyncio.gather(*index_tasks)
    json_dump = json.dumps(results, ensure_ascii=False, indent=2)
    logging.info('results %s', json_dump[:100])
    ids = []
    for index_data in results:
        if not index_data:
            continue
        for res in index_data['results']:
            ids.append(res['id'])
    detail_tasks = [asyncio.ensure_future(detail_scrape(id)) for _ in ids]
    await asyncio.gather(*detail_tasks)
    await session.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())