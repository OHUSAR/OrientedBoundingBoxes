from Core.BasicDefs import *


def GetOrthogonal( vector2d ):
    return vector( [ vector2d[1], -vector2d[0] ] )

def Distance( vertex1, vertex2 ):
    return np.linalg.norm( vertex1 - vertex2 )

def Normalize( vct ):
    norm = np.linalg.norm( vct )
    if norm == 0:
        return vct
    return vct / norm

    
