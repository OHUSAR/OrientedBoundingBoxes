from Core.BasicDefs import *
from Core.Utils.LinearAlgebra import *

from math import atan, sin, cos

_EPS = 10e-12

def _AngleToXAxis( ptA, ptB ):
    delta = ptA - ptB 
    return -atan( delta[1] / ( delta[0] + _EPS ) )

def _RotateByAngle( vct, angle ):
    return vector( [ vct[0] * cos (angle) - vct[1] * sin (angle),
		     vct[0] * sin (angle) + vct[1] * cos (angle) ] )

def _GetOrientedBox( minPt, maxPt, angle ):
    UL = [ minPt[0], maxPt[1] ]
    BL = minPt
    BR = [ maxPt[0], minPt[1] ]
    UR = maxPt

    box = [ UL, BL, BR, UR ]
    return [ _RotateByAngle( v, -angle ) for v in box ]

def GetOrientedBBox( vertices ):
    minBox = []
    minArea = float('inf')

    for i in range( len(vertices) ):
        currentVert = vertices[i]
        nextVert = vertices[ (i+1) % len(vertices) ]

        angleToX = _AngleToXAxis( currentVert, nextVert )

        maxPt = [ float('-inf'), float('-inf') ]
        minPt = [ float('inf'), float('inf') ]

        for vert in vertices:
            rotated = _RotateByAngle( vert, angleToX )

            maxPt[0] = max( maxPt[0], rotated[0] )
            maxPt[1] = max( maxPt[1], rotated[1] )

            minPt[0] = min( minPt[0], rotated[0] )
            minPt[1] = min( minPt[1], rotated[1] )

        area = ( maxPt[0] - minPt[0] ) * ( maxPt[1] - minPt[1] )
        if area < minArea:
            minArea = area
            minBox = _GetOrientedBox( minPt, maxPt, angleToX )
    
    return minBox        
