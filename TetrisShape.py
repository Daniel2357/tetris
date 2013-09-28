import random

import math

class TetrisShape:

	NONE = -1
	I_SHAPE = 0
	J_SHAPE = 1
	L_SHAPE = 2
	O_SHAPE = 3
	S_SHAPE = 4
	T_SHAPE = 5
	Z_SHAPE = 6
	 
	GLOBAL_COORDS = ( 
		((0, 0), (1, 0), (2, 0), (3, 0)),
		((0, 0), (0, 1), (1, 1), (2, 1)),
		((0, 1), (1, 1), (2, 1), (2, 0)),
		((0, 0), (0, 1), (1, 0), (1, 1)),
		((0, 1), (1, 1), (1, 0), (2, 0)),
		((0, 1), (1, 1), (1, 0), (2, 1)),
		((0, 0), (1, 0), (1, 1), (2, 1)) 
	)

	@staticmethod
	def getRandomShape(x):
		return TetrisShape(random.randint(0, 6), x)

	def __init__(self, shape, x):
		self._shape = shape
		self.coords = self.GLOBAL_COORDS[shape]
		self.x = x
		self.y = 0

	def getType(self):
		return self._shape
		
	def hasBlockAt(self, column):
		for x,y in self.coords:
			if self.x + x == column:
				return True
		return False
		
	def maxY(self, column):
		maxY = 0
		for x,y in self.coords:
			if self.x + x == column and self.y + y > maxY:
				maxY = self.y + y
		return maxY
		
	def atTop(self):
		for x,y in self.coords:
			if math.floor(self.y + y) == 0:
				return True
		return False
		
	def maxX(self):
		m = 0
		for x,y in self.coords:
			if self.x + x > m:
				m = self.x + x
		return m
		
	def tryMoveLeft(self, field):
		if self.x == 0:
			return
		for x,y in self.coords:
			if field.getTypeAt(self.x + x - 1, math.ceil(self.y + y)) != TetrisShape.NONE:
				return
		self.x -= 1
		
	def tryMoveRight(self, field):
		if self.maxX() >= field.width - 1:
			return
		for x,y in self.coords:
			if field.getTypeAt(self.x + x + 1, math.ceil(self.y + y)) != TetrisShape.NONE:
				return
		self.x += 1

	
