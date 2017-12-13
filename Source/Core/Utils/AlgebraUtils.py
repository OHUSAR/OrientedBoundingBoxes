from Core.BasicDefs import *

def GetOrthogonal( vector2d ):
    return vector( [ vector2d[1], -vector2d[0] ] )

def Distance( vertex1, vertex2 ):
    return np.linalg.norm( vertex1 - vertex2 )

def IntersectLines( dirA, ptA, dirB, ptB ):
    ptA2 = ptA + dirA
    ptB2 = ptB + dirB

    dxA = ptA[0] - ptA2[0];
    dxB = ptB[0] - ptB2[0];
    dyA = ptA[1] - ptA2[1];
    dyB = ptB[1] - ptB2[1];

    det = ( dxA ) * ( dyB ) - ( dyA ) * ( dxB );
    if ( det != 0 ):
            fctA = ptA[0] * ptA2[1] - ptA[1] * ptA2[0];
            fctB = ptB[0] * ptB2[1] - ptB[1] * ptB2[0];

            return vector( [
                    ( ( fctA ) * ( dxB ) - ( dxA ) * ( fctB ) ) / det,
                    ( ( fctA ) * ( dyB ) - ( dyA ) * ( fctB ) ) / det,
            ] );
    raise ValueError # TODO

def Normalize( vct ):
    norm = np.linalg.norm( vct )
    if norm == 0:
        return vct
    return vct / norm

    
