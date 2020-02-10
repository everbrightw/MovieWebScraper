import requests
import time
from bs4 import BeautifulSoup
import json


class Film(object):

    def __init__(self, name: str, year: int, total_gross: float, actors: dict, wiki_page: str):
        self.name = name
        self.year = str(year)
        self.total_gross = total_gross
        self.actors = actors
        self.wiki_page = wiki_page

    def print_film_name(self):
        print("Film: " + self.name)

    def get_dict(self) -> dict:
        ret = {'json_class': 'Movie', 'name': self.name, 'year': self.year,
               'total_gross': self.total_gross, 'actors': list(self.actors.keys())}
        return ret
