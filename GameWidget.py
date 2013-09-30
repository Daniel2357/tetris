from PyQt4 import QtGui, QtCore

import Polyomino

class GameWidget(QtGui.QWidget):

	def __init__(self):
		super().__init__()
		
		self.currentShape = None
		self.keyPressed = False

		self.setFocusPolicy(QtCore.Qt.ClickFocus)

		p = self.palette()
		p.setColor(QtGui.QPalette.Window, QtGui.QColor('white'))
		self.setPalette(p)
		self.setAutoFillBackground(True)
		
	def setCurrentShape(self, shape):
		self.currentShape = shape
		
	def setGameField(self, field):
		self.field = field
		
	def setBlockSize(self, size):
		self.blockSize = size
		
	def paintEvent(self, event):
		p = QtGui.QPainter(self)

		if self.currentShape != None and self.currentShape.isVisible(self.field):
			self.drawCurrentShape(p)

		for column in range(1, self.field.width + 1):
			for row in range(1, self.field.height - self.field.numHidden + 1):
				if self.field.getTypeAt(column, row) != Polyomino.Polyomino.NONE:
					self.drawSquare(p, (column - 1) * self.blockSize, (self.field.height - row) * self.blockSize, self.field.getTypeAt(column, row))
				
	def drawCurrentShape(self, p):
		d = self.field.getDistanceToBottom(self.currentShape)

		for x,y in self.currentShape.getCoords():
			self.drawSquare(p, (x - 1) * self.blockSize, (self.field.height - round(y - d)) * self.blockSize, Polyomino.Polyomino.SHADOW)
		
		for x,y in self.currentShape.getCoords():
			self.drawSquare(p, (x - 1) * self.blockSize, (self.field.height - y) * self.blockSize, self.currentShape.getType())
			
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

