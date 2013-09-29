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
		
		if self.currentShape != None:
			self.drawCurrentShape(p)
			
		for x in range(self.field.width):
			for y in range(self.field.height):
				if self.field.getTypeAt(x, y) != Polyomino.Polyomino.NONE:
					self.drawSquare(p, x * self.blockSize, y * self.blockSize, self.field.getTypeAt(x, y))
		
	def drawCurrentShape(self, p):
		d = self.field.getDistanceToBottom(self.currentShape)
		
		for x,y in self.currentShape.getCoords():
			self.drawSquare(p, x * self.blockSize, y * self.blockSize, self.currentShape.getType())
			if d >= 2:
				self.drawSquare(p, x * self.blockSize, (y + d) * self.blockSize, Polyomino.Polyomino.SHADOW)
			
	def drawSquare(self, painter, x, y, shape):	
		colorTable = [0xCCCCCC, 0xCC6666, 0x66CC66, 0x6666CC, 0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

		color = QtGui.QColor(colorTable[shape])
		painter.fillRect(x + 1, y + 1, self.blockSize - 2, self.blockSize - 2, color)

	def keyPressEvent(self, e):
		if e.key() == QtCore.Qt.Key_Space:
			self.emit(QtCore.SIGNAL('dropShape()'))
		else:
			self.keyPressed = True
			self.key = e.key()

	def keyReleaseEvent(self, e):
		self.keyPressed = False

