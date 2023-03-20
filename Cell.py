class Cell:
	CARDINALITY = 9
	
	def __init__(self, x, y, value):
		self.x = x
		self.y = y
		self.value = value
		self.owned = False
		self.parent = ''

	def __str__(self):
		# return f"({self.x},{self.y})={self.value}"
		return str(self.value)

	def __repr__(self):
		return str(self.value)

	def fullPrint(self):
		print(f"({self.x},{self.y})={self.value}")

	# neighbor is from the same zone
	def isNeighbor(self, neighbor):
		return (not neighbor.owned) or (neighbor.parent == self.parent)