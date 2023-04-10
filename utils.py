from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

def center(self):
    # Get the size of the screen
    screen = QtWidgets.QDesktopWidget().screenGeometry()
    # Get the size of the window
    size = self.geometry()
    # Calculate the center point of the screen
    center_point = QPoint(int(screen.width() / 2), int(screen.height() / 2))
    # Calculate the top-left point of the window to center it on the screen
    top_left = center_point - QPoint(int(size.width() / 2), int(size.height() / 2))
    # Move the window to the center of the screen
    self.move(top_left)
