from Core.BasicDefs import *

def IntersectLines( dirA, ptA, dirB, ptB ):
    ptA2 = ptA + dirA
    ptB2 = ptB + dirB

    dxA = ptA[0] - ptA2[0]
    dxB = ptB[0] - ptB2[0]
    dyA = ptA[1] - ptA2[1]
    dyB = ptB[1] - ptB2[1]

    det = ( dxA * dyB ) - ( dyA * dxB )
    if det != 0:
            fctA = ptA[0] * ptA2[1] - ptA[1] * ptA2[0]
            fctB = ptB[0] * ptB2[1] - ptB[1] * ptB2[0]

            return vector( [
                    ( ( fctA * dxB ) - ( dxA * fctB ) ) / det,
                    ( ( fctA * dyB ) - ( dyA * fctB ) ) / det,
            ] )
    return None

def IntersectLineSegment( lineDir, linePt, segStart, segEnd ):
    segEnd = np.array(segEnd)
    segStart = np.array(segStart)

    segDir = segEnd - segStart

    intersectPt = IntersectLines( lineDir, linePt, segDir, segStart )
    if intersectPt is not None:
        if ( ( intersectPt[0] >= min( segStart[0], segEnd[0] ) ) and
             ( intersectPt[0] <= max( segStart[0], segEnd[0] ) ) and
             ( intersectPt[1] >= min( segStart[1], segEnd[1] ) ) and
             ( intersectPt[1] <= max( segStart[1], segEnd[1] ) ) ):
                return intersectPt
    
    return None


def IntersectSegments( segment1, segment2 ):    
    seg1Start = np.array( segment1[:2] )
    seg1End = np.array( segment1[2:] )
    seg2Start = np.array( segment2[:2] )
    seg2End = np.array( segment2[2:] )

    seg1Dir = seg1End - seg1Start
    seg2Dir = seg2End - seg2Start

    intersectPt = IntersectLines( seg1Dir, seg1Start, seg2Dir, seg2Start )
    if intersectPt is not None:
        if ( ( intersectPt[0] >= min( seg1Start[0], seg1End[0] ) ) and
             ( intersectPt[0] <= max( seg1Start[0], seg1End[0] ) ) and
             ( intersectPt[0] >= min( seg2Start[0], seg2End[0] ) ) and
             ( intersectPt[0] <= max( seg2Start[0], seg2End[0] ) ) and 
             ( intersectPt[1] >= min( seg1Start[1], seg1End[1] ) ) and
             ( intersectPt[1] <= max( seg1Start[1], seg1End[1] ) ) and
             ( intersectPt[1] >= min( seg2Start[1], seg2End[1] ) ) and
             ( intersectPt[1] <= max( seg1Start[1], seg1End[1] ) ) ):
            return True
        
    return False
