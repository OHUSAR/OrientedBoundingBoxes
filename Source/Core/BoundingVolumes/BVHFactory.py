from Core.BasicDefs import *

from Core.Utils.QuadTree import QuadTree
from Core.Geometry.Polygon import Polygon
from Core.BoundingVolumes.OrientedBoundingBox2 import GetOrientedBBox
from Core.ConvexHull.ConvexHull import GetConvexHull
from Core.Geometry.Slicing import SliceObject, Axis

def GetOrientedBoundingBox( vertices ):
    ch = GetConvexHull( vertices )
    return GetOrientedBBox( ch )

def _SliceObject( boudingVolume, originalVertices ):
        splitBox = GetOrientedBBox( boudingVolume.GetVertices() )
        splitAxis1 = Axis( splitBox[3] - splitBox[0],
                           ( splitBox[0] + splitBox[1] ) / 2 )
        splitAxis2 = Axis( splitBox[1] - splitBox[0],
                           ( splitBox[0] + splitBox[3] ) / 2 )

        slice_Ax1_1, slice_Ax1_2 = SliceObject( originalVertices, splitAxis1 )
        slice0, slice1 = SliceObject( slice_Ax1_1, splitAxis2 )
        slice2, slice3 = SliceObject( slice_Ax1_2, splitAxis2 )
        return ( slice0, slice1, slice2, slice3 )


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
