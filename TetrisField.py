import TetrisShape

import math

class TetrisField:

	def __init__(self):
		self.width = 0
		self.height = 0
		self._rows = []

	def setDimensions(self, width, height):
		self.width = width
		self.height = height
		self.clear()

	def clear(self):
		self._rows = [[TetrisShape.TetrisShape.NONE] * self.width for i in range(self.height)]

	def setTypeAt(self, x, y, shapeType):
		self._rows[y][x] = shapeType

	def getTypeAt(self, x, y):
		return self._rows[y][x]

	def shapeInValidPosition(self, shape):
		for x,y in shape.getCoords():
			if x < 0 or x >= self.width or y < 0 or y >= self.height - 1:
				return False
			if self.getTypeAt(x, math.ceil(y)) != TetrisShape.TetrisShape.NONE:
				return False
		return True

	def addToRows(self, shape):
		for x,y in shape.getCoords():
			self.setTypeAt(x, math.ceil(y), shape.getType())

