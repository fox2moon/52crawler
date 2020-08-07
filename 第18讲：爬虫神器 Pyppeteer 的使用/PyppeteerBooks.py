# coding=utf-8
"""
@Time : 2020/6/9 17:49
@Author: zhangqian
"""

import asyncio
import json
from os import makedirs
from os.path import exists

from pyppeteer import launch
import logging
from pyppeteer.errors import TimeoutError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
# INDEX_URL = 'https://dynamic5.scrape.cuiqingcai.com/api/book/?limit=18&offset={offset}'
INDEX_URL = 'https://dynamic2.scrape.cuiqingcai.com/page/{page}'
DETAIL_URL = 'https://dynamic5.scrape.cuiqingcai.com/api/book/{id}'
MAX_PAGE = 3
PAGE_SIZE = 18
WINDOW_WIDTH, WINDOW_HEIGHT = 1366, 768
HEADLESS = False
browser, tab = None, None
TIMEOUT = 15
HEADLESS = True
RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)


async def init():
    '''
    根据selector判断该页面元素是否可操作
    :return:
    '''
    global browser, tab
    browser = await launch(headless=HEADLESS,
                           args=['--disable-infobars',
                                 f'--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}'])
    tab = await browser.newPage()
    await tab.setViewport({'width': WINDOW_WIDTH, 'height': WINDOW_HEIGHT})


async def scrape_page(url, selector):
    '''
    根据selector判断该页面元素是否可操作
    :param url:
    :param selector:
    :return:
    '''
    logging.info('scrape page %s', url)
    try:
        await tab.goto(url)
        await tab.waitForSelector(selector, options={'timeout': TIMEOUT * 1000})  # 会出现timeout 15000ms exceeds
        # await asyncio.wait([tab.waitForNavigation(), tab.querySelector(selector)])
    except TimeoutError:
        logging.error('error occurred while scraping %s', url, exc_info=True)


async def scrape_index(page):
    '''
    根据页码生成的列表url、元素选择器判断是否可操作
    :param page:
    :return:
    '''
    url = INDEX_URL.format(page=page)
    await scrape_page(url, '.item .name')


async def parse_index():
    '''
    解析列表页，返回详情页链接
    :return:
    '''
    return await tab.querySelectorAllEval('.item .name', 'nodes => nodes.map(node => node.href)')


async def scrape_detail(url):
    '''
    判断详情页是否可操作
    :param url:
    :return:
    '''
    await scrape_page(url, 'h2')


async def parse_detail():
    '''
    解析详情页，返回json
    :return:
    '''
    url = tab.url
    name = await tab.querySelectorEval('.m-b-sm', 'node => node.innerText')
    categories = await tab.querySelectorAllEval('.categories button span', 'nodes => nodes.map(node => node.innerText)')
    score = await tab.querySelectorEval('.score', 'node => node.innerText')
    cover = await tab.querySelectorEval('.cover', 'node => node.src')
    drama = await tab.querySelectorEval('.drama p', 'node => node.innerText')
    return {
        'url': url,
        'name': name,
        'score': score,
        'categories': categories,
        'cover': cover,
        'drama': drama
    }


async def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


async def main():
    await init()
    try:
        for page in range(1, MAX_PAGE+1):
            await scrape_index(page)
            detail_urls = await parse_index()
            logging.info('detailUrls %s', detail_urls)
            for detail_url in detail_urls:
                await scrape_detail(detail_url)
                res = await parse_detail()
                logging.info('data : %s', res)
                await save_data(res)
                logging.info('save data.')
    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())