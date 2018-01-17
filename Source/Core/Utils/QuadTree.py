class QuadTree:

    def __init__(self, maxDepth, initialValue = None):
        self.capacity = ( 4**(maxDepth+1) - 1 ) // 3
        self.nodes = [initialValue]* self.capacity

    def __len__( self ):
        return self.capacity

    def __getitem__(self, ix):
        return self.nodes[ix]

    def __setitem__(self, ix, obj):
        self.nodes[ix] = obj

    def Get( self, level, ix ):
        return self.nodes[ 4*level + ix ]

    def GetParent( self, ix ):
        return self.nodes[ (ix-1)//4 ]

    def GetChild( self, ix, childIx ):
        return self.nodes[ (4*ix) + childIx ]
