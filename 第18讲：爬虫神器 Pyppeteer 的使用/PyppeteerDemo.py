# coding=utf-8
"""
@Time : 2020/6/6 16:20
@Author: zhangqian
"""


from pyppeteer import launch
from pyquery import PyQuery as pq
import asyncio


async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto("https://dynamic2.scrape.cuiqingcai.com/")
    await page.waitForSelector('.item .name')
    doc = pq(await page.content())
    names = [item.text() for item in doc('.item .name').items()]
    print('names: ', names)
    await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
