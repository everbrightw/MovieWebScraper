from src.graphModel.actor import Actor


class Vertex:
    """
    Node used for storing actor or film data object
    """

    def __init__(self, val: object):
        self.val = val
        self.key = val.name
        self.edges = []  # storing all edges that out go from this vertex

    def get_val(self) -> object:
        """
        :return:storing information in current Vertex
        """
        return self.val

    def add_edge(self, edge):
        """
        add an edge from current node to end Vertex
        :param edge:
        :return:
        """
        self.edges.append(edge)
