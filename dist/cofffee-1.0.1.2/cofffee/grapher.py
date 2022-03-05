import pygame
import numpy as np
import pandas as pd


class Grapher:
    def __init__(self, handler, size):
        self.handler = handler
        self.graphs = []
        self.size = size

        self.initialize_graphs()

    def initialize_graphs(self):
        for i, graph in enumerate(self.graphs):
            # do a better job assigning the positions of multiple graphs
            self.graphs[i].pos = (200, 100)
            self.graphs[i].size = (500, 500)

    def render(self):
        for graph in self.graphs:
            graph.render()
