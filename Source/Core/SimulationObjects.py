from Core.Utils.QuadTree import QuadTree
from Core.Geometry.Polygon import Polygon
from Core.ConvexHull.ConvexHull import GetConvexHull
from Core.BoundingVolumes.BoundingVolumeHierarchy import BoundingVolumeHierarchy
from Core.Collisions.CollisionDetector import CollisionObject, ObjectsCollide

class SimulationPolygon:
    
    def __init__( self, vertices, bvhDepth = 1, bvhType = 'oobb' ):
        self.originalPolygon = Polygon( vertices )
        self.convexHull = Polygon( GetConvexHull( vertices ) )
        self.bvh = BoundingVolumeHierarchy( vertices, bvhDepth, bvhType )

    def Move( self, dx, dy ):
        self.originalPolygon.Move( dx, dy )
        self.convexHull.Move( dx, dy )
        self.bvh.Move( dx, dy )

    def GetPolygon(self):
        return self.originalPolygon

    def GetConvexHull(self):
        return self.convexHull

    def GetBVH(self):
        return self.bvh

    def GetCollisions( self, other ):
        colTree1 = QuadTree( self.bvh.GetDepth(), initialValue = False )
        colTree2 = QuadTree( other.bvh.GetDepth(), initialValue = False )

        for bv1Ix in range(len(self.bvh)):
            boundingVolume1 = self.bvh[bv1Ix]
            if boundingVolume1 is not None:
                for bv2Ix in range(len(other.bvh)):
                    boundingVolume2 = other.bvh[bv2Ix]
                    if boundingVolume2 is not None and self.Collides( boundingVolume1, boundingVolume2 ):
                        colTree1[bv1Ix] = True
                        colTree2[bv2Ix] = True
                    
        return [colTree1, colTree2]

    def Collides( self, bv1, bv2 ):
        colObj1 = CollisionObject( bv1.GetVertices(), bv1.GetEdgeNormals() )
        colObj2 = CollisionObject( bv2.GetVertices(), bv2.GetEdgeNormals() )
        return ObjectsCollide( colObj1, colObj2 )        
