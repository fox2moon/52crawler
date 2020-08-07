# coding=utf-8
"""
@Time : 2020/6/11 10:35
@Author: zhangqian
"""
import asyncio
from pyppeteer import launch


async def main():
    browser = await launch(headless=False)
    page = await browser.newPage()
    # await page.goto('https://dynamic2.scrape.cuiqingcai.com/')
    # await page.waitForSelector('.item .name')
    # await page.click('.name', options={
    #     'button': 'left',
    #     'clickCount': 1,  #  1 or 2
    #     'delay': 2000,  #  毫秒
    #     })
    # await page.click('.item .name', options={'delay': 2000})
    await page.goto('https://baidu.com/')
    await page.waitForSelector('#form')
    await page.type('#kw', 'puppeteer', {'delay': 100})  # 打开百度后，自动在搜索框里慢慢输入puppeteer ,
    await page.click('#su')
    await page.waitFor(1000)
    await browser.close()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())

