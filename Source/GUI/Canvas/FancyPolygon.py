POINT_RADIUS = 5

class FancyPolygon:

    def __init__(self, canvas, fill='white', outline='black', width=1):
        self.canvas = canvas
        self.fill = fill
        self.outline = outline
        self.width = width
        
        self.gfxIds = []
        self.canvasIdentifier = None

    def Invalidate(self, vertices, deleteCurrent = False ):
        if deleteCurrent:
            self.canvas.delete( *self.gfxIds )
            
        self.canvasIdentifier = self.canvas.create_polygon( vertices,
                                                            tags = 'token',
                                                            fill = self.fill,
                                                            outline = self.outline,
                                                            width = self.width )
        self.gfxIds.append(self.canvasIdentifier)
        
        for vertex in vertices:
            self.gfxIds.append( self.canvas.create_oval( vertex[0] - POINT_RADIUS,
                                                         vertex[1] - POINT_RADIUS,
                                                         vertex[0] + POINT_RADIUS,
                                                         vertex[1] + POINT_RADIUS,
                                                         fill = self.outline,
                                                         outline = self.outline ) )

        return self.canvasIdentifier

    def Move(self, dx, dy):
        for gfxId in self.gfxIds:
            self.canvas.move( gfxId, dx, dy )
            self.canvas.tag_raise( gfxId )

    def GetCanvasId(self):
        return self.canvasIdentifier
