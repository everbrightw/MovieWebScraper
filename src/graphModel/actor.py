import requests
import time
from bs4 import BeautifulSoup
import json


class Actor(object):

    def __init__(self, name: str, age: int, total_gross: int, films: dict):
        self.name = name
        self.age = age
        self.films = films
        self.total_gross = total_gross

    def print_actor_name(self):
        print("Actor Name: " + self.name)

    def get_dict(self) -> dict:
        ret = {'json_class': 'Actor', 'name': self.name, 'age': self.age, 'films': list(self.films.keys())}
        return ret
