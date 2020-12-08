import base64
import hashlib
import time
from typing import List, Any

import requests

'''
列表页 Ajax 入口寻找
js生成token分析：
1.全局搜索关键词
2.xhr断点
token :_0x2b4ffd
    1.传入的/api/movie会构造一个初始化列表，变量命名为_0x5b4f53
    2.获取当前时间戳，变量命名为_0x4814ff，然后push到_0x5b4f53
    3.将变量_0x5b4f53用“,”拼接，然后进行SHA1编码，命名为_0x32d914
    4.将_0x32d914和_0x4814ff（时间戳）用“,”拼接，命名为_0x829249
    5.将_0x829249进行Base64编码，命名为_0x3ea520，就是最后的token
'''
INDEX_URL = 'https://dynamic6.scrape.cuiqingcai.com/api/movie?limit={limit}&offset={offset}&token={token}'
LIMIT = 10
OFFSET = 0


def get_token(args: List[Any]):
    # 1.取当前时间戳
    print(int(time.time()))
    timestamp = str(int(time.time()))
    args.append(timestamp)
    # 2.进行 SHA1 编码
    sign = hashlib.sha1(','.join(args).encode('utf-8')).hexdigest()
    print(sign)
    # 3.Base64 编码
    return base64.b64encode(','.join([sign, timestamp]).encode('utf-8')).decode('utf-8')


args = ['/api/movie']
token = get_token(args=args)
print(token)

url = INDEX_URL.format(limit=LIMIT, offset=OFFSET, token=token)
response = requests.get(url)
print('response', response.json())
