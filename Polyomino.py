import random

class Polyomino:

	NONE = -1
	SHADOW = 0
	I_SHAPE = 1
	O_SHAPE = 2
	T_SHAPE = 3
	S_SHAPE = 4
	Z_SHAPE = 5
	J_SHAPE = 6
	L_SHAPE = 7

	ROT_0 = 0
	ROT_90 = 1
	ROT_180 = 2
	ROT_270 = 3

	bag = []

	@staticmethod
	def getRandomPolyomino(field):
		polyominos = [ITetromino, JTetromino, LTetromino, OTetromino, STetromino, TTetromino, ZTetromino]

		if Polyomino.bag == []:
			Polyomino.bag = random.sample(range(0, len(polyominos)), len(polyominos))
	
		rand = polyominos[Polyomino.bag[0]](field)
		del Polyomino.bag[0]
		
		return rand

	@staticmethod
	def getJLSTZWallKickOffsets(startRotation, endRotation):
		if startRotation == Polyomino.ROT_0 and endRotation == Polyomino.ROT_90:
			return ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2))
		elif startRotation == Polyomino.ROT_90 and endRotation == Polyomino.ROT_0:
			return ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2))
		elif startRotation == Polyomino.ROT_90 and endRotation == Polyomino.ROT_180:
			return ((0, 0), (1, 0), (1, -1), (0, 2), (1, 2))
		elif startRotation == Polyomino.ROT_180 and endRotation == Polyomino.ROT_90:
			return ((0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2))
		elif startRotation == Polyomino.ROT_180 and endRotation == Polyomino.ROT_270:
			return ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2))
		elif startRotation == Polyomino.ROT_270 and endRotation == Polyomino.ROT_180:
			return ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2))
		elif startRotation == Polyomino.ROT_270 and endRotation == Polyomino.ROT_0:
			return ((0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2))
		elif startRotation == Polyomino.ROT_0 and endRotation == Polyomino.ROT_270:
			return ((0, 0), (1, 0), (1, 1), (0, -2), (1, -2))

	@staticmethod
	def getIWallKickOffsets(startRotation, endRotation):
		if startRotation == Polyomino.ROT_0 and endRotation == Polyomino.ROT_90:
			return ((0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2))
		elif startRotation == Polyomino.ROT_90 and endRotation == Polyomino.ROT_0:
			return ((0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2))
		elif startRotation == Polyomino.ROT_90 and endRotation == Polyomino.ROT_180:
			return ((0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1))
		elif startRotation == Polyomino.ROT_180 and endRotation == Polyomino.ROT_90:
			return ((0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1))
		elif startRotation == Polyomino.ROT_180 and endRotation == Polyomino.ROT_270:
			return ((0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2))
		elif startRotation == Polyomino.ROT_270 and endRotation == Polyomino.ROT_180:
			return ((0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2))
		elif startRotation == Polyomino.ROT_270 and endRotation == Polyomino.ROT_0:
			return ((0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1))
		elif startRotation == Polyomino.ROT_0 and endRotation == Polyomino.ROT_270:
			return ((0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1))

	def __init__(self, field):
		self._x = self.getStartX(field.width)
		self._y = field.height
		
		self._rotation = Polyomino.ROT_0

	def getCoords(self):
		raise 'getCoords() is abstract in TetrisShape.'

	def getType(self):
		raise 'getType() is abstract in TetrisShape.'

	def canShow(self, field):
		return field.polyominoAtValidPosition(self)

	def isVisible(self, field):
		for x,y in self.getCoords():
			if y < field.height - field.numHidden + 1:
				return True
		return False

	def tryFall(self, field, speed):
		self._y -= speed
		if not field.polyominoAtValidPosition(self):
			self._y += speed
			return False
		return True

	def tryMove(self, field, numBlocks):
		self._x += numBlocks
		if not field.polyominoAtValidPosition(self):
			self._x -= numBlocks

	def tryRotateCounterClockwise(self, field):
		startRotation = self._rotation
		self._rotateCounterClockwise()
		
		for x,y in self.getWallKickOffsets(startRotation, self._rotation):
			self._x += x
			self._y += y
			if field.polyominoAtValidPosition(self):
				break
			self._x -= x
			self._y -= y
		else:
			self._rotateClockwise()

	def tryRotateClockwise(self, field):
		startRotation = self._rotation
		self._rotateClockwise()
		
		for x,y in self.getWallKickOffsets(startRotation, self._rotation):
			self._x += x
			self._y += y
			if field.polyominoAtValidPosition(self):
				break
			self._x -= x
			self._y -= y
		else:
			self._rotateCounterClockwise()

	def _rotateCounterClockwise(self):
		self._rotation = (self._rotation - 1) % 4

	def _rotateClockwise(self):
		self._rotation = (self._rotation + 1) % 4

	def moveToBottom(self, field):
		self._y -= field.getDistanceToBottom(self)

