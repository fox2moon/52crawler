# coding=utf-8
"""
协程的入门使用 ：asyncio
@Time : 2020/5/28 10:42
@Author: zhangqian
"""
import asyncio
import requests

'''
协程定义
async 定义的方法就会变成一个无法直接执行的 coroutine 对象，
必须将其注册到事件循环loop中才可以执行'''


# async def execute(x):
#     print(x)
# coroutine = execute(1)
# print('coroutine: ', coroutine)
# print("After calling execute.")
# loop = asyncio.get_event_loop()
# loop.run_until_complete(coroutine)
# print("After calling loop.")


'''
task对coroutine对象的进一步封装
根据task这些状态来获取协程对象的执行情况'''


# async def execute(x):
#     print(x)
#     return x
# coroutine = execute(1)
# print('coroutine: ', coroutine)
# print('After calling execute.')
# loop = asyncio.get_event_loop()
# task = loop.create_task(coroutine)
# task = asyncio.ensure_future(coroutine) # 定义task对象的另一种方式
# print('task: ', task)
# loop.run_until_complete(task)
# print('task: ', task)
# print('After calling loop.')


'''task 绑定回调'''


# async def request():
#     res = requests.get('https://www.baidu.com/')
#     return res
#
#
# def callback(task):
#     print("status: ", task.result())
#
#
# coroutine = request()
# task = asyncio.ensure_future(coroutine)
# task.add_done_callback(callback)
# print('Task:', task)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(task)
# print('Task:', task)

'''多任务协程 列表传给asyncio的wait'''


async def request():
    res = requests.get("https://www.baidu.com/")
    return res


tasks = [asyncio.ensure_future(request()) for _ in range(5)]
print('tasks:', tasks)
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
print('tasks:', tasks)
