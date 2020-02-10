from bs4 import BeautifulSoup
from datetime import datetime as dt
import src.utils as utils
import re

POWERS = {
    'thousand': 10 ** 3,
    'million': 10 ** 6,
    'billion': 10 ** 9
}


def get_film_name(soup: BeautifulSoup) -> str:
    return soup.find('th', {'class': 'summary'}).text


def get_film_release_year(soup: BeautifulSoup) -> dt.date:
    date_str = soup.find('span', {'class': ['bday', 'dtstart', 'published']})

    if date_str is None:
        date_str = "0-0-0"
    else:
        date_str = date_str.text

    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%Y-%m'):
        try:
            return dt.strptime(date_str, fmt).date()
        except ValueError:
            pass


def get_movie_page_actors(soup: BeautifulSoup) -> dict:
    """
    get all actors that are relate to this movie
    :param soup:
    :return:
    """
    ret = {}
    title_child = soup.find(id='Cast')
    # if title_child is None:
    #     return ret

    table_sibling = title_child.find_parent().find_next_sibling('div')
    for row in table_sibling.find_all('a'):  # finding all urls under wiki table
        try:
            ret[row['title']] = utils.format_wiki_url(row['href'])
        except KeyError:
            pass

    return ret


def get_movie_gross(soup: BeautifulSoup) -> float:
    """
    format and
    return the grossing information about this movie
    :param soup:
    :return: grossing of current movie (box office)
    """
    box_office_sibling = soup.find('th', string='Box office')
    # if box_office_sibling is None:
    #     return Float()

    box_office_str = box_office_sibling.find_parent().find('td').get_text()

    # re.sub('[.*?]', '', box_office_str)
    # replacing end notes
    if box_office_str.endswith(']'):
        box_office_str = box_office_str[:-3]
    # removing $ sign
    box_office_str = box_office_str.replace('$', '')

    if '.' in box_office_str:
        # powers situation
        prefix, multiplier = box_office_str.split(' ')
        grossing = float(prefix) * POWERS[multiplier]
        return grossing
    elif ',' in box_office_str:
        # non powers situation
        box_office_str = box_office_str.replace(',', '')
        grossing = float(box_office_str)
        return grossing
    else:
        return float(''.join(re.findall('\d+', box_office_str)))