class ITetromino(Polyomino):
	def getStartX(self, width):
		return (width - 4) // 2 + 1

	def getCoords(self):
		if self._rotation == Polyomino.ROT_0:
			return ((self._x + x, self._y + y) for (x,y) in ((0, -1), (1, -1), (2, -1), (3, -1)))
		elif self._rotation == Polyomino.ROT_90:
			return ((self._x + x, self._y + y) for (x,y) in ((2, 0), (2, -1), (2, -2), (2, -3)))
		elif self._rotation == Polyomino.ROT_180:
			return ((self._x + x, self._y + y) for (x,y) in ((0, -2), (1, -2), (2, -2), (3, -2)))
		elif self._rotation == Polyomino.ROT_270:
			return ((self._x + x, self._y + y) for (x,y) in ((1, 0), (1, -1), (1, -2), (1, -3)))

	def getWallKickOffsets(self, startRotation, endRotation):
		return Polyomino.getIWallKickOffsets(startRotation, endRotation)
	
	def getType(self):
		return Polyomino.I_SHAPE

class JTetromino(Polyomino):
	def getStartX(self, width):
		return (width - 4) // 2 + 1

	def getCoords(self):
		if self._rotation == Polyomino.ROT_0:
			return ((self._x + x, self._y + y) for (x,y) in ((0, 0), (0, -1), (1, -1), (2, -1)))
		elif self._rotation == Polyomino.ROT_90:
			return ((self._x + x, self._y + y) for (x,y) in ((1, 0), (2, 0), (1, -1), (1, -2)))
		elif self._rotation == Polyomino.ROT_180:
			return ((self._x + x, self._y + y) for (x,y) in ((0, -1), (1, -1), (2, -1), (2, -2)))
		elif self._rotation == Polyomino.ROT_270:
			return ((self._x + x, self._y + y) for (x,y) in ((1, 0), (1, -1), (1, -2), (0, -2)))

	def getWallKickOffsets(self, startRotation, endRotation):
		return Polyomino.getJLSTZWallKickOffsets(startRotation, endRotation)

	def getType(self):
		return Polyomino.J_SHAPE

class LTetromino(Polyomino):
	def getStartX(self, width):
		return (width - 4) // 2 + 1
	
	def getCoords(self):
		if self._rotation == Polyomino.ROT_0:
			return ((self._x + x, self._y + y) for (x,y) in ((0, -1), (1, -1), (2, -1), (2, 0)))
		elif self._rotation == Polyomino.ROT_90:
			return ((self._x + x, self._y + y) for (x,y) in ((1, 0), (1, -1), (1, -2), (2, -2)))
		elif self._rotation == Polyomino.ROT_180:
			return ((self._x + x, self._y + y) for (x,y) in ((0, -1), (1, -1), (2, -1), (0, -2)))
		elif self._rotation == Polyomino.ROT_270:
			return ((self._x + x, self._y + y) for (x,y) in ((0, 0), (1, 0), (1, -1), (1, -2)))

	def getWallKickOffsets(self, startRotation, endRotation):
		return Polyomino.getJLSTZWallKickOffsets(startRotation, endRotation)

	def getType(self):
		return Polyomino.L_SHAPE

