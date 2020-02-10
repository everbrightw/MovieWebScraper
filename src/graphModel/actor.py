import requests
import time
from bs4 import BeautifulSoup
import json


class Actor(object):

    def __init__(self, name: str, age: int, nationality: str, total_gross: int):
        self.name = name
        self.age = age
        self.nationality = nationality
        self.total_gross = total_gross

