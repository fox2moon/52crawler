from urllib.parse import urljoin

import requests

BASE_URL = 'https://login2.scrape.cuiqingcai.com/'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

login_response = requests.post(LOGIN_URL, data={'username': USERNAME, 'password': PASSWORD}, allow_redirects=False)
cookies = login_response.cookies
print(cookies)

index_response = requests.post(INDEX_URL, cookies=cookies)
print('index_response Status', index_response.status_code)
print('index_response URL', index_response.url)

