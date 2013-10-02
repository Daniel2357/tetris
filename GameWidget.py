from PyQt4 import QtGui, QtCore

import Polyomino

class GameWidget(QtGui.QWidget):

	def __init__(self):
		super().__init__()
		
		self.currentPolyomino, self.nextPolyominos = None, []
		self.keyPressed = False

		self.setFocusPolicy(QtCore.Qt.ClickFocus)

	def minimumSizeHint(self):
		minX = 100
		minY = 100
		if self.field != None:
			minX = self.blockSize * self.field.width
			minY = self.blockSize * self.field.height
		if self.nextPolyominos != []:
			minX += self.blockSize * (1 + 6)
		return QtCore.QSize(minX, minY)
		
	def setCurrentPolyomino(self, polyomino):
		self.currentPolyomino = polyomino
		
	def setNextPolyominos(self, polyominos):
		self.nextPolyominos = polyominos
		
	def setGameField(self, field):
		self.field = field
		
	def setBlockSize(self, size):
		self.blockSize = size
		
	def paintEvent(self, event):
		p = QtGui.QPainter(self)

		p.fillRect(0, 0, self.field.width * self.blockSize, self.field.height * self.blockSize, QtGui.QColor(0xFFFFFF))
		p.fillRect((self.field.width + 1) * self.blockSize, 0, 6 * self.blockSize, self.field.height * self.blockSize, QtGui.QColor(0xCCCCCC))

		if self.currentPolyomino != None and self.currentPolyomino.isVisible(self.field):
			self.drawPolyomino(p, self.currentPolyomino, 0, 0, True)

		for i, next in enumerate(self.nextPolyominos):
			self.drawPolyomino(p, next, self.field.width - next._x + 2 + 1, -3 * i - 1, False)

		for column in range(1, self.field.width + 1):
			for row in range(1, self.field.height - self.field.numHidden + 1):
				if self.field.getTypeAt(column, row) != Polyomino.Polyomino.NONE:
					self.drawSquare(p, (column - 1) * self.blockSize, (self.field.height - row) * self.blockSize, self.field.getTypeAt(column, row))
				
	def drawPolyomino(self, painter, polyomino, offsetX, offsetY, drawShadow):
		if drawShadow:
			d = self.field.getDistanceToBottom(polyomino)
			for x,y in polyomino.getCoords():
				self.drawSquare(painter, (x - 1 + offsetX) * self.blockSize, (self.field.height - (round(y - d) + offsetY)) * self.blockSize, Polyomino.Polyomino.SHADOW)
		
		for x,y in polyomino.getCoords():
			self.drawSquare(painter, (x - 1 + offsetX) * self.blockSize, (self.field.height - (y + offsetY)) * self.blockSize, polyomino.getType())
			
	def drawSquare(self, painter, x, y, shape):	
		colorTable = [0xCCCCCC, 0x00F0F0, 0xF0F000, 0xA000F0, 0x00F000, 0xF00000, 0x0000F0, 0xF0A000]

		color = QtGui.QColor(colorTable[shape])
		painter.fillRect(x + 1, y + 1, self.blockSize - 2, self.blockSize - 2, color)

	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Space:
			self.emit(QtCore.SIGNAL('dropShape()'))
		elif e.key() == QtCore.Qt.Key_Up:
			self.emit(QtCore.SIGNAL('rotateCounterClockwise()'))
		elif e.key() == QtCore.Qt.Key_Down:
			self.emit(QtCore.SIGNAL('rotateClockwise()'))
		else:
			self.keyPressed = True
			self.key = e.key()

	def keyReleaseEvent(self, e):
		self.keyPressed = False

