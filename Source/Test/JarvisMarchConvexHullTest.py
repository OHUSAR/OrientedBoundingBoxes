import unittest

from Core.BasicDefs import *
from Core.ConvexHull.JarvisMarch import GetConvexHull

class JarvisCHTest( unittest.TestCase ):
    def vectorEqual( self, a, b, msg = None ):
        if (a == b).all():
            return True
        raise self.failureException( "{} != {}".format( a, b ) )
    
    def setUp( self ):
        self.addTypeEqualityFunc( type(vector([])), self.vectorEqual )

    def compareHulls( self, verts, chExpected ):
        chActual = GetConvexHull( verts )

        self.assertEqual( len(chActual), len(chExpected) )
        for i in range( len(chActual) ):
            self.assertEqual( chActual[i], chExpected[i] )
    
    def test_simple( self ):
        verts = [ vector([4,5]), vector([-2,4]), vector([-4,-2]),
                  vector([1,0]), vector([6,1]) ]

        chExpected = [ vector([-4,-2]), vector([6,1]), vector([4,5]), vector([-2,4])]
        self.compareHulls( verts, chExpected )

    def test_hull_complex( self ):
        verts = [vector([ 65.90910339, -37.72727203]), vector([105.90910339,  12.27272606]), vector([-4.09089661, 42.27272797]), vector([65.90910339, 52.27272797]), vector([ 5.90910339, 72.27272797]), vector([-44.09089661,  62.27272797]), vector([-74.09089661,   2.27272606]), vector([-34.09089661,  32.27272797]), vector([-34.09089661,  52.27272797]), vector([-14.09089661,  42.27272797]), vector([-24.09089661,  -7.72727394]), vector([-84.09089661, -17.72727394]), vector([-64.09089661, -47.72727203]), vector([-14.09089661, -27.72727394]), vector([15.90910339, 22.27272606]), vector([25.90910339,  2.27272606]), vector([ -4.09089661, -37.72727203]), vector([ 5.90910339, -7.72727394]), vector([-24.09089661, -47.72727203]), vector([ 15.90910339, -67.72727203]), vector([ 55.90910339, -27.72727394]), vector([ 55.90910339, -67.72727203])]
                
        chExpected = [vector([-84.09089661, -17.72727394]), vector([-64.09089661, -47.72727203]), vector([ 15.90910339, -67.72727203]), vector([ 55.90910339, -67.72727203]), vector([105.90910339,  12.27272606]), vector([65.90910339, 52.27272797]), vector([ 5.90910339, 72.27272797]), vector([-44.09089661,  62.27272797])]
        self.compareHulls( verts, chExpected )

    def test_self_intersecting( self ):
        verts = [ vector([20,-5]), vector([14.15, -6.96]), vector([13.55, -1.64]), vector([19.76, -9.01]), vector([17.83, -1.1]), vector([9.5, -6.23]), vector([16.56, -10.46]) ]
        chExpected = [ vector([9.5, -6.23]), vector([16.56, -10.46]), vector([19.76, -9.01]), vector([20,-5]), vector([17.83, -1.1]), vector([13.55, -1.64]) ]
        self.compareHulls( verts, chExpected )
                      
    def test_error_empty( self ):
        verts = []
        self.assertRaises( ValueError, GetConvexHull, verts )

    def test_error_fewVerts( self ):
        verts = [vector([1,2])]
        self.assertRaises( ValueError, GetConvexHull, verts )
        verts.append( vector([3,4]) )
        self.assertRaises( ValueError, GetConvexHull, verts )

