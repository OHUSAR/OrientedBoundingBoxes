from numpy import array as vector
from numpy import matrix
import numpy as np

class INDICES:
    def __init__(self):
        # BBOX
        self.LEFT = 0
        self.BOTTOM = 1
        self.RIGHT = 2
        self.TOP = 3

        # Coords
        self.X = 0
        self.Y = 1

        # Calipers
        self.VERTICAL = 0
        self.HORIZONTAL = 1
