import requests
import logging
from os import mkdir
from os.path import exists
import json

TOTAL_PAGE = 2
LIMIT = 10
INDEX_URL = "https://dynamic1.scrape.cuiqingcai.com/api/movie/?limit={limit}&offset={offset}"
DETAIL_URL = 'https://dynamic1.scrape.cuiqingcai.com/api/movie/{id}'

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(levelname)s:%(message)s')


def scrape_index(page):
    index_url = INDEX_URL.format(limit=LIMIT, offset=(page-1)*LIMIT)
    return scrape_api(index_url)


def scrape_detail(id):
    detail_url = DETAIL_URL.format(id=id)
    return scrape_api(detail_url)


def scrape_api(url):
    logging.info('scraping %s...', url)
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        logging.error('get?invalid?status?code?%s?while?scraping?%s', res.status_code, url)
    except requests.RequestException:
        logging.error('error?occurred?while?scraping?%s', url, exc_info=True)


RESULTS_DIR = 'results2'
exists(RESULTS_DIR) or mkdir(RESULTS_DIR)


def save_json(data):
    name = data.get('name')
    json_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(json_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)


def main():
    for page in range(1, TOTAL_PAGE+1):
        res_index = scrape_index(page)
        for item in res_index.get('results'):
            id = item.get("id")
            res_detail = scrape_detail(id)
            logging.info('detail data %s', res_detail)
            save_json(res_detail)


if __name__ == '__main__':
    main()
