from Core.BasicDefs import *
from Core.Utils.LinearAlgebra import Distance 

class Turn:
    CCW = -1
    COLINEAR = 0
    CW = 1

def _GetTurn( a, b, c ):
    return np.sign( ( ( b[0] - a[0] ) * ( c[1] - a[1] ) ) -
                    ( ( c[0] - a[0] ) * ( b[1] - a[1] ) ) )

def _GetNextHullVertex( vertices, startPt ):
    endPt = vertices[0]
    for candidatePt in vertices[1:]:
        turn = _GetTurn( startPt, endPt, candidatePt )
        if (   turn == Turn.CCW or
             ( turn == Turn.COLINEAR and Distance( startPt, endPt ) < Distance( startPt, candidatePt ) ) ):
            endPt = candidatePt
    return endPt
    

def GetConvexHull( vertices ):
    if len( vertices ) < 3:
        raise ValueError( "convex hull cannot be computed for {} vertices".format( len(vertices ) ) )

    convexHull = [ min( vertices, key = lambda v: ( v[0], v[1] ) ) ]

    for i in range( len( vertices ) ):
        endpoint = _GetNextHullVertex( vertices, convexHull[i] )
        if np.allclose( convexHull[0], endpoint ):
            break
        convexHull.append( endpoint )
        
    return [ vector(v) for v in convexHull ]

