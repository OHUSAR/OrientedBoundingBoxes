from GUI.oobb_hierarchy import OOBBHierarchy

class PolygonStorage:
    def __init__(self):
        self.polygons = {}
        self.ordered = []

    def add(self, polygon):
        self.polygons[polygon.canvas_id] = polygon
        self.ordered.append(polygon)

    def get(self, i, by_order=False):
        if by_order:
            return self.ordered[i]
        return self.polygons[i]

class PolygonObject:
    def __init__(self, vertices):
        self.vertices = vertices
        self.canvas_id = None
        self.oobb_canvas_ids = {}

        self.oobb_hierarchy = OOBBHierarchy(vertices)

    def all_canvas_ids(self):
        return [self.canvas_id] + self.oobb_hierarchy.canvas_ids()

    def OOBBs(self):
        queue = [self.oobb_hierarchy.root]
        result = []
        while queue:
            oobb_level = queue.pop(0)
            result.append(oobb_level)
            for ch in oobb_level.children:
                if ch is not None:
                    queue.append(ch)
        return result

    def move(self, x, y):
        for vector in self.vertices:
            vector[0], vector[1] = vector[0] + x, vector[1] + y
        self.oobb_hierarchy.move(x, y)