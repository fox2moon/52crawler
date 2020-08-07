# coding=utf-8
"""
@Time : 2020/6/9 11:22
@Author: zhangqian
"""

import asyncio
from pyppeteer import launch


async def main():
    await launch(headless=False)
    await asyncio.sleep(30)

asyncio.get_event_loop().run_until_complete(main())
