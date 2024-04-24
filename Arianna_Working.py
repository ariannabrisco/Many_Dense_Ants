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
    def __init__(self, distance):
        self.path = []
        self.shortestPath = []
        self.distance = distance
        self.i = Node()
        self.j = Node()

    def addPath(self, path):
        self.path.append(path)

    def addShortestPath(self, path):
        self.shortestPath.append(path)
        return (f"The shortest path from start to finish is: {self.shortestPath}")  # can decide how output looks

    def addDistance(self, distance):
        self.distance = math.inf

    def findDistance(self, i, j):
        distanceBetween = i.distance - j.distance
        return distanceBetween

class Node:
    def __init__(self, intensity):
        self.intensity = intensity

    def addIntensity(self, intensity):
        self.intensity = 1
