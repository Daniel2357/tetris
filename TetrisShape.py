import random

class TetrisShape:

	NONE = -1
	I_SHAPE = 0
	J_SHAPE = 1
	L_SHAPE = 2
	O_SHAPE = 3
	S_SHAPE = 4
	T_SHAPE = 5
	Z_SHAPE = 6

	@staticmethod
	def getRandomShape(initialX):
		shapes = [IShape, JShape, LShape, OShape, SShape, TShape, ZShape]
		return shapes[random.randint(0, len(shapes) - 1)](initialX)

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

	def tryFall(self, field, speed):
		self._y += speed
		if not field.shapeInValidPosition(self):
			self._y -= speed
			return False
		return True

	def tryMove(self, field, numBlocks):
		self._x += numBlocks
		if not field.shapeInValidPosition(self):
			self._x -= numBlocks


class IShape(TetrisShape):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 0), (1, 0), (2, 0), (3, 0)))

	def getType(self):
		return TetrisShape.I_SHAPE

class JShape(TetrisShape):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 0), (0, 1), (1, 1), (2, 1)))

	def getType(self):
		return TetrisShape.J_SHAPE

class LShape(TetrisShape):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 1), (1, 1), (2, 1), (2, 0)))

	def getType(self):
		return TetrisShape.L_SHAPE

class OShape(TetrisShape):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 0), (0, 1), (1, 0), (1, 1)))

	def getType(self):
		return TetrisShape.O_SHAPE		

class SShape(TetrisShape):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 1), (1, 1), (1, 0), (2, 0)))

	def getType(self):
		return TetrisShape.S_SHAPE

class TShape(TetrisShape):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 1), (1, 1), (1, 0), (2, 1)))

	def getType(self):
		return TetrisShape.T_SHAPE

class ZShape(TetrisShape):
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x, y) in ((0, 0), (1, 0), (1, 1), (2, 1)))

	def getType(self):
		return TetrisShape.Z_SHAPE

