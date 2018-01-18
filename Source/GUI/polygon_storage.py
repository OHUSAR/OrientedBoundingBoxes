from Core.SimulationObjects import SimulationPolygon

class PolygonStorage:
    class Entry:
        def __init__(self, poly, polyGfx ):
            self.polygon = poly
            self.polygonGfx = polyGfx
    
    def __init__(self):
        self.polygons = {}
        self.ordered = []

    def add(self, polygon, polygonGfx, canvasId):
        entry = self.Entry( polygon, polygonGfx )
        self.polygons[canvasId] = entry
        self.ordered.append( entry )

    def get(self, i, by_order=False):
        if by_order:
            return self.ordered[i]
        return self.polygons[i]

    def __len__(self):
        return len(self.ordered)

    def ReplaceBy( self, newData ):
        self.polygons = newData
        self.ordered = list( self.polygons.values() )

