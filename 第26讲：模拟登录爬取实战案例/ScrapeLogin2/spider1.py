from urllib.parse import urljoin
import requests

BASE_URL = 'https://login2.scrape.cuiqingcai.com/'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

login_reponse = requests.post(LOGIN_URL, data={
    'username': USERNAME,
    'password': PASSWORD
})

cookies = login_reponse.cookies
print(cookies)

index_reponse = requests.post(INDEX_URL)
print('Response STATUS', index_reponse.status_code)
print('Response URL', index_reponse.url)

