from PIL import Image

import skimage as ski
import numpy as np
import os
import matplotlib.pyplot as plt

from MazeSolver import MazeSolver

class ImageConverter:

    def __init__(self):
        pass


    def __treatContrast( self, image ):

        if (len(image[0][0]) == 4):
            image = ski.color.rgba2rgb(image)
            image = ski.color.rgb2gray(image)

        else:
            image = ski.color.rgb2gray(image)

        mask = image > 0.98
        image[mask] = 0

        mask = image < 0.94
        image[mask] = 0

        return image

    def __transformToRoadMatrix( self, image , scale):

        downscale_size = scale

        dim = image.shape
        new_x_dim = (int) (image.shape[1]/downscale_size)
        new_y_dim = (int) (image.shape[0]/downscale_size)
        
        new_image_rows = 0
        new_image_cols = 0
        new_image = []

        for col_old in range(new_y_dim):
            new_image.append([])
            for row_old in range(new_x_dim):

                median = 0
                nbr_of_sums = 0

                for median_x in range(col_old*downscale_size, (col_old+1)*downscale_size):
                    for median_y in range(row_old*downscale_size, (row_old+1)*downscale_size):
                        median += image[median_x][median_y]
                        nbr_of_sums += 1

                median /= nbr_of_sums
                
                if (median < 0.28):
                    median = 0
                else:
                    median = 1

                new_image[col_old].append(median)
                        
        return new_image

    def __findShortestPath( self, image, start_xy, stop_xy, scale ):

        mazeToSolve = image
        #mazeToSolve = np.transpose(image)

        mazeSolver = MazeSolver(mazeToSolve)

        start_xy = [ int(start_xy[0] / scale) , int(start_xy[1] / scale)]
        stop_xy = [ int(stop_xy[0] / scale) , int(stop_xy[1] / scale)]

        path = np.zeros(len(mazeToSolve[0]))
        path = np.tile(path, (len(mazeToSolve), 1 ))
        path[ start_xy[1] ][ start_xy[0] ] = 1

        solution = mazeSolver.shortestPath(start_xy, stop_xy)

        if (solution == None):
            print("Error: Starting or stopping point is not valid")
            return None
        
        return solution
        """
        while(solution.getParent() != None):

            path[ solution.getY() ][ solution.getX() ] = 1
            solution = solution.getParent()

        return path
        """
        
    def __pathToPlot( self, node , startXY):

        x, y = [], []

        if ( node == None): 
            raise Exception("No valid path found")

        while( node.getParent() != None ):

            # Entire set of if-statements are placed to smooth out the path by changing its coordinate to better accomodate to nearby paths
            if ( node.getParent().getParent() != None and len(x) >= 2 ):

                approx_x = (node.getX() + node.getParent().getX() + node.getParent().getParent().getX() + x[len(x)-1] + x[len(x)-2]) / 5
                approx_y = (node.getY() + node.getParent().getY() + node.getParent().getParent().getY() + y[len(y)-1] + y[len(y)-2]) / 5

            elif ( node.getParent().getParent() != None and len(x) >= 1 ):

                approx_x = (node.getX() + node.getParent().getX() + node.getParent().getParent().getX() + x[len(x)-1] ) / 4
                approx_y = (node.getY() + node.getParent().getY() + node.getParent().getParent().getY() + y[len(y)-1] ) / 4

            elif ( node.getParent().getParent() != None ):

                approx_x = (node.getX() + node.getParent().getX() + node.getParent().getParent().getX() ) / 3
                approx_y = (node.getY() + node.getParent().getY() + node.getParent().getParent().getY() ) / 3

            elif ( node.getParent() != None and len(x) >= 2 ):

                approx_x = (node.getX() + node.getParent().getX() + x[len(x)-1] + x[len(x)-2]) / 4
                approx_y = (node.getY() + node.getParent().getY() + y[len(y)-1] + y[len(y)-2]) / 4

            else:
                approx_x = node.getX()
                approx_y = node.getY()

            x.append( approx_x )
            y.append( approx_y )
            node = node.getParent()

            

        x.append(startXY[0])
        y.append(startXY[1])

        newX = x[::-1]
        newY = y[::-1]

        return newX, newY

    def __rescalePath( self, pathX, pathY, scale ):
        new_pathX = []
        new_pathY = []

        for i in range(len(pathX)):
            new_pathX.append( int(scale * pathX[i]))
            new_pathY.append( int(scale * pathY[i]))
        
        return new_pathX, new_pathY
            
    # Main function, used by other files to path a google maps picture from point a to point b

    def findShortestPathOfImage(self, imagePath, startxy, stopxy, scale ):

        navigPicture = ski.io.imread(imagePath)

        navigPicture = self.__treatContrast(navigPicture)
        navigPicture = self.__transformToRoadMatrix(navigPicture, scale)

        path_find = np.copy(navigPicture)

        shortest_path = self.__findShortestPath(path_find, startxy, stopxy, scale)

        path_x, path_y = self.__pathToPlot( shortest_path, startxy )
        path_x, path_y = self.__rescalePath( path_x, path_y, scale)

        path_x[0] = int( path_x[0] / scale )
        path_y[0] = int( path_y[0] / scale )

        return path_x, path_y

    def testCase(self):
        

        filename = os.path.join(ski.data_dir, "NavigationTest.png")

        orgPicture = ski.io.imread(filename)
        navPicture = ski.io.imread(filename)

        scale = 10
        navPicture = self.__treatContrast(navPicture)
        navPicture = self.__transformToRoadMatrix(navPicture, scale)
        """
        test_maze = [[1, 1, 1, 1, 1],
                    [1, 0, 1, 0, 0],
                    [1, 0, 0, 0, 1],
                    [0, 0, 1, 1, 1],
                    [1, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1]]

        start, stop = [0, 3], [4, 1]

        shortestPath = findShortestPath(test_maze, start, stop)
        path_x, path_y = pathToPlot( shortestPath, start )
        """

        path_find = np.copy(navPicture)
        shortest_path = self.__findShortestPath(path_find, [15, 58], [101, 14])

        path_x, path_y = self.__pathToPlot( shortest_path, [15, 58] )
        path_x, path_y = self.__rescalePath( path_x, path_y, scale)

        # BIG TEST CASE
        #TEST_PICTURE = treatContrast(orgPicture)
        #TEST_PICTURE = transformToRoadMatrix(TEST_PICTURE, 1)
        #TEST_PICTURE = tightenPath(TEST_PICTURE)
        #navPicture = tightenPath(navPicture)

        imgplot = plt.imshow(orgPicture)
        plt.plot(path_x, path_y, color="r")
        plt.show()

