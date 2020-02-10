from typing import List
import json
from src.graphModel.actor import Actor
from src.graphModel.film import Film
from src.graphModel.vertex import Vertex


class Edge:
    def __init__(self, start: Vertex, end: Vertex, weight: float):
        self.start = start
        self.end = end
        self.weight = weight


def from_json_to_graph(json_file_str: str, g):

    actors = {}  # storing actors
    films = {}  # storing films
    with open(json_file_str, encoding='utf-8') as json_file:
        data = json.load(json_file)
        for value_dict in data[0].values():
            for key in value_dict.keys():
                if key == 'json_class' and value_dict.get(key) == 'Actor':
                    # This is an  actor
                    movies_dict = {}
                    for m in value_dict['movies']:
                        movies_dict[m] = ''
                    actor = Actor(value_dict['name'], value_dict['age'], value_dict['total_gross'],
                                  movies_dict)
                    g.actor_list.append(actor)
                    actors[actor.name] = actor

        for value_dict in data[1].values():
            for key in value_dict.keys():
                if key == 'json_class' and value_dict.get(key) == 'Movie':
                    # This is a movie
                    actors_dict = {}
                    for a in value_dict['actors']:
                        actors_dict[a] = ''

                    film = Film(value_dict['name'], value_dict['year'], value_dict['box_office'], actors_dict,
                                value_dict['wiki_page'])
                    g.film_list.append(film)
                    films[film.name] = film
    for it_actor in actors:
        g.add_vertex(Vertex(actors[it_actor]))
    for it_film in films:
        g.add_vertex(Vertex(films[it_film]))
    g.connect_vertices_with_edges(actors, films)
    # g.print_graph()
    g.to_json()
    return g


class Graph:
    def __init__(self):
        self.vertices = {}
        self.film_list = []
        self.actor_list = []

    def get_vertex_by_name(self, name) -> Vertex:
        return self.vertices.get(name)

    def add_vertex(self, vertex: Vertex):
        """
        add vertex in graph
        :param vertex:
        :return:
        """
        if isinstance(vertex, Vertex) and vertex.key not in self.vertices:
            self.vertices[vertex.key] = vertex
            return True
        else:  # adding vertex failed
            return False

    def add_edge(self, edge: Edge):
        """
        add edges
        :param edge:
        :return:
        """
        if edge.start in self.vertices.values() and edge.end in self.vertices.values():
            edge.start.add_edge(edge)
            return True
        else:  # adding edge failed
            print("failed adding edges")
            return False

    def connect_vertices_with_edges(self, actors, films):
        """
        connect vertices together with adjacent dictionary
        :param actors:
        :param films:
        :return:
        """
        for vertex_key in list(self.vertices.keys()):
            val = self.vertices.get(vertex_key).get_val()
            if isinstance(val, Film):
                # connect from film to actor
                actor_names = []
                for actor_name in actors.keys():
                    if actor_name in val.actors.keys():
                        actor_names.append(actor_name)
                # self.vertices[vertex_key] = actor_vertices
                for actor_name in actor_names:
                    # print('adding edges')
                    # print(actor_name)
                    self.add_edge(Edge(self.vertices.get(vertex_key), self.get_vertex_by_name(actor_name),
                                       val.total_gross + actors.get(actor_name).age))

            if isinstance(val, Actor):
                # connect from actor to film
                film_names = []
                for film_name in films.keys():
                    if film_name in val.films.keys():
                        # matched
                        film_names.append(film_name)
                # self.vertices[vertex_key] = film_vertices
                for film_name in film_names:
                    # print('adding edges')
                    # print(film_name)
                    self.add_edge(Edge(self.vertices.get(vertex_key), self.get_vertex_by_name(film_name),
                                       val.age + films.get(film_name).total_gross))

    def print_graph(self):
        """
        printing graph
        :return:
        """
        for key in list(self.vertices.keys()):
            val = self.vertices.get(key).get_val()
            if isinstance(val, Film):
                val.print_film_name()
                print("Edges: {")
                for it in self.vertices.get(key).edges:
                    print("Edge: " + "from: " + it.start.key + " to: " +
                          it.end.key)
                print(" }")
            if isinstance(val, Actor):
                val.print_actor_name()
                print("Edges: {")
                for it in self.vertices.get(key).edges:
                    print("Edge: " + "from: " + it.start.key + " to: " +
                          it.end.key)
                print(" }")

    def to_json(self):
        """
        Convert to a dictionary of movies and dictionary of actors
        :return:
        """
        sum_dict = {}
        for vertex in self.vertices.values():
            if isinstance(vertex.get_val(), Film):
                film_dict = vertex.get_val().get_dict()
                sum_dict[film_dict.get('name')] = film_dict
            if isinstance(vertex.get_val(), Actor):
                actor_dict = vertex.get_val().get_dict()
                sum_dict[actor_dict.get('name')] = actor_dict

        j = json.dumps(sum_dict, indent=4)

        f = open('out_from_graph.json', 'w')
        print(j, file=f)

        f.close()
