from collections import deque


def _IsLeftTurn( a, b, c ):
    return ( ( ( b[0] - a[0] ) * ( c[1] - a[1] ) ) -
             ( ( c[0] - a[0] ) * ( b[1] - a[1] ) ) 
	    ) > 0

def GetConvexHull( vertices ):
    if len(vertices) < 3:
        raise ValueError # TODO

    convexHull = deque()

    if _IsLeftTurn( vertices[0], vertices[1], vertices[2] ):
        convexHull.append( vertices[0] )
        convexHull.append( vertices[1] )
    else:
        convexHull.append( vertices[1] )
        convexHull.append( vertices[0] )
    convexHull.append( vertices[2] )
    convexHull.appendleft( vertices[2] )

    for i in range( 3, len(vertices) ):
        currentVertex = vertices[i]
        
        if ( not _IsLeftTurn( convexHull[0], convexHull[1], currentVertex ) or
             not _IsLeftTurn( convexHull[-2], convexHull[-1], currentVertex ) ):
            while not _IsLeftTurn( convexHull[0], convexHull[1], currentVertex ):
                convexHull.popleft()
            convexHull.appendleft( currentVertex )

            while not _IsLeftTurn( convexHull[-2], convexHull[-1], currentVertex ):
                convexHull.pop()
            convexHull.append( currentVertex )
            
    return list( convexHull )[:-1]
