#! /usr/bin/python3

import numpy as np
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, \
		QSizePolicy, QMessageBox, QWidget, QLabel, QLineEdit, QVBoxLayout, \
		QPushButton, QGridLayout, QSyntaxHighlighter

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvass
from matplotlib.figure import Figure

import matplotlib.pyplot as plt

class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
 
        nameLabel = QLabel("Name:")
        self.nameLine = QLineEdit()
        self.submitButton = QPushButton("&amp;Submit")
 
        buttonLayout1 = QVBoxLayout()
        buttonLayout1.addWidget(nameLabel)
        buttonLayout1.addWidget(self.nameLine)
        buttonLayout1.addWidget(self.submitButton)
 
        self.submitButton.clicked.connect(self.submitContact)
 
        mainLayout = QGridLayout()
        # mainLayout.addWidget(nameLabel, 0, 0)
        mainLayout.addLayout(buttonLayout1, 0, 1)
 
        self.setLayout(mainLayout)
        self.setWindowTitle("Hello Qt")
 
    def submitContact(self):
        name = self.nameLine.text()
 
        if name == "":
            QMessageBox.information(self, "Empty Field",
                                    "Please enter a name and address.")
            return
        else:
            QMessageBox.information(self, "Success!",
                                    "Hello %s!" % name)

class MyHighlighter(QSyntaxHighlighter):
    """docstring for MyHighlighter"""
    def __init__(self, parent):
        QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        self.highlightrules
        
 
if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = Form()
    screen.show()
 
    sys.exit(app.exec_())