from random import randrange

from Core.Utils.QuadTree import QuadTree

from GUI.StaticData.Colors import Colors

class PolygonGfx:
    def __init__( self, simPolygon, canvas ):
        self.polygonId = None
        self.bvhIds = None

        self.polyColor = self.GetRandomColor()
        self.Invalidate( simPolygon, canvas )

    def Invalidate( self, simPolygon, canvas, deleteCurrent = False ):
        if deleteCurrent:
            canvas.delete( *[self.polygonId] + self.bvhIds.nodes )
        
        polyVertices = [ tuple(v) for v in simPolygon.GetPolygon().GetVertices()]

        self.polygonId = canvas.create_polygon( polyVertices, tags="token",
                                                fill = self.polyColor,
                                                outline = self.polyColor )

        bvh = simPolygon.GetBVH()
        self.bvhIds = QuadTree( bvh.GetDepth(), -1 )
        for bvI in range( len( bvh ) ):
            boundVolume = bvh[bvI]
            if boundVolume is not None:
                bvVertices = [ tuple(v) for v in boundVolume.GetVertices() ]
                bvVertices.append( bvVertices[0] )
                self.bvhIds[bvI] = canvas.create_line( bvVertices, fill = Colors.OOBB,
                                                       tags="oobb", width = 2 )

    def GetRandomColor(self):
        return Colors.objectPalette[ randrange(len(Colors.objectPalette)) ]

    def Move( self, canvas, dx, dy ):
        canvas.move( self.polygonId, dx, dy )
        for bvhId in self.bvhIds:
            if bvhId > 0:
                canvas.move( bvhId, dx, dy )

        canvas.tag_raise( self.polygonId )
        for bvhId in self.bvhIds:
            if bvhId > 0:
                canvas.tag_raise( bvhId )
        
    def SetBvhColors( self, collisionTree, canvas, hideNonColliding ):
        for i in range( len(collisionTree) ):
            gfxId = self.bvhIds[i]

            if gfxId > 0:
                color = Colors.OOBB
                lineWidth = 2
                gfxState = "hidden" if hideNonColliding else "normal"
                
                if collisionTree[i]:
                    lineWidth = 4
                    color = Colors.OOBB_COLLISION
                    gfxState = "normal"

                for childI in range(4):
                    if collisionTree.GetChild( i, childI ):
                        lineWidth = 2
                        color = Colors.OOBB_COLLISION_PARENT
                        break
                 
                canvas.itemconfig( gfxId, fill = color, width = lineWidth, state = gfxState )
        
        
