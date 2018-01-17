from Core.Utils.QuadTree import QuadTree

class PolygonManipulator:
    def __init__(self, polygonStorage, canvas ):
        self.polygons = polygonStorage
        self.canvas = canvas

        self._drag_data = {"x": 0, "y": 0, "item": None}

    def OnDragStart( self, x, y ):
        polygonId = self.canvas.find_closest( x, y )[0]

        self._drag_data["item"] = self.polygons.get( polygonId )
        self._drag_data["x"] = x
        self._drag_data["y"] = y

    def OnDragEnd( self ):
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def OnDrag( self, x, y ):
        deltaX = x - self._drag_data["x"]
        deltaY = y - self._drag_data["y"]

        storageEntry = self._drag_data["item"]
        storageEntry.polygon.Move( deltaX, deltaY )
        storageEntry.polygonGfx.Move( self.canvas, deltaX, deltaY )

        self.CheckCollisions()

        self._drag_data["x"] = x
        self._drag_data["y"] = y


    def CheckCollisions( self ):
        collisionTrees = self.InitCollisionTrees()

        for obj1Ix in range( len(self.polygons) ):
            for obj2Ix in range( obj1Ix+1, len(self.polygons) ):
                obj1 = self.polygons.get( obj1Ix, True ).polygon
                obj2 = self.polygons.get( obj2Ix, True ).polygon
                
                colTree1, colTree2 = obj1.GetCollisions( obj2 )

                self.MergeTrees( collisionTrees, (obj1Ix, colTree1), (obj2Ix, colTree2) )

        self.ColorCollisions( collisionTrees )

    def InitCollisionTrees( self ):
        return [ QuadTree( self.polygons.get(i, True).polygon.GetBVH().GetDepth() ) for i in range( len(self.polygons) ) ]
     
    def MergeTrees( self, colTrees, tree1, tree2 ):
        tree1Ix, tree1 = tree1
        tree2Ix, tree2 = tree2

        for i in range(len(tree1)):
            colTrees[tree1Ix][i] = colTrees[tree1Ix][i] or tree1[i]
        for i in range(len(tree2)):
            colTrees[tree2Ix][i] = colTrees[tree2Ix][i] or tree2[i]

    def ColorCollisions( self, colTrees ):
        for objectI in range(len(self.polygons)):
            polyGfx = self.polygons.get(objectI, True).polygonGfx
            polyGfx.SetBvhColors( colTrees[objectI], self.canvas )

            
