import unittest

from Core.BasicDefs import vector
from Core.Geometry.Intersections import *

class LineLineTest( unittest.TestCase ):
    def test_parallel( self ):
        pt1 = vector( [ 1, 5 ] )
        pt2 = vector( [ 10, 2 ] )
        dirV = vector( [ -14, 3 ] )

        self.assertEqual( IntersectLines( dirV, pt1, dirV, pt2 ), None )

    def test_basic( self ):
        pt1 = vector( [ 44, 234 ] )
        pt2 = vector( [ 86, 54 ] )
        dir1 = vector( [ -2, 33 ] )
        dir2 = vector( [ 76, 1 ] )

        self.assertEqual( type(IntersectLines( dir1, pt1, dir2, pt2 )), type( vector([]) ) )
        
class SegmentSegmentTest( unittest.TestCase ):
    def test_no_intersect( self ):
        seg1 = [ 3, 5, -3.34, 1.42 ]
        seg2 = [ 3.7, 0.12, 0.26, 2.88 ]
        self.assertEqual( IntersectSegments( seg1, seg2 ), False )

    def test_intersect( self ):
        seg1 = [ 4.42, 4.42, -2.36, -2 ]
        seg2 = [ 5.46, 1.48, 2.74, 5.24 ]
        self.assertEqual( IntersectSegments( seg1, seg2 ), True )
