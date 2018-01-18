from Core.Geometry.Utils import GetOrientedEdges, GetEdgeNormals

class Polygon:

    def __init__(self, vertices, ch = None):
        self.vertices = vertices
        self.edgeNormals = GetEdgeNormals( GetOrientedEdges( vertices ) )
        
        self.chVertices = ch

    def GetVertices( self ):
        return self.vertices

    def GetEdgeNormals( self ):
        return self.edgeNormals
    
    def __getitem__(self, vertIx):
        return self.vertices[vertIx]

    def Move( self, dx, dy ):
        for vertex in self.vertices:
            vertex[0] += dx
            vertex[1] += dy


    
