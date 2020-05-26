# coding=utf-8
"""
获取电影列表然后获取详情页数据
@Time : 2020/5/25 16:28
@Author: zhangqian
"""

import logging
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from os import makedirs
from os.path import exists
import json
import pymongo

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')

INDEX_PAGE_URL = 'https://dynamic2.scrape.cuiqingcai.com/page/{page}'
INDEX_URL = 'https://dynamic2.scrape.cuiqingcai.com'
TIME_OUT = 10
TOTAL_PAGE = 2
RESULT_DIR = 'result'
exists(RESULT_DIR) or makedirs(RESULT_DIR)

MONGO_CONNECTION_STRING = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'movies'
MONGO_COLLECTION_NAME = 'movies'
client = pymongo.MongoClient(MONGO_CONNECTION_STRING)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]


# 浏览器无头模式
options = webdriver.ChromeOptions()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
wait = WebDriverWait(browser, TIME_OUT)


def get_index(page):
    """
    根据页码参数拼接url,模拟浏览器获取列表页面
    :param page:
    :return:
    """
    url = INDEX_PAGE_URL.format(page=page)
    get_page(url, condition=EC.visibility_of_all_elements_located, locator=(By.CSS_SELECTOR, "#index .el-card"))


def get_page(url, condition, locator):
    """
    模拟打开url网页
    :param url:目标网页url
    :param condition:页面加载的判定条件
    :param locator:元素定位器
    :return:
    """
    logging.info("scrapy page..."+url)
    try:
        browser.get(url)
        wait.until(condition(locator))
    except TimeoutError:
        logging.error('error occurred while scraping %s', url, exc_info=True)


def parse_index():
    """
    解析列表 获取详情页url
    :return:
    """
    selector = browser.find_elements_by_css_selector("#index .name")
    for a in selector:
        href = a.get_attribute("href")
        yield urljoin(INDEX_URL, href)


def get_detail(url):
    get_page(url, condition=EC.visibility_of_element_located, locator=(By.CSS_SELECTOR, ".m-b-sm"))


def parse_detail():
    url = browser.current_url
    name = browser.find_element_by_class_name("m-b-sm").text
    categories = [element.text for element in browser.find_elements_by_css_selector(".categories span")]
    cover = browser.find_element_by_class_name("cover").get_attribute("src")
    score = browser.find_element_by_class_name("score").text
    drama = browser.find_element_by_css_selector(".drama p").text
    return {
        'url': url,
        'name': name,
        'categories': categories,
        'cover': cover,
        'score': score,
        'drama': drama
    }


def save_file(data):
    name = data.get("name")
    data_path = f'{RESULT_DIR}/{name}.json'
    json.dump(data, open(data_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def save_mongodb(data):
    collection.update_one({
        'name': data.get('name')
    }, {
        '$set': data
    }, upsert=True)


def main():
    try:
        for page in range(1, TOTAL_PAGE+1):
            get_index(page)
            detail_urls = parse_index()
            for detail_url in list(detail_urls):
                logging.info("get detail url %s ", detail_url)
                get_detail(detail_url)
                detail_data = parse_detail()
                logging.info('detail data %s', detail_data)
                # save_file(detail_data)
                save_mongodb(detail_data)
                logging.info('data saved successfully')
    finally:
        browser.close()


if __name__ == '__main__':
    main()

