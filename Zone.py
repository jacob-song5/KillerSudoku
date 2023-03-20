import Cell

class Zone:
	def __init__(self):
		self.cells = list()
		self.id = ''

	def __str__(self):
		output = f"{self.id}\n"
		# output = ''
		sumTotal = 0
		length = len(self.cells)
		for i in range(length):
			sumTotal += self.cells[i].value
			# output += f"({self.cells[i].x},{self.cells[i].y})={self.cells[i].value}\n"
			output += f"({self.cells[i].x+1},{self.cells[i].y+1})\n"
		output += f"Total value={sumTotal}"
		return output

	def total(self):
		output = 0
		length = len(self.cells)
		for i in range(length):
			output += self.cells[i].value
		return output

	def add(self, cell):
		self.cells.append(cell)
		self.updateId()

	def contains(self, cell):
		length = len(self.cells)
		for i in range(length):
			if self.cells[i].x == cell.x and self.cells[i].y == cell.y:
				return True
		return False

	def containsValue(self, val):
		for c in self.cells:
			if c.value == val:
				return True
		return False

	def updateId(self):
		name = ''
		length = len(self.cells)
		for i in range(length):
			name += str(self.cells[i].x) + str(self.cells[i].y)
		self.id = name

	def topLeftMostCell(self):
		output = Cell.Cell(9, 9, 0)
		for c in self.cells:
			if c.y < output.y:
				output = c
			elif (c.y == output.y) and (c.x < output.x):
				output = c
		return output

	def isAlignedWith(self, z):
		columns = set()
		rows = set()
		zColumns = set()
		zRows = set()

		for i in self.cells:
			columns.add(i.x)
			rows.add(i.y)

		for i in z.cells:
			zColumns.add(i.x)
			zRows.add(i.y)

		if len(columns) > 1 and len(zColumns) > 1:
			return columns == zColumns

		elif len(rows) > 1 and len(zRows) > 1:
			return rows == zRows

		return False

	def sameValuesWith(self, z):
		val = set()
		zVal = set()

		for i in self.cells:
			val.add(i.value)

		for i in z.cells:
			zVal.add(i.value)

		return val == zVal