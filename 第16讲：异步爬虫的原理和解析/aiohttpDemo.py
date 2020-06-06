# coding=utf-8
"""
aiohttp 是一个支持异步请求的库，利用它和 asyncio 配合我们可以非常方便地实现异步请求操作

代码里面我们使用了 await，后面跟了 get 方法，
在执行这 10 个协程的时候，如果遇到了 await，那么就会将当前协程挂起，转而去执行其他的协程，
直到其他的协程也挂起或执行完毕，再进行下一个协程的执行。

@Time : 2020/5/28 15:37
@Author: zhangqian
"""

import aiohttp
import asyncio
import time

start = time.time()


async def request():
    url = "https://www.baidu.com/"
    print('Waiting for ', url)
    res = await get(url)  # 要实现异步处理，我们得先要有挂起的操作
    print('Get response from ', url, 'response', res)


async def get(url):
    session = aiohttp.ClientSession()
    res = await session.get(url)  # await 用来用来声明程序挂起
    await res.text()
    await session.close()
    return res


tasks = [asyncio.ensure_future(request()) for _ in range(10)]  # 定义 task 对象
loop = asyncio.get_event_loop()  # 创建了一个事件循环 loop
loop.run_until_complete(asyncio.wait(tasks))  # 将10个协程注册到loop
end = time.time()
print('Cost time :', (end-start))

