# coding=utf-8

"""
Ajax 获取电影信息
@Time : 2020/5/23 15:53
@Author: zhangqian
"""

import requests
import logging
import json
from os import makedirs
from os.path import exists


logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s:%(message)s')
INDEX_URL = 'https://dynamic1.scrape.cuiqingcai.com/api/movie/?limit={limit}&offset={offset}'


def scrape_api(url):

    """
    根据url获取返回数据
    :param url:
    :return:
    """
    logging.info('scraping %s...', url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        logging.error('get?invalid?status?code?%s?while?scraping?%s', response.status_code, url)
    except requests.RequestException:
        logging.error('error?occurred?while?scraping?%s', url, exc_info=True)


LIMIT = 10


def scrape_index(page):
    """
    根据page生成请求url、调用返回数据
    :param page:
    :return:
    """
    url = INDEX_URL.format(limit=LIMIT, offset=LIMIT * (page - 1))
    return scrape_api(url)


DETAIL_URL = 'https://dynamic1.scrape.cuiqingcai.com/api/movie/{id}'


def scrape_detail(id):
    """
    根据电影的id 获取电影详情url
    :param id:
    :return:
    """
    url = DETAIL_URL.format(id=id)
    return scrape_api(url)


RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)


def save_data(data):
    """
    存储json数据到本地
    :param data:
    :return:
    """
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


TOTAL_PAGE = 10


def main():
    for page in range(1, TOTAL_PAGE + 1):
        index_data = scrape_index(page)
        for item in index_data.get('results'):
            id = item.get('id')
            detail_data = scrape_detail(id)
            logging.info('detail data %s', detail_data)
            save_data(detail_data)


if __name__ == '__main__':
    main()
