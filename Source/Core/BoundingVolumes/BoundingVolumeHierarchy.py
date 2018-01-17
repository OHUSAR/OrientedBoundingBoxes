from Core.Geometry.Polygon import Polygon
from Core.BoundingVolumes.OOBBHierarchy import GetOOBBHierarchy

class BoundingVolumeHierarchy:

    def __init__( self, vertices, depth, subType = 'oobb' ):
        self.boundingVolumes = self.InitializeFrom( vertices, depth, subType )
        self.depth = depth

    def InitializeFrom( self, vertices, depth, subType ):
        volumes = []
        
        if subType == 'oobb':
            volumes = GetOOBBHierarchy( vertices, depth )
        else:
            raise ValueError( 'Unsuportted bvh sub-type: {}'.format( subType ) )

        return volumes

    def __getitem__( self, ix ):
        return self.boundingVolumes[ix]

    def __len__( self ):
        return len( self.boundingVolumes )

    def GetDepth( self ):
        return self.depth
        
    def Move( self, dx, dy ):
        for bv in self.boundingVolumes:
            bv.Move( dx, dy )
            
