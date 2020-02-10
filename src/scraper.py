import time
from bs4 import BeautifulSoup
import src.utils as utils
import requests
import src.actor_page as actor_page
import src.film_page as film_page
import logging
from collections import deque


from src.graphModel.actor import Actor
from src.graphModel.film import Film
from src.graphModel.graph import Graph
from src.graphModel.vertex import Vertex

START_WIKI_PAGE = 'https://en.wikipedia.org/wiki/Cary_Elwes'

if __name__ == '__main__':
    start_time = time.time()

    logging.getLogger().setLevel(logging.INFO)
    logging.info('start scraping')

    visited_urls = set()  # storing visited urls
    actors = {}  # storing actors
    films = {}  # storing films

    curr_url = ''
    pages_queue = deque(['https://en.wikipedia.org/wiki/Cary_Elwes'])
    while len(actors) < 250 or len(films) < 125:
        curr_url = pages_queue.popleft()
        if curr_url in visited_urls:
            continue

        logging.info(f'visiting {curr_url}')
        visited_urls.add(curr_url)
        try:
            response = requests.get(curr_url)
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception:
            pass
        try:
            if utils.is_actor_page(soup):
                logging.info(f'{curr_url} is an actor page')
                # this is an actor page
                films_pages_dict = actor_page.get_actor_page_movies(soup)
                actor = Actor(actor_page.get_actor_name(soup), actor_page.get_actor_age(soup), 0, films_pages_dict)
                actors[actor.name] = actor
                pages_queue.extend(films_pages_dict.values())

            if utils.is_film_page(soup):
                logging.info(f'{curr_url} is an film page')
                # this is a film page
                actors_pages_dict = film_page.get_movie_page_actors(soup)
                film = Film(film_page.get_film_name(soup), film_page.get_film_release_year(soup),
                            film_page.get_movie_gross(soup), actors_pages_dict, curr_url)
                films[film.name] = film
                pages_queue.extend(actors_pages_dict.values())
        except Exception:
            logging.warning("cant find val")
            pass

    g = Graph()
    # generating a graph
    for it_actor in actors:
        g.add_vertex(Vertex(actors[it_actor]))
    for it_film in films:
        g.add_vertex(Vertex(films[it_film]))

    g.connect_vertices_with_edges(actors, films)  # creat edges and connect vertices
    g.print_graph()

    print("total vertices ", len(g.vertices))
    elapsed_time = time.time() - start_time
    print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

    g.to_json()
