import Cell
import random
import math

class Board:
	CARDINALITY = 9
	
	def __init__(self, srcString):
		self.board = list()
		self.zones = list()
		length = len(srcString)

		for i in range(self.CARDINALITY):
			self.board.append(list())
			for j in range(self.CARDINALITY):
				if length > 0:
					srcIndex = (i * self.CARDINALITY) + j
					#print(f"srcIndex={srcIndex} reads={srcString[srcIndex]}")
					#self.board[i].append(srcString[srcIndex])
					c = Cell.Cell(j, i, int(srcString[srcIndex]))
					self.board[i].append(c)
				else:
					c = Cell.Cell(j, i, 0)
					self.board[i].append(c)

	def isFull(self):
		for i in range(self.CARDINALITY):
			for j in range(self.CARDINALITY):
				if self.board[j][i].value == 0:
					return False
		return True

	def simplePrint(self):
		print()
		for i in range(self.CARDINALITY):
			print(self.board[i])
		print()

	def printZones(self):
		length = len(self.zones)
		for i in range(length):
			print(self.zones[i])
			print()

	def get(self, x, y):
		return self.board[y][x]

	def addZone(self, z):
		self.zones.append(z)

	def zoneTotal(self):
		total = 0
		length = len(self.zones)
		for i in range(length):
			total += self.zones[i].total()
		return total

	def markCellOwned(self, x, y):
		self.board[y][x].owned = True

	def markCellOwned(self, cell):
		self.board[cell.y][cell.x].owned = True

	def zoneAttrition(self, zone):
		length = len(zone.cells)
		for i in range(length):
			x = zone.cells[i].x
			y = zone.cells[i].y
			self.board[y][x].owned = True
			self.board[y][x].parent = zone.id

	def getRandomUnownedCell(self):
		unowned = list()
		for i in range(self.CARDINALITY):
			unownedRow = filter(lambda e: not e.owned, self.board[i])
			unowned += unownedRow

		length = len(unowned)
		if length > 1:
			c = random.choice(unowned)
			return self.board[c.y][c.x]
		elif length == 1:
			c = unowned[0]
			return self.board[c.y][c.x]
		else: 
			return None

	def randomAdjacentCell(self, zone):
		availableCells = set()
		length = len(zone.cells)
		for i in range(length):
			availableNeighbors = self.getAvailableCellNeighbors(zone.cells[i])
			for j in availableNeighbors:
				if not zone.containsValue(j.value):
					availableCells.add(j)
		availableCells = list(availableCells)
		if len(availableCells) > 0:
			return random.choice(availableCells)
		return None

	def getAvailableCellNeighbors(self, homeCell):
		output = list()

		c = self.cellAbove(homeCell)
		if c != None and (not c.owned):
			output.append(c)

		c = self.cellRight(homeCell)
		if c != None and (not c.owned):
			output.append(c)

		c = self.cellBelow(homeCell)
		if c != None and (not c.owned):
			output.append(c)

		c = self.cellLeft(homeCell)
		if c != None and (not c.owned):
			output.append(c)

		return output

	def cellAbove(self, cell):
		if cell == None or cell.y == 0:
			return None
		return self.board[cell.y-1][cell.x]

	def cellBelow(self, cell):
		if cell.y == self.CARDINALITY - 1:
			return None
		return self.board[cell.y+1][cell.x]

	def cellRight(self, cell):
		if cell.x == self.CARDINALITY - 1:
			return None
		return self.board[cell.y][cell.x+1]

	def cellLeft(self, cell):
		if cell.x == 0:
			return None
		return self.board[cell.y][cell.x-1]
		
	def checkSolution(self):
		for i in range(self.CARDINALITY):
			for j in range(self.CARDINALITY):
				if not self.isCellValid(self.board[j][i]):
					return False
		return True

	# Checks if any other cell in row/column/section has same value
	def isCellValid(self, cell):
		if cell == None or cell.value == 0:
			return False
		return not self.checkCollisionCells(cell, lambda x, y: x.value == y.value)

	# For a given cell, run a comparison function against all other cells from row, column, section. Returns True when any cell evaluates to true in checkFunction
	def checkCollisionCells(self, cell, checkFunction):
		# Check rows and columns
		for i in range(self.CARDINALITY):
			if (i != cell.x) and (checkFunction(cell, self.board[cell.y][i])):
				print(f"Cell ({i + 1},{cell.y + 1}) was found to have the same value {cell.value} as ({cell.x + 1},{cell.y + 1}) from row")
				return True
			if (i != cell.y) and (checkFunction(cell, self.board[i][cell.x])):
				print(f"Cell ({cell.x + 1},{i + 1}) was found to have the same value {cell.value} as ({cell.x + 1},{cell.y + 1}) from column")
				return True

		lowerXBound = math.floor(cell.x / 3) * 3
		lowerYBound = math.floor(cell.y / 3) * 3

		# Check 3x3 section
		for y in range(lowerYBound, lowerYBound+3):
			for x in range(lowerXBound, lowerXBound + 3):
				if (x != cell.x or y != cell.y) and (checkFunction(cell, self.board[y][x])):
					print(f"Cell ({x},{y}) was found to have the same value {cell.value} as ({cell.x},{cell.y}) from section")
					return True
		return False

	def getZoneOfCell(self, cell):
		for z in self.zones:
			if z.contains(cell):
				return z

		return None

	# Check if two cells come from the same zone
	def sameZone(self, cell1, cell2):
		for z in self.zones:
			if z.contains(cell1):
				return z.contains(cell2)