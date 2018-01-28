import unittest

from Core.BasicDefs import *
from Core.Geometry.Slicing import Axis, SliceObject


class SliceTest( unittest.TestCase ):
    def vectorEqual( self, a, b, msg = None ):
        if (a == b).all():
            return True
        raise self.failureException( "{} != {}".format( a, b ) )
    
    def setUp( self ):
        self.addTypeEqualityFunc( type(vector([])), self.vectorEqual )
    
    def test_slice1( self ):
        verts = [ vector([4,5]), vector([-2,4]), vector([-4,-2]),
                  vector([1,0]), vector([6,1]) ]
        ax = Axis( vector([2,6]) - vector([3,-2]), vector([2,6]) )

        slice1Expected = [vector([4, 5]), vector([2.16, 4.69]), vector([2.71, 0.34]), vector([6, 1])]
        slice2Expected = [vector([2.16, 4.69]), vector([-2,  4]), vector([-4, -2]), vector([1, 0]), vector([2.71, 0.34])]


        slice1, slice2 = SliceObject( verts, ax )
        
        self.assertEqual( len(slice1), len(slice1Expected) )
        self.assertEqual( len(slice2), len(slice2Expected) )
        
        for i in range(len(slice1)):
            self.assertEqual( np.round(slice1[i], 2 ), slice1Expected[i] )
            
        for i in range(len(slice2)):
            self.assertEqual( np.round(slice2[i], 2 ), slice2Expected[i] )

    def test_slice2( self ):
        verts = [ vector([4,5]), vector([-2,4]), vector([-4,-2]),
                  vector([1,0]), vector([6,1]) ]
        ax = Axis( vector([6.8, 1.48]) - vector([4.74, -1.46]), vector([6.8, 1.48]) )

        slice1, slice2 = SliceObject( verts, ax )
        self.assertEqual( len(slice1), 0 )
        self.assertEqual( len(slice2), len(verts) )

        for i in range( len(verts) ):
            self.assertEqual( slice2[i], verts[i] )
        
            
