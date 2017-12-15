from Core.BasicDefs import *

def IntersectLines( dirA, ptA, dirB, ptB ):
    ptA2 = ptA + dirA
    ptB2 = ptB + dirB

    dxA = ptA[0] - ptA2[0]
    dxB = ptB[0] - ptB2[0]
    dyA = ptA[1] - ptA2[1]
    dyB = ptB[1] - ptB2[1]

    det = ( dxA * dyB ) - ( dyA * dxB )
    if ( det != 0 ):
            fctA = ptA[0] * ptA2[1] - ptA[1] * ptA2[0]
            fctB = ptB[0] * ptB2[1] - ptB[1] * ptB2[0]

            return vector( [
                    ( ( fctA * dxB ) - ( dxA * fctB ) ) / det,
                    ( ( fctA * dyB ) - ( dyA * fctB ) ) / det,
            ] )
    return None

def IntersectLineSegment( lineDir, linePt, segStart, segEnd ):
    segDir = segEnd - segStart

    intersectPt = IntersectLines( lineDir, linePt, segDir, segStart )
    if intersectPt is not None:
        if ( ( intersectPt[0] >= min( segStart[0], segEnd[0] ) ) and
             ( intersectPt[0] <= max( segStart[0], segEnd[0] ) ) and
             ( intersectPt[1] >= min( segStart[1], segEnd[1] ) ) and
             ( intersectPt[1] <= max( segStart[1], segEnd[1] ) ) ):
                return intersectPt
    
    return None
