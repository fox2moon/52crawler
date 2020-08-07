import requests
from urllib.parse import urljoin

BASE_URL = 'https://login2.scrape.cuiqingcai.com/'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

session = requests.Session()
login_response = session.post(LOGIN_URL, data={'username': USERNAME, 'password': PASSWORD})
cookies = session.cookies
print('Cookies', cookies)
index_response = session.post(INDEX_URL)
print('index_response Status', index_response.status_code)
print('index_response URL', index_response.url)

