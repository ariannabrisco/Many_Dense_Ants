"""
path object:
- intensity = 0
v1 = Node()
v2 = Node()
distance = Inf
need weights (distances)
"""

import math


class Path:
    def __init__(self, intensity, distance):
        self.path = []
        self.shortestPath = []
        self.intensity = intensity
        self.distance = distance
        self.v1 = Node()
        self.v2 = Node()

    def addPath(self, path):
        self.path.append(path)

    def addShortestPath(self, path):
        self.shortestPath.append(path)
        return (f"The shortest path from start to finish is: {self.shortestPath}")  # can decide how output looks

    def addIntensity(self, intensity):
        self.intensity = 0

    def addDistance(self, distance):
        self.distance = math.inf

    def findDistance(self, v1, v2):
        distanceBetween = v1.distance - v2.distance
        return distanceBetween
