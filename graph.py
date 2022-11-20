import networkx as nx
import numpy as np
from typing import List


class SuperGraph:
    """
    Container class for all the NGraphs
    """

    def __init__(self) -> None:
        pass


class NGraph(nx.DiGraph):
    """
    Class for containing the information about words with N distance
    """

    # def __init__(self, dist: int) -> None:
    #     super().__init__()
    #     self._dist = dist

    # @property
    # def dist(self):
    #     """
    #     Returns the N distance
    #     """
    #     return self._dist


    def add_edges_from_text(self, word_list: List[str]) -> None:
        """
        Adds edges from a list of words
        """
        
        rolled = np.roll(word_list, -1)
        edges = list(zip(word_list, rolled))[:-1]  # Remove last element so that it does not wrap around
        self.add_edges_from(edges)