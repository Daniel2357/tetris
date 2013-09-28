#!/usr/bin/python3

from PyQt4 import QtGui
import sys

import TetrisMainWindow
import GameWidget
import TetrisGame

app = QtGui.QApplication(sys.argv)

gameWidget = GameWidget.GameWidget()
mainWindow = TetrisMainWindow.TetrisMainWindow(gameWidget)
game = TetrisGame.TetrisGame(mainWindow, gameWidget)
mainWindow.show()

sys.exit(app.exec_())

