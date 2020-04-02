import requests
from bs4 import BeautifulSoup

URL = 'https://xa.58.com/qzyewu/?PGTID=0d202409-001e-3223-b76a-013e693c0dda&ClickID=4'
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36' }
wb_data = requests.get(URL,headers=headers)
soup = BeautifulSoup(wb_data.content, 'lxml')
print(soup)
