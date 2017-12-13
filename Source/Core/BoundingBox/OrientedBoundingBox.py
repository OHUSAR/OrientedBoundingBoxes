from Core.BasicDefs import *
from Core.Utils.AlgebraUtils import *

def _GetExtremePointIndices( vertices ):
    maxPt = [ float('-inf'), float('-inf') ]
    minPt = [ float('inf'), float('inf') ]
    indices = [-1] * 4

    INDEX = INDICES()
    
    for ix, vertex in enumerate( vertices ):
        if vertex[INDEX.X] < minPt[INDEX.X]:
            minPt[INDEX.X] = vertex[INDEX.X]
            indices[INDEX.LEFT] = ix
        if vertex[INDEX.X] > maxPt[INDEX.X]:
            maxPt[INDEX.X] = vertex[INDEX.X]
            indices[INDEX.RIGHT] = ix
        if vertex[INDEX.Y] < minPt[INDEX.Y]:
            minPt[INDEX.Y] = vertex[INDEX.Y]
            indices[INDEX.BOTTOM] = ix
        if vertex[INDEX.Y] > maxPt[INDEX.Y]:
            maxPt[INDEX.Y] = vertex[INDEX.Y]
            indices[INDEX.TOP] = ix
            
    return indices

def _GetBox( caliperDirs, edgeIndices, vertices ):
    INDEX = INDICES()
    box = [None] * 4
    box[INDEX.LEFT] = IntersectLines( caliperDirs[INDEX.LEFT],
                                      vertices[edgeIndices[INDEX.LEFT]],
                                      caliperDirs[INDEX.BOTTOM],
                                      vertices[edgeIndices[INDEX.TOP]] )
    box[INDEX.BOTTOM] = IntersectLines( caliperDirs[INDEX.LEFT],
                                        vertices[edgeIndices[INDEX.LEFT]],
                                        caliperDirs[INDEX.BOTTOM],
                                        vertices[edgeIndices[INDEX.BOTTOM]] )
    box[INDEX.RIGHT] = IntersectLines( caliperDirs[INDEX.LEFT],
                                       vertices[edgeIndices[INDEX.RIGHT]],
                                       caliperDirs[INDEX.BOTTOM],
                                       vertices[edgeIndices[INDEX.BOTTOM]] )
    box[INDEX.TOP] = IntersectLines( caliperDirs[INDEX.LEFT],
                                     vertices[edgeIndices[INDEX.RIGHT]],
                                     caliperDirs[INDEX.BOTTOM],
                                     vertices[edgeIndices[INDEX.TOP]] )

    area = ( Distance( box[INDEX.LEFT], box[INDEX.BOTTOM] ) *
             Distance( box[INDEX.LEFT], box[INDEX.TOP] ) )

    return box, area
            
def GetOrientedBBox( vertices, edges ):
    minBox = None
    minArea = float('inf')

    edgeIndices = _GetExtremePointIndices( vertices )
    caliperDirs = [ vector( [0, -1] ), vector( [1, 0] ) ]

    for i in range( len( vertices ) ):        
        angles = [ np.dot( caliperDirs[ix % 2], edges[ edgeIndices[ ix ] ] ) ** 2 for ix in range(4) ]
        
        minAngleIx = angles.index( max( angles ) )
        minCaliperIx = minAngleIx % 2

        caliperDirs[minCaliperIx] = edges[ edgeIndices[minAngleIx] ]
        caliperDirs[ ( minCaliperIx + 1 ) % 2 ] = GetOrthogonal( caliperDirs[minCaliperIx] )
        edgeIndices[ minAngleIx ] = ( edgeIndices[minAngleIx] + 1 ) % len(vertices)

        box, area = _GetBox( caliperDirs, edgeIndices, vertices )

##        with open( 'Boxes/Box{}.txt'.format(i), 'w', encoding='utf-8' ) as f:            
##            for j in box:
##                print( '{}, {}'.format( j[0], j[1] ), file = f)
##        print( edgeIndices )
        
        if area < minArea:
            minArea = area
            minBox = box
    
    return minBox
