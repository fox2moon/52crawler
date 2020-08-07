import time

import requests
from urllib.parse import urljoin

from selenium import webdriver

BASE_URL = 'https://login2.scrape.cuiqingcai.com/'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

chrome_driver = 'D:/python/chromedriver.exe'
browser = webdriver.Chrome(executable_path=chrome_driver)
browser.get(LOGIN_URL)

browser.find_element_by_css_selector('input[name="username"]').send_keys(USERNAME)
browser.find_element_by_css_selector('input[name="password"]').send_keys(PASSWORD)
browser.find_element_by_css_selector('input[type="submit"]').click()
time.sleep(10)

# get cookies from selennium
cookies = browser.get_cookies()
print(cookies)
browser.close()

# set cookies to requests
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

index_response = session.post(INDEX_URL)
print('index_response Status', index_response.status_code)
print('index_response URL', index_response.url)

