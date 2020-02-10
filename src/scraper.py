from bs4 import BeautifulSoup
import requests
import logging
import json

START_WIKI_PAGE = 'https://en.wikipedia.org/wiki/Morgan_Freeman'


response = requests.get(START_WIKI_PAGE)
soup = BeautifulSoup(response.text, 'html.parser')
posts = soup.find_all(class_='div-col columns column-width')

for post in posts:
    # test = posts.find(class_='mw-headline')
    # print(test.get_text())
    it = post.find()
    title = post.find('a')['title']
    link = post.find('a')['href']
    print(title, link)
