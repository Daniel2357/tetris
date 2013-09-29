import Polyomino

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
		self._rows = [[Polyomino.Polyomino.NONE] * self.width for i in range(self.height)]

	def setTypeAt(self, x, y, polyominoType):
		self._rows[y][x] = polyominoType

	def getTypeAt(self, x, y):
		return self._rows[y][x]

	def getDistanceToBottom(self, polyomino):
		dist = self.height
		for x,y in polyomino.getCoords():
			for i in range(math.ceil(y) + 1, self.height):
				if self.getTypeAt(x, i) != Polyomino.Polyomino.NONE:
					if i - y - 1 < dist:
						dist = i - y - 1
					break
			else:
				if self.height - y - 1 < dist:
					dist = self.height - y - 1
		return dist

	def polyominoAtValidPosition(self, polyomino):
		for x,y in polyomino.getCoords():
			if x < 0 or x >= self.width or y < 0 or y > self.height - 1 or self.getTypeAt(x, math.floor(y) + 1) != Polyomino.Polyomino.NONE:
				return False
		return True

	def addToRows(self, polyomino):
		for x,y in polyomino.getCoords():
			self.setTypeAt(x, math.ceil(y), polyomino.getType())

