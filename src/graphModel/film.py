import requests
import time
from bs4 import BeautifulSoup
import json


class Film(object):

    def __init__(self, name: str, actors: list, year: int, total_gross: int):
        self.name = name
        self.actors = actors
        self.list = list
        self.year = year
        self.total_gross = total_gross
