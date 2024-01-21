class MazeNode:

    def __init__( self , posXY, prev_node = None):
        self.posXY = posXY          # Stored as [x, y]
        self.prev_node = prev_node

    def setPrevNode( self, prev_node ):
        self.prev_node = prev_node

    def getParent( self ):
        
        return self.prev_node
    
    def getX( self ):

        return self.posXY[0]
    
    def getY( self ):

        return self.posXY[1]
    
    