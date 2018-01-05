import numpy as np

from Core.BoundingBox.OrientedBoundingBox import GetOrientedBBox
from Core.ConvexHull.ConvexHull import GetConvexHull
from Core.Geometry.Slicing import SliceObject, Axis
from Core.Geometry.Utils import GetOrientedEdges, vector


class OOBBHierarchy:
    def __init__(self, vertices, depth=3):
        self.root = None
        self.vertices = vertices
        self.depth = depth
        self.compute()

    def compute(self):
        self.root = self.compute_level(self.vertices, 0)

    def compute_level(self, vertices, level):
        if level >= self.depth:
            return None

        oobb_level = OOBBLevel(vertices)

        ax = Axis(oobb_level[3] - oobb_level[0], (oobb_level[0] + oobb_level[1]) / 2)
        ax2 = Axis(oobb_level[1] - oobb_level[0], (oobb_level[0] + oobb_level[3]) / 2)

        sliceA, sliceB = SliceObject(vertices, ax)
        slice1, slice2 = SliceObject(sliceA, ax2)
        slice3, slice4 = SliceObject(sliceB, ax2)
        slices = [slice1, slice2, slice3, slice4]

        oobb_level.add_children([self.compute_level(s, level + 1) for s in slices])
        return oobb_level

    def move(self, x , y):
        q = [self.root]
        while q:
            oobb_level = q.pop()
            oobb_level.move(x, y)
            for ch in oobb_level.children:
                if ch is not None:
                    q.append(ch)

    def canvas_ids(self):
        ids = []
        q = [self.root]
        while q:
            oobb_level = q.pop()
            ids.append(oobb_level.canvas_id)
            for ch in oobb_level.children:
                if ch is not None:
                    q.append(ch)
        return ids

class OOBBLevel:
    def __init__(self, vertices):
        self.vertices = [np.array(v) for v in vertices]
        self.oobb = None
        self.children = []
        self.canvas_id = None

        self.compute()

    def compute(self):
        vertices = [vector(v) for v in self.vertices]
        ch = GetConvexHull(vertices)
        edges = GetOrientedEdges(ch)
        oobb = GetOrientedBBox(ch, edges)
        self.oobb = [vector(v) for v in self.round_oobb(oobb)]
        return self.oobb

    def move(self, x, y):
        for vector in self.oobb:
            vector[0], vector[1] = vector[0] + x, vector[1] + y

    def OOBB(self):
        if self.oobb is None:
            self.compute()
        return self.round_oobb(self.oobb + [self.oobb[0]])

    def round_oobb(self, oobb):
        rounded_oobb = []
        for v in oobb:
            rounded_oobb.append([round(x) for x in v])
        return rounded_oobb

    def __getitem__(self, item):
        return self.oobb[item]

    def add_children(self, children):
        self.children = children