class OTetromino(Polyomino):
	def getStartX(self, width):
		return (width - 2) // 2 + 1
	
	def getCoords(self):
		return ((self._x + x, self._y + y) for (x,y) in ((0, 0), (1, 0), (0, -1), (1, -1)))

	def getWallKickOffsets(self, startRotation, endRotation):
		return ((0, 0), (0,0))

	def getType(self):
		return Polyomino.O_SHAPE		

class STetromino(Polyomino):
	def getStartX(self, width):
		return (width - 4) // 2 + 1

	def getCoords(self):
		if self._rotation == Polyomino.ROT_0:
			return ((self._x + x, self._y + y) for (x,y) in ((1, 0), (2, 0), (0, -1), (1, -1)))
		elif self._rotation == Polyomino.ROT_90:
			return ((self._x + x, self._y + y) for (x,y) in ((1, 0), (1, -1), (2, -1), (2, -2)))
		elif self._rotation == Polyomino.ROT_180:
			return ((self._x + x, self._y + y) for (x,y) in ((1, -1), (2, -1), (0, -2), (1, -2)))
		elif self._rotation == Polyomino.ROT_270:
			return ((self._x + x, self._y + y) for (x,y) in ((0, 0), (0, -1), (1, -1), (1, -2)))

	def getWallKickOffsets(self, startRotation, endRotation):
		return Polyomino.getJLSTZWallKickOffsets(startRotation, endRotation)

	def getType(self):
		return Polyomino.S_SHAPE

class TTetromino(Polyomino):
	def getStartX(self, width):
		return (width - 4) // 2 + 1

	def getCoords(self):
		if self._rotation == Polyomino.ROT_0:
			return ((self._x + x, self._y + y) for (x,y) in ((1, 0), (0, -1), (1, -1), (2, -1)))
		elif self._rotation == Polyomino.ROT_90:
			return ((self._x + x, self._y + y) for (x,y) in ((1, 0), (1, -1), (2, -1), (1, -2)))
		elif self._rotation == Polyomino.ROT_180:
			return ((self._x + x, self._y + y) for (x,y) in ((0, -1), (1, -1), (2, -1), (1, -2)))
		elif self._rotation == Polyomino.ROT_270:
			return ((self._x + x, self._y + y) for (x,y) in ((1, 0), (0, -1), (1, -1), (1, -2)))

	def getWallKickOffsets(self, startRotation, endRotation):
		return Polyomino.getJLSTZWallKickOffsets(startRotation, endRotation)

	def getType(self):
		return Polyomino.T_SHAPE

class ZTetromino(Polyomino):
	def getStartX(self, width):
		return (width - 4) // 2 + 1

	def getCoords(self):
		if self._rotation == Polyomino.ROT_0:
			return ((self._x + x, self._y + y) for (x,y) in ((0, 0), (1, 0), (1, -1), (2, -1)))
		elif self._rotation == Polyomino.ROT_90:
			return ((self._x + x, self._y + y) for (x,y) in ((2, 0), (1, -1), (2, -1), (1, -2)))
		elif self._rotation == Polyomino.ROT_180:
			return ((self._x + x, self._y + y) for (x,y) in ((0, -1), (1, -1), (1, -2), (2, -2)))
		elif self._rotation == Polyomino.ROT_270:
			return ((self._x + x, self._y + y) for (x,y) in ((1, 0), (0, -1), (1, -1), (0, -2)))

	def getWallKickOffsets(self, startRotation, endRotation):
		return Polyomino.getJLSTZWallKickOffsets(startRotation, endRotation)
		
	def getType(self):
		return Polyomino.Z_SHAPE

