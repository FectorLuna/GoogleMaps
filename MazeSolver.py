import numpy as np
import queue

from MazeNode import MazeNode

class MazeSolver:

    def __init__(self, maze):
        self.maze = maze
        self.dim_y = len(maze)
        self.dim_x = len(maze[0])

        for i in range(len(maze)):
            if (len(maze[i]) != self.dim_x):
                raise Exception("Incorrect maze size, maze must be of size n x m")

    def __shortPathAlghorithm(self, start_x, start_y, stop_x, stop_y):

        explored = self.maze

        # Initiate queue
        q = queue.Queue()

        # Define starting point and point previus node 
        root = MazeNode( [start_x, start_y] )

        # Set root as explored and put on queue
        explored[start_y][start_x] = 1
        q.put(root)

        while ( q.empty() == False ):

            # Get oldest object in queue
            v = q.get()

            # Check if this position is end point
            if ( v.getX() == stop_x and v.getY() == stop_y ):
                return v
            
            # Iterates over all nearby nodes (max 4) and if they are path, places them in queue
            for next_node in self.__getAjacentPaths( v ):

                next_node_x = next_node.getX()
                next_node_y = next_node.getY()

                if ( explored[ next_node_y ][ next_node_x ] != 1 ):
                    explored[next_node_y][next_node_x] = 1
                    q.put(next_node)

        return None
            
        
    def __getAjacentPaths( self, prev_node ):
        edges = []
        x = prev_node.getX()
        y = prev_node.getY() 

        if (x != (self.dim_x - 1)):
            if ( self.maze[y][x+1] == 0):
                
                new_node = MazeNode([x+1, y], prev_node )
                edges.append( new_node )

        if( x != 0 ):
            if ( self.maze[y][x-1] == 0):
                
                new_node = MazeNode([x-1, y], prev_node )
                edges.append( new_node )

        if (y != self.dim_y - 1):
            if ( self.maze[y+1][x] == 0):

                new_node = MazeNode([x, y+1], prev_node )
                edges.append( new_node )

        if (y != 0):
            if ( self.maze[y-1][x] == 0):
                
                new_node = MazeNode([x, y-1], prev_node )
                edges.append( new_node )

        return edges

    def shortestPath(self, start_xy, stop_xy):
        start_x = start_xy[0]
        start_y = start_xy[1]
        stop_x = stop_xy[0]
        stop_y = stop_xy[1]

        if (start_x > self.dim_x or start_y > self.dim_y or stop_x > self.dim_x or stop_y > self.dim_y):
            raise Exception("Starting and stopping point must be within maze")
    
        return self.__shortPathAlghorithm(start_x, start_y, stop_x, stop_y)
    
    def __printMaze(self, maze, solve_maze):

        for i in len(maze):
            print(maze[i] + " " + solve_maze[i])

def __testCase():
    test_maze = [[1, 1, 1, 1, 1],
                [1, 0, 1, 0, 0],
                [1, 0, 0, 0, 1],
                [0, 0, 1, 1, 1],
                [1, 0, 0, 0, 1],
                [1, 1, 1, 1, 1]]

    start_xy = [4, 1]
    stop_xy = [0, 3]

    mz = MazeSolver(test_maze)
    solved = mz.shortestPath(start_xy, stop_xy)

    while(solved.getParent() != None):
        print(str(solved.getX())+" , "+str(solved.getY()))
        solved = solved.getParent()

    print(str(solved.getX())+" , "+str(solved.getY()))
