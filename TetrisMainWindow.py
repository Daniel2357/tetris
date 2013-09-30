from PyQt4 import QtGui, uic, QtCore

import TetrisGame
import GameWidget

class TetrisMainWindow(QtGui.QMainWindow):
	
	def __init__(self, gameWidget):
		super().__init__()
		uic.loadUi('TetrisMainWindow.ui', self)
		
		self.gameWidget = gameWidget
		self.centralWidget().layout().addWidget(self.gameWidget)
		
		self.connect(self.btnStart, QtCore.SIGNAL('clicked()'), self.onStartClicked)
		self.connect(self.btnTogglePause, QtCore.SIGNAL('clicked()'), self.onTogglePauseClicked)

	def onStartClicked(self):
		self.emit(QtCore.SIGNAL('gameStarted()'))
		
	def onTogglePauseClicked(self):
		self.emit(QtCore.SIGNAL('pauseToggled()'))
		
	def setStartButtonEnabled(self, e):
		self.btnStart.setEnabled(e)
		
	def setTogglePauseButtonEnabled(self, e):
		self.btnTogglePause.setEnabled(e)
	
	def togglePauseResumeText(self):
		if self.btnTogglePause.text() == 'pause':
			self.btnTogglePause.setText('resume')
		else:
			self.btnTogglePause.setText('pause')

