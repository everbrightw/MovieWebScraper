from bs4 import BeautifulSoup
from datetime import datetime as dt
import src.utils as utils


def calculate_age(birthday):
    """
    calculate age by birthday
    :param birthday:
    :return:
    """
    today = dt.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    return age


def get_actor_age(soup: BeautifulSoup) -> int:
    """
    get actor age
    :param soup:
    :return:
    """

    birthday_text = soup.find('span', {'class': 'bday'}).text
    birthday = dt.strptime(birthday_text, '%Y-%m-%d').date()

    return calculate_age(birthday)


def get_actor_page_movies(soup: BeautifulSoup) -> dict:
    """
    get all movies that are relate to this actor
    :param soup:
    :return:
    """
    ret = {}
    title_child = soup.find(id='Filmography')
    if title_child is None:
        return ret

    table_sibling = title_child.find_parent().find_next_sibling('table')
    for row in table_sibling.find_all('a'):  # finding all urls under wiki table
        try:
            ret[row['title']] = utils.format_wiki_url(row['href'])
        except KeyError:
            pass

    return ret


def get_actor_name(soup: BeautifulSoup) -> str:
    """
    get actor name
    :param soup:
    :return:
    """
    return soup.find('div', {'class': 'fn'}).text
