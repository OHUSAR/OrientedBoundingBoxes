from Core.BasicDefs import *

from Core.Utils.QuadTree import QuadTree
from Core.Utils.Logger import LOGGER
from Core.Geometry.Polygon import Polygon
from Core.BoundingVolumes.OrientedBoundingBox2 import GetOrientedBBox
from Core.ConvexHull.JarvisMarch import GetConvexHull
from Core.Geometry.Slicing import SliceObject, Axis

def GetOrientedBoundingBox( vertices ):
    ch = GetConvexHull( vertices )
    return GetOrientedBBox( ch )

def _SliceObject( boundingVolume, originalVertices ):
        splitBox = GetOrientedBBox( boundingVolume.GetVertices() )
        splitAxis1 = Axis( splitBox[3] - splitBox[0],
                           ( splitBox[0] + splitBox[1] ) / 2 )
        splitAxis2 = Axis( splitBox[1] - splitBox[0],
                           ( splitBox[0] + splitBox[3] ) / 2 )

        slice_Ax1_1, slice_Ax1_2 = SliceObject( originalVertices, splitAxis1 )
        slice0, slice1 = SliceObject( slice_Ax1_1, splitAxis2 )
        slice2, slice3 = SliceObject( slice_Ax1_2, splitAxis2 )

        slices = ( slice0, slice1, slice2, slice3 )
        
        LOGGER.log( '--------- Slicing report ----------' )
        LOGGER.log( "Original Object: {}".format( originalVertices ) )
        LOGGER.log( "Axis1: {}".format( splitAxis1 ) )
        LOGGER.log( "Axis2: {}".format( splitAxis2 ) )
        LOGGER.log( '\n'.join( ["Slice{}: {}".format(i, slc) for i,slc in enumerate(slices) ] ) )
        
        return slices


def GetBoundingVolumeHierarchy( vertices, depth, bvFnc ):
    volumes = QuadTree( depth )
    originalGeometry = QuadTree( depth )

    volumes[0] = Polygon( bvFnc( vertices ) )
    originalGeometry[0] = vertices

    queue = [0] if depth else []
    while len(queue):
        parentVolumeIx = queue.pop(0)
        parentVolume = volumes[parentVolumeIx]
        parentVerts = originalGeometry[parentVolumeIx]

        slices = _SliceObject( parentVolume, parentVerts )

        childVolumes = [ Polygon( bvFnc( slc ) ) if len(slc) > 2 else None for slc in slices ]
        for childIx in range(4):
            if childVolumes[childIx] is not None:
                treeIx = 4 * parentVolumeIx + (childIx+1)
                volumes[treeIx] = childVolumes[childIx]
                originalGeometry[treeIx] = slices[childIx]

                childOfChildIx = 4 * treeIx + 1
                if childOfChildIx < len(volumes):
                    queue.append( treeIx )
                    
    return volumes
