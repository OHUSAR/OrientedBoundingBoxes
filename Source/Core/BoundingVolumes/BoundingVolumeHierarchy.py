from Core.Geometry.Polygon import Polygon
import Core.BoundingVolumes.BVHFactory as BVHFactory
from Core.Utils.Logger import LOGGER


class BoundingVolumeHierarchy:

    def __init__( self, vertices, depth, subType = 'oobb' ):
        self.boundingVolumes = self.InitializeFrom( vertices, depth, subType )

        LOGGER.log( str( [ False if n is None else True for n in self.boundingVolumes ] ) )
        
        self.depth = depth

    def InitializeFrom( self, vertices, depth, subType ):
        volumeGenerator = None
        if subType == 'oobb':
            volumeGenerator = BVHFactory.GetOrientedBoundingBox
        elif subType == 'convHull':
            volumeGenerator = BVHFactory.GetConvexHull
        else:
            raise ValueError( 'Unsuportted bvh sub-type: {}'.format( subType ) )

        return BVHFactory.GetBoundingVolumeHierarchy( vertices, depth, volumeGenerator )

    def __getitem__( self, ix ):
        return self.boundingVolumes[ix]

    def __len__( self ):
        return len( self.boundingVolumes )

    def GetDepth( self ):
        return self.depth
        
    def Move( self, dx, dy ):
        for bv in self.boundingVolumes:
            if bv is not None:
                bv.Move( dx, dy )
            
