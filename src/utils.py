"""'
helper functions for format
"""
import re
import datetime
import json
from bs4 import BeautifulSoup
from datetime import datetime as dt


def format_wiki_url(url: str) -> str:
    return 'https://en.wikipedia.org' + url


def is_actor_page(soup: BeautifulSoup) -> bool:
    for headLine in soup.find_all(class_="mw-headline"):
        # head_str = " ".join(re.findall("[a-zA-Z]+", headLine.get_text()))
        # print(head_str)
        if "Filmography" in headLine.get_text():
            # This is an actor page
            # print("found actor page")
            return True
    # print('Its not an actor page')
    return False


def is_film_page(soup: BeautifulSoup) -> bool:
    """
    check if the current url is a film page
    :param soup:
    :return:true if current page is a film page; false otherwise
    """
    if soup.find('table', {'class': ['infobox', 'vevent']}) is None:
        # can not find film's basic information, pass it
        return False

    for headLine in soup.find_all(class_="mw-headline"):

        if "Cast" in headLine.get_text():
            # This is an actor page
            return True
    return False


def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")
