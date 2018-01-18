from Core.BasicDefs import *

from Core.Utils.QuadTree import QuadTree
from Core.Geometry.Polygon import Polygon
from Core.BoundingVolumes.OrientedBoundingBox2 import GetOrientedBBox
from Core.ConvexHull.ConvexHull import GetConvexHull
from Core.Geometry.Slicing import SliceObject, Axis
from Core.Geometry.Utils import GetOrientedEdges

def _GetBox( nonConvexVertices ):
    ch = GetConvexHull( nonConvexVertices )
    #edges = GetOrientedEdges( ch )
    #return GetOrientedBBox( ch, edges ), ch
    return GetOrientedBBox( ch ), ch

def GetOOBBHierarchy( vertices, depth ):
    boxes = QuadTree( depth )
    origGeom = QuadTree( depth )
    
    boxes[0] = Polygon( *_GetBox( vertices ) )
    origGeom[0] = vertices

    if depth > 0:
        queue = [0]
        while len(queue) > 0:
            parentVolumeIx = queue.pop(0)
            parentBox = boxes[ parentVolumeIx ]
            parentVerts = origGeom[ parentVolumeIx ]

            splitAxis1 = Axis( parentBox[3] - parentBox[0],
                               ( parentBox[0] + parentBox[1] ) / 2 )
            splitAxis2 = Axis( parentBox[1] - parentBox[0],
                               ( parentBox[0] + parentBox[3] ) / 2 )

            slice_Ax1_1, slice_Ax1_2 = SliceObject( parentVerts, splitAxis1 )

            slice0, slice1 = SliceObject( slice_Ax1_1, splitAxis2 )
            slice2, slice3 = SliceObject( slice_Ax1_2, splitAxis2 )
            slices = [ slice0, slice1, slice2, slice3 ]

            childVolumes = [ Polygon( *_GetBox( slc ) ) if len(slc) > 2 else None for slc in slices ]
            print( childVolumes )
            for childIx in range(4):
                if childVolumes[childIx] is not None:
                    treeIx = 4 * parentVolumeIx + (childIx+1)
                    boxes[treeIx] = childVolumes[childIx]
                    origGeom[treeIx] = slices[childIx]

                    childOfChildIx = 4 * treeIx + 1
                    if childOfChildIx < len(boxes):
                        queue.append( treeIx )
            

    return boxes
