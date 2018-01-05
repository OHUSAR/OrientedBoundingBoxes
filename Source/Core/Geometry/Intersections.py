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
    segEnd = np.array(segEnd) # TODO
    segStart = np.array(segStart) # TODO

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
    X1, Y1, X2, Y2 = segment1
    X3, Y3, X4, Y4 = segment2

    I1 = [min(X1, X2), max(X1, X2)]
    I2 = [min(X3, X4), max(X3, X4)]

    Ia = [max(min(X1, X2), min(X3, X4)),
          min(max(X1, X2), max(X3, X4))]

    if max(X1, X2) < min(X3, X4):
        return False

    try:
        A1 = (Y1 - Y2) / (X1 - X2)
        A2 = (Y3 - Y4) / (X3 - X4)

        if abs(A1 - A2) < 0.000001:
            return False
    except ZeroDivisionError:
        return False

    b1 = Y1 - A1 * X1
    b2 = Y3 - A2 * X3

    Xa = (b2 - b1) / (A1 - A2)
    Ya = A1 * Xa + b1
    Ya = A2 * Xa + b2

    if ( Xa < max(min(X1, X2), min(X3, X4)) ) or ( Xa > min(max(X1, X2), max(X3, X4)) ):
        return False

    return True
