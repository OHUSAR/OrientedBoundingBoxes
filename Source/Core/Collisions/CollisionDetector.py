from Core.BasicDefs import *

class CollisionObject:
    def __init__( self, vertices, edgeNormals ):
        self.vertices = vertices
        self.edgeNormals = edgeNormals

class _Projection:
    def __init__( self, minPt, maxPt ):
        self.minPt = minPt
        self.maxPt = maxPt
    def Overlaps( self, other ):
        return not ( ( other.minPt >= self.maxPt ) or ( other.maxPt <= self.minPt ) )

def _GetProjection( obj, axis ):
    minPt = np.dot( axis, obj.vertices[0] )
    maxPt = minPt

    for i in range( 1, len( obj.vertices ) ):
        dot = np.dot( axis, obj.vertices[i] )
        if dot > maxPt:
            maxPt = dot
        elif dot < minPt:
            minPt = dot

    return _Projection( minPt, maxPt )

def ObjectsCollide( objA, objB ):
    for projAxis in objA.edgeNormals:
        projA = _GetProjection( objA, projAxis )
        projB = _GetProjection( objB, projAxis )
        if not projA.Overlaps( projB ):
             return False

    for projAxis in objB.edgeNormals:
        projA = _GetProjection( objA, projAxis )
        projB = _GetProjection( objB, projAxis )
        if not projA.Overlaps( projB ):
             return False

    return True
