
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFileDialog
from PyQt5.QtGui import * #QPalette, QColor, QPixmap, QValidator


from ImageConverter import ImageConverter
import numpy as np
import sys

imageScale = 1

class MainWindow( QMainWindow ):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.displayedPicture = None
        self.displayedPicturePath = None
        self.windowWidth = 1200
        self.windowHeight = 800
        self.downsizeScale = 1
        self.mouseX, self.mouseY = -1 , -1
        self.startXY = [0, 0]
        self.stopXY = [0, 0]

        self.setMouseTracking(True)
        self.setGeometry(200, 200, self.windowWidth, self.windowHeight)
        self.setWindowTitle("Pathfinding")

        self.initUI()

    # Defines main layout and UI for the window
    def initUI(self):

        # Defines all buttons and windows viewed in the UI

        self.instructions = QtWidgets.QLabel(self)
        self.instructions.setText("Upload a picture from Google Maps")
        self.instructions.setFont(QtGui.QFont('Arial', 12))
        self.instructions.setAlignment(QtCore.Qt.AlignCenter)

        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.mousePressEvent = self.registerMousePos

        self.uploadButton = QtWidgets.QPushButton(self)
        self.uploadButton.setText("Upload image")
        self.uploadButton.clicked.connect(self.upload)

        self.findPathButton = QtWidgets.QPushButton(self)
        self.findPathButton.setText("Find path")
        self.findPathButton.clicked.connect(self.findPath)

        self.scaleBox = QtWidgets.QLineEdit(self)
        self.scaleBox.setPlaceholderText("Downsize scale")
        self.scaleBox.setValidator(QIntValidator(1, 99, self))
        self.scaleBox.setFixedWidth(150)


        # Defines the layout and places widgets correctly

        mainLayout = QVBoxLayout()
        secondLayout = QHBoxLayout()

        mainLayout.addWidget(self.instructions)
        mainLayout.addWidget(self.label)
        secondLayout.addWidget(self.uploadButton)
        secondLayout.addWidget(self.findPathButton)
        secondLayout.addWidget(self.scaleBox)
        mainLayout.addLayout(secondLayout)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.mainLayout = mainLayout
        self.setCentralWidget(widget)

    def upload(self):
        filename = QFileDialog.getOpenFileName(self, 'Open file', '.')[0]
        self.displayedPicturePath = filename
        self.displayedPicture = filename
        self.updatePicture()
        
    def findPath(self):
        if ( self.displayedPicture is None ):
            raise Exception("Error, no valid path found")
        
        #print(self.instructions.text())
        elif (self.instructions.text() !=  "All done, press \'Find path\' to begin"):
            raise Exception("Error, select valid start and stop point")

        else:
            qImage = QPixmap(self.displayedPicture).toImage()
            scale = int( self.scaleBox.text() )

            imageCon = ImageConverter()
            pathX, pathY = imageCon.findShortestPathOfImage( self.displayedPicturePath, self.startXY, self.stopXY, scale )

            circle_range = [-2, -1, 0, 1, 2]

            for i in range( len(pathX) ):
                for row in circle_range:
                    for col in circle_range:

                        if ( np.abs( np.abs(row) + np.abs(col) ) <= 3  ): 
                            qImage.setPixel( pathX[i] + row , pathY[i] + col, QColor("red").rgb() )

            new_image = QPixmap.fromImage( qImage )
            self.instructions.setText("All done!")
            self.displayedPicture = new_image
            new_image = new_image.scaledToWidth( int( imageScale * self.windowWidth ) )
            self.label.setPixmap( new_image )

    
    def updatePicture(self):
        
        pixmap = QPixmap(self.displayedPicture)
        pixmap = pixmap.scaledToWidth( int( imageScale * self.windowWidth ) )

        if (self.instructions.text() == "Upload a picture from Google Maps"):
            pixmap = QPixmap(self.displayedPicture)
            pixmap = pixmap.scaledToWidth( int( imageScale * self.windowWidth ) )
            self.instructions.setText("Indicate starting position by pressing left mouse button")
            self.label.setPixmap( pixmap )
        
        elif (self.instructions.text() == "Indicate starting position by pressing left mouse button"):
            qImage = QPixmap(self.displayedPicture).toImage()

            circle_range = [-3, -2, -1, 0, 1, 2, 3]

            for row in circle_range:
                for col in circle_range:

                    if ( np.abs( np.abs(row) + np.abs(col) ) <= 4  ): 
                        qImage.setPixel( self.mouseX + row , self.mouseY + col, QColor("red").rgb() )

            self.startXY = [ self.mouseX, self.mouseY ]

            new_image = QPixmap.fromImage( qImage )
            self.instructions.setText("Indicate stopping position by pressing left mouse button")
            self.displayedPicture = new_image
            new_image = new_image.scaledToWidth( int( imageScale * self.windowWidth ) )
            self.label.setPixmap( new_image )

        elif (self.instructions.text() == "Indicate stopping position by pressing left mouse button"):
            qImage = QPixmap(self.displayedPicture).toImage()

            circle_range = [-3, -2, -1, 0, 1, 2, 3]

            for row in circle_range:
                for col in circle_range:

                    if ( np.abs( np.abs(row) + np.abs(col) ) <= 4  ): 
                        qImage.setPixel( self.mouseX + row , self.mouseY + col, QColor("red").rgb() )

            self.stopXY = [ self.mouseX, self.mouseY ]

            new_image = QPixmap.fromImage( qImage )
            self.instructions.setText("All done, press \'Find path\' to begin")
            self.displayedPicture = new_image
            new_image = new_image.scaledToWidth( int( imageScale * self.windowWidth ) )
            self.label.setPixmap( new_image )



    def registerMousePos(self, event):
        if ( self.displayedPicture is not None ):
            temp_pix = QPixmap(self.displayedPicture)

            print( temp_pix.width() / self.windowWidth )

            self.mouseX , self.mouseY = int (event.x() * temp_pix.width() / self.windowWidth), int(event.y() * temp_pix.width() / self.windowWidth)

            if ( self.mouseX >= 0 and self.mouseX <= temp_pix.width() and
                 self.mouseY >= 0 and self.mouseY <= temp_pix.height()   ):
                
               self.updatePicture()


def runMap():
    return 0

def window():
    app = QApplication(sys.argv)
    win = MainWindow()

    win.show()
    sys.exit(app.exec_())


window()