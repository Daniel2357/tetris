import TetrisShape

import math

class TetrisField:
	
	def __init__(self):
		self.width = 0
		self.height = 0
		self.rows = []
		
	def setDimensions(self, width, height):
		self.width = width
		self.height = height
		self.clear()

	def clear(self):
		self.rows = [[TetrisShape.TetrisShape.NONE] * self.width for i in range(self.height)]
	
	def setTypeAt(self, x, y, shapeType):
		self.rows[y][x] = shapeType
		
	def getTypeAt(self, x, y):
		return self.rows[y][x]
		
	def reachedBottom(self, shape):
		for x in range(0, self.width):
			maxY = shape.maxY(x)
			if shape.hasBlockAt(x) and (math.floor(maxY) == self.height - 1 or self.getTypeAt(x, math.floor(maxY) + 1) != TetrisShape.TetrisShape.NONE):
				return True
		return False
		
	def addToRows(self, shape):
		shape.y = math.floor(shape.y)
		for x,y in shape.coords:
			self.setTypeAt(shape.x + x, shape.y + y, shape.getType())

