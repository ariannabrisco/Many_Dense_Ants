"""
path object:
- intensity = 0
v1 = Node()
v2 = Node()
distance = Inf
"""
import math


class Path:
    def __init__(self):
        self.path = []
        self.shortestPath = []
        self.intensity = 0
        self.distance = math.inf
        self.v1 = Node()
        self.v2 = Node()

    def addPath(self, path):
        self.path.append(path)

    def addShortestPath(self, path):
        self.shortestPath.append(path)

    def addIntensity(self, intensity):
        self.intensity = intensity

    def addDistance(self, distance):
        self.distance = distance