import requests
from urllib.parse import urljoin

BASE_URL = 'https://login3.scrape.cuiqingcai.com/'
LOGIN_URL = urljoin(BASE_URL, '/api/login')
INDEX_URL = urljoin(BASE_URL, '/api/book')
USERNAME = 'admin'
PASSWORD = 'admin'

response_login = requests.post(LOGIN_URL, json={
    'username': USERNAME,
    'password': PASSWORD
})
data = response_login.json()
jwt = data.get('token')
print(jwt)

headers = {
    'authorization': f'jwt {jwt}'
}
print(headers)

index_response = requests.get(INDEX_URL, params={'limit': 18, 'offset': 0}, headers=headers)
print('index_response Status', index_response.status_code)
print('index_response URL', index_response.url)
