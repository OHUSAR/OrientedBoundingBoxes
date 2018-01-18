from Core.Utils.LinearAlgebra import *


def GetOrientedEdges( vertices ):
    edges = [None]*len(vertices)
    for i in range( len(vertices) - 1 ):
        edges[i] = Normalize( vertices[i+1] - vertices[i] )

    edges[-1] = Normalize( vertices[0] - vertices[-1] )
    return edges

def GetEdgeNormals( edges ):
    normals = [None]*len(edges)
    for ix, edge in enumerate(edges):
        normals[ix] = GetOrthogonal( edge )
    return normals
