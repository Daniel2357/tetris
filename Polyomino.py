import random

class Polyomino:

	NONE = -1
	SHADOW = 0
	I_SHAPE = 1
	J_SHAPE = 2
	L_SHAPE = 3
	O_SHAPE = 4
	S_SHAPE = 5
	T_SHAPE = 6
	Z_SHAPE = 7

	@staticmethod
	def getRandomPolyomino(initialX):
		polyominos = [ITetromino, JTetromino, LTetromino, OTetromino, STetromino, TTetromino, ZTetromino]
		return polyominos[random.randint(0, len(polyominos) - 1)](initialX)

	def __init__(self, initialX):
		self._x = initialX
		self._y = 0

	def getCoords(self):
		raise 'getCoords() is abstract in TetrisShape.'

	def getType(self):
		raise 'getType() is abstract in TetrisShape.'

	def atTop(self):
		for x,y in self.getCoords():
			if y == 0:
				return True
		return False

	def canShow(self, field):
		return field.polyominoAtValidPosition(self)
	
	def tryFall(self, field, speed):
		self._y += speed
		if not field.polyominoAtValidPosition(self):
			self._y -= speed
			return False
		return True

	def tryMove(self, field, numBlocks):
		self._x += numBlocks
		if not field.polyominoAtValidPosition(self):
			self._x -= numBlocks

	def moveToBottom(self, field):
		self._y += field.getDistanceToBottom(self)

class ITetromino(Polyomino):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 0), (1, 0), (2, 0), (3, 0)))

	def getType(self):
		return Polyomino.I_SHAPE

class JTetromino(Polyomino):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 0), (0, 1), (1, 1), (2, 1)))

	def getType(self):
		return Polyomino.J_SHAPE

class LTetromino(Polyomino):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 1), (1, 1), (2, 1), (2, 0)))

	def getType(self):
		return Polyomino.L_SHAPE

class OTetromino(Polyomino):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 0), (0, 1), (1, 0), (1, 1)))

	def getType(self):
		return Polyomino.O_SHAPE		

class STetromino(Polyomino):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 1), (1, 1), (1, 0), (2, 0)))

	def getType(self):
		return Polyomino.S_SHAPE

class TTetromino(Polyomino):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 1), (1, 1), (1, 0), (2, 1)))

	def getType(self):
		return Polyomino.T_SHAPE

class ZTetromino(Polyomino):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 0), (1, 0), (1, 1), (2, 1)))

	def getType(self):
		return Polyomino.Z_SHAPE

