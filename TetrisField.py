import Polyomino

import math

class TetrisField:

	def __init__(self):
		self.width = 10
		self.height = 22
		self.numHidden = 2
		self.clear()

	def _getEmptyField(self):
		return [[Polyomino.Polyomino.NONE] * self.width for i in range(self.height)]

	def clear(self):
		self._rows = self._getEmptyField()

	def setTypeAt(self, column, row, polyominoType):
		self._rows[row - 1][column - 1] = polyominoType

	def getTypeAt(self, column, row):
		return self._rows[row - 1][column - 1]

	def getDistanceToBottom(self, polyomino):
		dist = self.height
		for x,y in polyomino.getCoords():
			for i in range(min(math.floor(y), math.ceil(y - 1)), 0, -1):
				if self.getTypeAt(x, i) != Polyomino.Polyomino.NONE:
					if y - i - 1 < dist:
						dist = y - i - 1
					break
			else:
				if y - 1 < dist:
					dist = y - 1
		return dist

	def polyominoAtValidPosition(self, polyomino):
		for x,y in polyomino.getCoords():
			outOfBounds = x < 1 or x > self.width or y < 1 or y > self.height
			if outOfBounds or self.getTypeAt(x, math.floor(y)) != Polyomino.Polyomino.NONE or self.getTypeAt(x, round(y)) != Polyomino.Polyomino.NONE:
				return False
		return True

	def addToRows(self, polyomino):
		for x,y in polyomino.getCoords():
			self.setTypeAt(x, round(y), polyomino.getType())

	def clearFullRows(self):
		newRows = self._getEmptyField()
		lastRow = 0
		for row in range(1, self.height + 1):
			for column in range(1, self.width + 1):
				if self.getTypeAt(column, row) == Polyomino.Polyomino.NONE:
					newRows[lastRow] = self._rows[row - 1]
					lastRow += 1
					break
		self._rows = newRows

