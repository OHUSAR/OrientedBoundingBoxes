from Core.BasicDefs import *
from Core.Geometry.Intersections import IntersectLineSegment

class Axis:
    def __init__( self, dirVector, point ):
        self.dir = dirVector
        self.point = point

def _GetSide( vertex, axis ):
    pt = axis.point
    pt2 = pt + axis.dir
    
    det = ( ( pt2[0] - pt[0] ) * ( vertex[1] - pt[1] ) -
            ( pt2[1] - pt[1] ) * ( vertex[0] - pt[0] ) )
    return np.sign( det )

def SliceObject( vertices, axis ):
    verts1 = []
    verts2 = []

    for i in range( len(vertices ) ):
        vertex = vertices[i]
        side = _GetSide( vertex, axis )

        if side == -1:
            verts1.append( vertex )
        elif side == 1:
            verts2.append( vertex )
        else:
            verts1.append( vertex )
            verts2.append( vertex )

        intersectVertex = IntersectLineSegment( axis.dir, axis.point, vertex, vertices[( i+1 ) % len(vertices)] )
        if intersectVertex is not None:
            verts1.append( intersectVertex )
            verts2.append( intersectVertex )
        
    return verts1, verts2
