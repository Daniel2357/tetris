from PyQt4 import QtCore

import random, time

import TetrisMainWindow, TetrisField, Polyomino

class TetrisGame(QtCore.QObject):

	def __init__(self, mainWindow, gameWidget):
		super().__init__()
		
		random.seed()
		self.REFRESH_INTERVAL = 10 # ms
		self.FALL_SPEED = 5 # squares per second
		self.BLOCK_SIZE = 20 # pixels
		self.KEY_PRESS_INTERVAL = 65 # ms
		
		self.field = TetrisField.TetrisField()
		self.currentPolyomino, self.nextPolyominos = None, []
		self.lastKeyPressTime = 0
		
		self.gameWidget = gameWidget
		self.gameWidget.setGameField(self.field)
		self.gameWidget.setBlockSize(self.BLOCK_SIZE)
		self.connect(self.gameWidget, QtCore.SIGNAL('dropShape()'), self.dropShape)
		self.connect(self.gameWidget, QtCore.SIGNAL('rotateCounterClockwise()'), self.rotateShapeCounterClockwise)
		self.connect(self.gameWidget, QtCore.SIGNAL('rotateClockwise()'), self.rotateShapeClockwise)
		
		self.mainWindow = mainWindow
		self.connect(mainWindow, QtCore.SIGNAL('gameStarted()'), self.startGame)
		self.connect(mainWindow, QtCore.SIGNAL('pauseToggled()'), self.toggleGamePaused)
		
		self.timer = QtCore.QTimer()
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.tick)
		
	def tick(self):
		currTime = round(time.time() * 1000)
	
		if self.gameWidget.keyPressed and currTime - self.lastKeyPressTime >= self.KEY_PRESS_INTERVAL:
			self.lastKeyPressTime = currTime
			if self.gameWidget.key == QtCore.Qt.Key_Left:
				self.currentPolyomino.tryMove(self.field, -1)
			elif self.gameWidget.key == QtCore.Qt.Key_Right:
				self.currentPolyomino.tryMove(self.field, +1)
			
		if not self.currentPolyomino.tryFall(self.field, self.FALL_SPEED * self.REFRESH_INTERVAL / 1000):
			self.field.addToRows(self.currentPolyomino)
			self.field.clearFullRows()
			if not self.nextPolyominos[0].canShow(self.field) or not self.currentPolyomino.isVisible(self.field):
				self.resetGame()
			else:
				self.currentPolyomino = self.nextPolyominos[0]
				del self.nextPolyominos[0]
				self.nextPolyominos += [Polyomino.Polyomino.getRandomPolyomino(self.field)]
				self.gameWidget.setCurrentPolyomino(self.currentPolyomino)
				self.gameWidget.setNextPolyominos(self.nextPolyominos)
		self.gameWidget.update()

	def startGame(self):
		self.field.clear()
		
		self.currentPolyomino = Polyomino.Polyomino.getRandomPolyomino(self.field)
		self.nextPolyominos = [Polyomino.Polyomino.getRandomPolyomino(self.field), Polyomino.Polyomino.getRandomPolyomino(self.field), Polyomino.Polyomino.getRandomPolyomino(self.field)]
		
		self.gameWidget.setCurrentPolyomino(self.currentPolyomino)
		self.gameWidget.setNextPolyominos(self.nextPolyominos)
		self.gameWidget.setFocus()
		self.gameWidget.setFixedSize(self.gameWidget.minimumSizeHint())
		self.mainWindow.setFixedSize(self.mainWindow.minimumWidth(), self.mainWindow.minimumHeight())
		
		self.mainWindow.setStartButtonEnabled(False)
		self.mainWindow.setTogglePauseButtonEnabled(True)
		
		self.timer.start(self.REFRESH_INTERVAL)
		
	def toggleGamePaused(self):
		if self.timer.isActive():
			self.timer.stop()
		else:
			self.timer.start(self.REFRESH_INTERVAL)
		self.mainWindow.togglePauseResumeText()
			
	def resetGame(self):
		self.timer.stop()
		self.gameWidget.setCurrentPolyomino(None)
		self.gameWidget.setNextPolyominos([])
		self.mainWindow.setStartButtonEnabled(True)
		self.mainWindow.setTogglePauseButtonEnabled(False)
		
	def dropShape(self):
		self.currentPolyomino.moveToBottom(self.field)

	def rotateShapeCounterClockwise(self):
		self.currentPolyomino.tryRotateCounterClockwise(self.field)

	def rotateShapeClockwise(self):
		self.currentPolyomino.tryRotateClockwise(self.field)

