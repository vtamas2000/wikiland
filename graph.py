import networkx as nx
import numpy as np
from typing import List


class SuperGraph:

    """
    Container class for all the NGraphs
    """

    def __init__(self, max_distance) -> None:
        self._max_dist = max_distance
        self._ngraphs = [NGraph(i) for i in range(1, self._max_dist + 1)]


    def __repr__(self):
        return (f'Supergraph with {len(self._ngraphs)} NGraphs with each having '
                f'{ {ngraph.nth: len(ngraph.edges()) for ngraph in self._ngraphs} } edges')


    def add_article(self, word_list: List[str]) -> None:
        for ngraph in self._ngraphs:
            ngraph.add_edges_from_text(word_list)


    def tally(self) -> None:
        for i in range(1, self._max_dist + 1):
            raise NotImplementedError
    


class NGraph(nx.MultiDiGraph):

    """
    Class for containing the information about words with N distance
    """

    def __init__(self, nth):
        super().__init__()
        self._nth = nth


    @property
    def nth(self):
        return self._nth


    def add_edges_from_text(self, word_list: List[str]) -> None:

        """
        Adds edges from a list of words
        """

        if self._nth < len(word_list):
            rolled = np.roll(word_list, -self._nth)
            edges = list(zip(word_list, rolled))[:-self._nth]  # Remove last element so it does not wrap around
            self.add_edges_from(edges)


    def count_edges(self) -> nx.DiGraph:
        returnGraph = nx.DiGraph()
        for edge in self.edges():
            w = self.number_of_edges(*edge)
            returnGraph.add_edge(*edge, weight=w)

        return returnGraph
