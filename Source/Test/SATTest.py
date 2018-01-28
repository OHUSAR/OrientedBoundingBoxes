import unittest

from Core.BasicDefs import *
from Core.Geometry.Utils import GetOrientedEdges, GetEdgeNormals
from Core.Collisions.CollisionDetector import CollisionObject, ObjectsCollide

class SATTest( unittest.TestCase ):
    def GetCollisionObject( self, verts ):
        normals = GetEdgeNormals( GetOrientedEdges( verts ) )
        return CollisionObject( verts, normals )

    def NonCollides( self, verts1, verts2 ):
        colO1 = self.GetCollisionObject( verts1 )
        colO2 = self.GetCollisionObject( verts2 )

        self.assertFalse( ObjectsCollide( colO1, colO2 ) )

    def Collides( self, verts1, verts2 ):
        colO1 = self.GetCollisionObject( verts1 )
        colO2 = self.GetCollisionObject( verts2 )

        self.assertTrue( ObjectsCollide( colO1, colO2 ) )

    def test_non_col_1( self ):
        verts1 = [ vector([0.78, 0.97]), vector([ -0.43, 2.25]), vector([-1.96,2.32]), vector([-2.37, 0.66]), vector([-1,0]) ]
        verts2 = [ vector([0.64,1.66]), vector([1.82, 0.21]), vector([2,3]) ]
        self.NonCollides( verts1, verts2 )

    def test_non_col_2( self ):
        verts1 = [ vector([3,1]), vector([3,2]), vector([1,2]), vector([0,1]), vector([2,0]) ]
        verts2 = [ vector([-1,0]), vector([-3,1]), vector([-2,3]) ]
        self.NonCollides( verts1, verts2 )

    def test_intersect( self ):
        verts1 = [ vector([3,1]), vector([3,2]), vector([1,2]), vector([0,1]), vector([2,0]) ]
        verts2 = [ vector([1,0]), vector([-1,1]), vector([0,3]) ]
        self.Collides( verts2, verts1 )

    def test_intersect_no_verts( self ):
        verts1 = [ vector([1,1]), vector([1,2]), vector([-1,2]), vector([-2,1]), vector([0,0]) ]
        verts2 = [ vector([1,0]), vector([-1.98,0.42]), vector([0,3]) ]
        self.Collides( verts1, verts2 )

    def test_contains( self ):
        verts1 = [ vector([2,2]), vector([0,3]), vector([-2,1]), vector([1,0]) ]
        verts2 = [ vector([0.19, 2.26]), vector([-0.84, 1.87]), vector([-0.82, 1.02]), vector([0.05, 0.62]), vector([0.93, 1.16]), vector([1,2]) ]
        self.Collides( verts1, verts2 )
    

        
        

    
    
