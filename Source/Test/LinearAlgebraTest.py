import unittest
import random

from Core.BasicDefs import vector
from Core.Utils.LinearAlgebra import *

class OrthogonalTest( unittest.TestCase ):
    def test_zero( self ):
        v = vector( [0, 0] )
        o = GetOrthogonal( v )
        self.assertEqual( list( o ), list( v ) )
    
    def test_basic( self ):
        v = vector( [ 13, 76] )
        o = GetOrthogonal( v )
        self.assertEqual( np.dot( v, o ), 0 )

class NormalizationTest( unittest.TestCase ):
    def test_zero( self ):
        v = vector( [0, 0] )
        n = Normalize( v )
        self.assertEqual( list(n), list(v) )
    def test_basic( self ):
        v = vector( [ 457, 2455 ] )
        self.assertAlmostEqual( np.linalg.norm( Normalize( v ) ), 1 )
    def test_random( self ):
        for i in range( 100 ):
            v = vector( [ random.random(), random.random() ] )
            self.assertAlmostEqual( np.linalg.norm( Normalize( v ) ), 1 )

class PointDistanceTest( unittest.TestCase ):
    def test_same( self ):
        v1 = vector( [ 10, 4354 ] )
        self.assertEqual( Distance( v1, v1 ), 0 )

    def test_basic_x( self ):
        v1 = vector( [ 5, 7 ] )
        v2 = vector( [ 81, 7 ] )
        self.assertEqual( Distance( v1, v2 ), (v2[0] - v1[0])**2 )

    def test_basic_y( self ):
        v1 = vector( [ 18, 134 ] )
        v2 = vector( [ 18, 42 ] )
        self.assertEqual( Distance( v1, v2 ), (v2[1] - v1[1])**2 )
        
        
if __name__ == '__main__':
    unittest.main()
