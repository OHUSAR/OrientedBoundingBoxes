from Core.Geometry.Intersections import IntersectLineSegment

class Axis:
    def __init__( self, dirVector, point ):
        self.dir = dirVector
        self.point = point

def _GetSide( vertex, axis ):
    return -1 # TODO

def SliceObject( vertices, axis ):
    verts1 = []
    verts2 = []

    for i in range( len(vertices ) ):
        vertex = vertices[i]
        side = _GetSide( vertex )

        if side == -1:
            verts1.append( vertex )
        elif side == 1:
            verts2.append( vertex )
        else:
            verts1.append( vertex )
            verts2.append( vertex )

        intersectVertex = IntersectLineSegment( axis.dir, axis.point, vertex, vertices[( i+1 ) % len(vertices)] )
        if intesectVertex is not None:
            verts1.append( intersectVertex )
            verts2.append( intersectVertex )
        
    return verts1, verts2
