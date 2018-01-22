from Core.BasicDefs import *


def GetOrthogonal( vector2d ):
    return vector( [ vector2d[1], -vector2d[0] ] )

def Distance( vertex1, vertex2 ):
    d = vertex2 - vertex1
    return d[0] * d[0] + d[1] * d[1]

def Normalize( vct ):
    norm = np.linalg.norm( vct )
    if norm == 0:
        return vct
    return vct / norm

    
