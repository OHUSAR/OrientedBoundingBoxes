from Core.BasicDefs import *
from Core.Geometry.Utils import *
from Core.ConvexHull.ConvexHull import *
from Core.BoundingBox.OrientedBoundingBox import *
from Core.Collisions.CollisionDetector import *

vertices = [
    vector( [  65.9091033935547,	-37.7272720336914	] ),
    vector( [  105.909103393555,	12.27272605896		] ),
    vector( [  -4.09089660644531,	42.2727279663086	] ),
    vector( [  65.9091033935547,	52.2727279663086	] ),
    vector( [  5.90910339355469,	72.2727279663086	] ),
    vector( [  -44.0908966064453,	62.2727279663086	] ),
    vector( [  -74.0908966064453,	2.27272605895996	] ),
    vector( [  -34.0908966064453,	32.2727279663086	] ),
    vector( [  -34.0908966064453,	52.2727279663086	] ),
    vector( [  -14.0908966064453,	42.2727279663086	] ),
    vector( [  -24.0908966064453,	-7.72727394104004	] ),
    vector( [  -84.0908966064453,	-17.72727394104	] ),
    vector( [  -64.0908966064453,	-47.7272720336914	] ),
    vector( [  -14.0908966064453,	-27.72727394104	] ),
    vector( [  15.9091033935547,	22.27272605896		] ),
    vector( [  25.9091033935547,	2.27272605895996	] ),
    vector( [  -4.09089660644531,	-37.7272720336914	] ),
    vector( [  5.90910339355469,	-7.72727394104004	] ),
    vector( [  -24.0908966064453,	-47.7272720336914	] ),
    vector( [  15.9091033935547,	-67.7272720336914	] ),
    vector( [  55.9091033935547,	-27.72727394104	] ),
    vector( [  55.9091033935547,	-67.7272720336914	] )
    ]

ch = GetConvexHull( vertices )
edges = GetOrientedEdges( ch )

oobb = GetOrientedBBox( ch, edges )

for i in vertices:
    print( '{}, {}'.format( i[0], i[1] ) )

print( 'ConvexHull')
for i in ch:
    print( '{}, {}'.format( i[0], i[1] ) )

print( 'OOBB')
for i in oobb:
    print( '{}, {}'.format( i[0], i[1] ) )


colVA = [
        vector( [ 1,1 ] ),
        vector( [ 2,2 ] ),
        vector( [ 3,1 ] ),
        vector( [ 4,2.5 ] ),
]
colVB = [
##        vector( [ -1, -1 ] ),
##        vector( [ -2, 2 ] ),
##        vector( [ -3, -1 ] ),
##        vector( [ -5, 3 ] ),

         vector( [ 5, 2 ] ),
         vector( [ 0, 1 ] ),
         vector( [ -1, 2 ] ),
         vector( [ 3, 3 ] ),
]

colEA = GetOrientedEdges( colVA )
colEB = GetOrientedEdges( colVB )
normalsA = GetEdgeNormals( colEA )
normalsB = GetEdgeNormals( colEB )

colObjA = CollisionObject( colVA, normalsA )
colObjB = CollisionObject( colVB, normalsB )

print( ObjectsCollide( colObjA, colObjB ) )

