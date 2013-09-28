from PyQt4 import QtCore

import random, time

import TetrisMainWindow, TetrisField, TetrisShape

class TetrisGame(QtCore.QObject):

	def __init__(self, mainWindow, gameWidget):
		super().__init__()
		
		random.seed()
		self.REFRESH_INTERVAL = 10 # ms
		self.FALL_SPEED = 10 # squares per second
		self.BLOCK_SIZE = 20 # pixels
		self.KEY_PRESS_INTERVAL = 50 # ms
		
		self.field = TetrisField.TetrisField()
		self.currentShape, self.nextShape = None, None
		self.lastKeyPressTime = 0
		
		self.gameWidget = gameWidget
		self.gameWidget.setGameField(self.field)
		self.gameWidget.setBlockSize(self.BLOCK_SIZE)
		self.connect(self.gameWidget, QtCore.SIGNAL('dropShape()'), self.dropCurrent)
		
		self.mainWindow = mainWindow
		self.connect(mainWindow, QtCore.SIGNAL('gameStarted()'), self.startGame)
		self.connect(mainWindow, QtCore.SIGNAL('pauseToggled()'), self.toggleGamePaused)
		
		self.timer = QtCore.QTimer()
		self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.tick)
		
	def tick(self):
		currTime = int(round(time.time() * 1000))
	
		if self.gameWidget.keyPressed and currTime - self.lastKeyPressTime >= self.KEY_PRESS_INTERVAL:
			self.lastKeyPressTime = currTime
			if self.gameWidget.key == QtCore.Qt.Key_Left:
				self.currentShape.tryMove(self.field, -1)
			elif self.gameWidget.key == QtCore.Qt.Key_Right:
				self.currentShape.tryMove(self.field, +1)
			
		if not self.currentShape.tryFall(self.field, self.FALL_SPEED * self.REFRESH_INTERVAL / 1000):
			self.field.addToRows(self.currentShape)
			if self.currentShape.atTop():
				self.resetGame()
			else:
				self.currentShape = self.nextShape
				if self.currentShape.canShow(self.field):
					self.nextShape = TetrisShape.TetrisShape.getRandomShape(self.field.width // 2 - 1)
					self.gameWidget.setCurrentShape(self.currentShape)
				else:
					self.resetGame()
			
		self.gameWidget.update()
	
	def startGame(self):	
		self.field.setDimensions(self.mainWindow.getFieldWidth(), self.mainWindow.getFieldHeight())
		
		self.currentShape = TetrisShape.TetrisShape.getRandomShape(self.field.width // 2 - 1)
		self.nextShape = TetrisShape.TetrisShape.getRandomShape(self.field.width // 2 - 1)
		
		self.gameWidget.setCurrentShape(self.currentShape)
		self.gameWidget.setFixedSize(self.BLOCK_SIZE * self.field.width, self.BLOCK_SIZE * self.field.height)
		self.gameWidget.setFocus()
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
		self.gameWidget.setCurrentShape(None)
		self.mainWindow.setStartButtonEnabled(True)
		self.mainWindow.setTogglePauseButtonEnabled(False)
		
	def dropCurrent(self):
		self.currentShape.moveToBottom(self.field)
		
