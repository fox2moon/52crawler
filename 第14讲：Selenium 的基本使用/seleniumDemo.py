# coding=utf-8
"""
@Time : 2020/5/24 15:21
@Author: zhangqian
"""
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

try:
    browser = webdriver.Chrome()
    browser.get("https://www.baidu.com/")
    input_ = browser.find_element_by_id("kw")
    input_.send_keys("James")
    input_.send_keys(Keys.ENTER)
    print(browser.current_url)
    print(type(browser.page_source))
    print(browser.page_source.encode("utf-8"))
    print(browser.get_cookies())
except TimeoutException:
    print('Time Out')
finally:
    browser.close()


