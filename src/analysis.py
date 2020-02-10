from src.graphModel.graph import Graph, from_json_to_graph
import matplotlib.pyplot as plt
import logging

json_file_str = '/Users/yusenwang/cs242/hw2/fa19-cs242-assignment2/src/graphModel/data.json'
g = Graph()
g = from_json_to_graph(json_file_str, g)
logging.getLogger().setLevel(logging.INFO)


def find_hub_actor(graph: Graph) -> str:
    """
    Who are the "hub" actors in your dataset? That is,
    which actors have the most connections with other actors?
    Two actors have a connection if they have acted in the same movie together.
    :param graph:
    :return:
    """
    logging.info('start finding hub actor')
    actor_connect = {}
    for movie in graph.film_list:
        for actor in movie.actors.keys():
            # print(actor)
            original_list = []
            if actor_connect.get(actor) is not None:
                # dealing with null error
                original_list = actor_connect.get(actor)

            appended_list = original_list + list(movie.actors.keys())
            actor_connect[actor] = appended_list

    max_connections = 0
    hub_actor = None
    hub_actors_dict = {}
    for actor, connections in actor_connect.items():
        hub_actors_dict[actor] = len(connections)
        if len(connections) > max_connections:
            logging.info('current hub actor is: ' + actor)
            hub_actor = actor
            max_connections = len(connections)

    logging.info('we find the hub actor: ' + hub_actor)
    return hub_actor


def find_age_group_total_gross_avg(graph: Graph) -> dict:
    """
    find relation between age groups and gross per person (avg of total gross)
    :param graph:
    :return: dict{key: age_group, val: avg of total gross}
    """
    age_groups_dict = {0: [], 10: [], 20: [], 30: [], 40: [], 50: [], 60: [], 70: [], 80: []}
    age_groups = [20, 30, 40, 50, 60, 70, 80]
    for actor in graph.actor_list:
        if actor.total_gross == 0:
            continue
        for age in age_groups:
            if actor.age < age:  # in the correct age group range, append
                age_groups_dict[age].append(actor.total_gross)
                break
    age_groups_avg_dict = {}
    for age, gross in age_groups_dict.items():
        len_gross = 1
        if len(gross) != 0:
            len_gross = len(gross)
        age_groups_avg_dict[age] = sum(gross) / len_gross
    return age_groups_avg_dict


def find_age_group_total_gross(graph: Graph) -> dict:
    """
    find relation between age group and total gross
    :param graph:
    :return:dict {key: age group, val: total gross}
    """
    age_groups_dict = {0: [], 10: [], 20: [], 30: [], 40: [], 50: [], 60: [], 70: [], 80: []}
    age_groups = [20, 30, 40, 50, 60, 70, 80]
    for actor in graph.actor_list:
        if actor.total_gross == 0:
            continue
        for age in age_groups:
            if actor.age < age:  # in the correct age group range, append
                age_groups_dict[age].append(actor.total_gross)
                break

    age_groups_dict = {age: sum(gross) for age, gross in age_groups_dict.items()}
    return age_groups_dict


def find_movies_years_total_gross(graph: Graph) -> dict:
    """
    find relation between move's year and total gross
    :param graph:
    :return:dict {key: year group, val: total gross}
    """
    year_groups_dict = {1900: [], 1910: [], 1920: [], 1930: [], 1940: [],
                        1950: [], 1960: [], 1970: [], 1980: [], 1990: [], 2000: []}
    year_groups = [1900, 1910, 1920, 1930, 1940,
                   1950, 1960, 1970, 1980, 1990, 2000]
    for film in graph.film_list:
        if film.total_gross == 0:
            continue
        for year in year_groups:
            minus = int(film.year) - year
            if 10 > minus > 0:  # in the correct age group range, append
                year_groups_dict[year].append(film.total_gross)
                break

    year_groups_dict = {year: sum(gross) for year, gross in year_groups_dict.items()}
    return year_groups_dict


def plot_gross_dict(input_dict: dict):
    plt.bar(range(len(input_dict)), list(input_dict.values()), align='center')
    plt.xticks(range(len(input_dict)), list(input_dict.keys()))
    plt.xlabel('Age Group')
    plt.ylabel('Avg total_gross')
    plt.show()


plot_gross_dict(find_movies_years_total_gross(g))
print(find_movies_years_total_gross(g))
print(find_age_group_total_gross_avg(g))
plot_gross_dict(find_age_group_total_gross_avg(g))

find_hub_actor(g)
