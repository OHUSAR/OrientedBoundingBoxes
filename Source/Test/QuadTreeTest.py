import unittest

from Core.Utils.QuadTree import QuadTree

class QuadTreeTestDepth0( unittest.TestCase ):
    @classmethod
    def setUpClass(cls):
        cls.tree = QuadTree( 0 )
    
    def test_0_len( self ):
        self.assertEqual( len(self.tree), 1 )

    def test_1_defaultValue( self ):
        self.assertEqual( self.tree[0], None )

    def test_2_assign( self ):
        self.tree[0] = 'string'
        self.assertEqual( self.tree[0], 'string' )

    def test_3_child( self ):
        rootIx = 0
        for i in range(4):
            self.assertEqual( self.tree.GetChild( rootIx, i ), None )

    def test_4_parent( self ):
        self.assertEqual( self.tree.GetParent( 0 ), None )

class QuadTreeTest( unittest.TestCase ):
    @classmethod
    def setUpClass(cls):
        cls.defaultVal = 52
        cls.tree = QuadTree( 2, cls.defaultVal )

    def test_0_len( self ):
        self.assertEqual( len(self.tree), 21 )

    def test_1_defaultValue( self ):
        for node in self.tree:
            self.assertEqual( node, self.defaultVal )

    def test_2_assign( self ):
        self.tree[1] = 98
        self.assertEqual( self.tree[1], 98 )

    def test_3_child( self ):
        nodeIx = 1
        for i in range(4):
            self.assertEqual( self.tree.GetChild( nodeIx, i ), self.defaultVal )

    def test_4_parent( self ):
        self.assertEqual( self.tree.GetParent( 1 ), self.defaultVal )
