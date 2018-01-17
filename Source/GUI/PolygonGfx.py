from random import randrange
from GUI.StaticData.Colors import Colors

class PolygonGfx:
    def __init__( self, simPolygon, canvas ):
        self.polygonId = None
        self.convexHullId = None
        self.bvhIds = []

        self.ConstructFrom( simPolygon, canvas )

    def ConstructFrom( self, simPolygon, canvas ):
        polyVertices = [ tuple(v) for v in simPolygon.GetPolygon().GetVertices()]
        polyColor = self.GetRandomColor()
        self.polygonId = canvas.create_polygon( polyVertices, tags="token",
                                                fill = polyColor, outline = polyColor )

 #       chVertices = simPolygon.GetConvexHull().GetVertices()
#        self.convexHullId = self.GetConvexHullGfx( chVertices, canvas )

        bvh = simPolygon.GetBVH()
        for bvI in range( len(bvh) ):
            oobb = bvh[bvI]
            if oobb is not None:
                bvVertices = [ tuple(v) for v in oobb.GetVertices() ]
                bvVertices.append( bvVertices[0] )
                self.bvhIds.append( canvas.create_line( bvVertices, fill = Colors.OOBB,
                                                       tags="oobb", width = 2 ) )
##                self.GetConvexHullGfx( oobb.chVertices, canvas )

    def GetConvexHullGfx( self, ch, canvas ):
        ch = [ tuple(v) for v in ch ]
        ch.append( ch[0] )
        return canvas.create_line( ch, tags="convHull",
                                   fill = Colors.CONVEX_HULL, width = 3 )

    def GetRandomColor(self):
        return Colors.objectPalette[ randrange(len(Colors.objectPalette)) ]

    def Move( self, canvas, dx, dy ):
        canvas.move( self.polygonId, dx, dy )
        if self.convexHullId is not None:
            canvas.move( self.convexHullId, dx, dy )

        for bvhId in self.bvhIds:
            canvas.move( bvhId, dx, dy )

        canvas.tag_raise( self.polygonId )
        if self.convexHullId is not None:
            canvas.tag_raise( self.convexHullId )
        for bvhId in self.bvhIds:
            canvas.tag_raise( bvhId )
        

    def SetBvhColors( self, collisionTree, canvas ):
        for i in range(len(self.bvhIds)):
            if collisionTree[i]:
                canvas.itemconfig( self.bvhIds[i], fill = Colors.OOBB_COLLISION, width = 4 )
            else:
                canvas.itemconfig( self.bvhIds[i], fill = Colors.OOBB, width = 2 )
        
        
