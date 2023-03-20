import tkinter as tk
import Board
import Zone
import math
import random
import os

class GameDisplay:
	CARDINALITY = 9
	SOURCE_PUZZLES_PATH = "./sudoku.csv"
	DEMO_PUZZLE_STRINGS = [
		"070000043040009610800634900094052000358460020000800530080070091902100005007040802,679518243543729618821634957794352186358461729216897534485276391962183475137945862", 
		"301086504046521070500000001400800002080347900009050038004090200008734090007208103,371986524846521379592473861463819752285347916719652438634195287128734695957268143",
		"048301560360008090910670003020000935509010200670020010004002107090100008150834029,748391562365248791912675483421786935589413276673529814834962157296157348157834629",
		"008317000004205109000040070327160904901450000045700800030001060872604000416070080,298317645764285139153946278327168954981453726645792813539821467872634591416579382",
		"040890630000136820800740519000467052450020700267010000520003400010280970004050063,142895637975136824836742519398467152451328796267519348529673481613284975784951263"
	]

	def __init__(self):
		self.board = Board.Board(self.getRandomPuzzleString(self.SOURCE_PUZZLES_PATH))
		self.userBoard = Board.Board('')

		self.selectedCell = None
		self.cellWidth = 100
		self.cellHeight = 100
		self.labels = list()
		self.zoneTotalLabels = list()
		self.noteMode = False

		self.root = tk.Tk()
		# self.root.geometry("1000x900")
		self.frame = tk.Frame(self.root, bg='white')
		self.frame.grid()
		self.noteModeLabel = tk.Label(self.frame, bg='white', text='Number', font=("Arial", 12))
		self.noteModeLabel.grid(column=0, row=9)
		self.root.bind('<Button-1>', self.mouseClick)
		self.root.bind('<KeyPress>', self.keyPress)

		self.loadBoard()
		self.resetGame()

	def start(self):
		self.root.mainloop()

	def resetGame(self):
		if self.selectedCell != None:
			self.setCellColor(self.selectedCell.x, self.selectedCell.y, 'white')
		self.selectedCell = None
		self.noteMode = False
		self.noteModeLabel.config(text='Number')
		self.userBoard = Board.Board('')
		# reset zone and cell labels
		for i in range(self.CARDINALITY):
			for j in range(self.CARDINALITY):
				self.zoneTotalLabels[i][j].config(text='')
				self.labels[i][j].config(text='', font=("Arial", 40), fg='black')
				self.labels[i][j].master.delete('border')
				self.setCellColor(j, i, 'white')

		s = self.getRandomPuzzleString(self.SOURCE_PUZZLES_PATH)
		self.board = Board.Board(s)
		self.initBoardZones()
		self.loadZoneTotals()
		self.loadAutoZoneNotes()
		self.markIdenticalZones()
		self.markSingleCellZones()

		# self.board.simplePrint()
		# print(self.board.zones[0].isAlignedWith(self.board.zones[1]))

	def initBoardZones(self):
		c = self.board.getRandomUnownedCell()
		z = Zone.Zone()
		while c != None:
			# c.fullPrint()
			# print()

			zoneLength = len(z.cells)
			if (zoneLength < 2):
				z.add(c)
				self.board.zoneAttrition(z)
				c = self.board.randomAdjacentCell(z)
				if c == None:
					self.board.addZone(z)
					z = Zone.Zone()
					c = self.board.getRandomUnownedCell()
			elif self.yesOrNo() and len(z.cells) < 5:
				z.add(c)
				self.board.zoneAttrition(z)
				c = self.board.randomAdjacentCell(z)
				if c == None:
					self.board.addZone(z)
					z = Zone.Zone()
					c = self.board.getRandomUnownedCell()
			else:
				self.board.addZone(z)
				z = Zone.Zone()
				c = self.board.getRandomUnownedCell()

		length = len(z.cells)
		if length > 0:
			for i in range(length):
				self.board.markCellOwned(z.cells[i])
			self.board.addZone(z)

	def yesOrNo(self):
		options = [1, 2]
		return random.choice(options) % 2 == 0

	def getRandomPuzzleString(self, srcFile):
		if os.path.isfile(srcFile):
			r = random.randrange(1, 100000)
			#print(r)
			startLineOffset = len("puzzle,solution\n")
			lineOffset = ((self.CARDINALITY**2) * 2) + 2 #newline, comma
			totalOffset = startLineOffset + (r * lineOffset)

			f = open(srcFile, 'r')
			f.seek(totalOffset)
			output = f.readline()
			output = output.split(',')[1]
			f.close()
			# print(output)
			return output
		else:
			return random.choice(self.DEMO_PUZZLE_STRINGS).split(',')[1]

	def keyPress(self, e):
		# print(f"Key pressed: {e}")
		# Number key
		if (48 < e.keycode < 58):
			self.numKeyPressed(e.keycode-48)
		# 0 key / Backspace
		elif e.keycode == 48 or e.keycode == 8:
			self.labels[self.selectedCell.y][self.selectedCell.x].config(text='', font=("Arial", 40), fg='black')
			self.setCellColor(self.selectedCell.x, self.selectedCell.y, 'cyan')
			self.userBoard.board[self.selectedCell.y][self.selectedCell.x].value = 0
		# Page down
		elif e.keycode == 34:
			self.noteMode = not self.noteMode
			if self.noteMode:
				self.noteModeLabel.config(text="Note")
			else:
				self.noteModeLabel.config(text="Number")
		# Arrow keys
		elif (36 < e.keycode < 41):
			self.arrowKeyPressed(e.keycode)
		# N key
		elif e.keycode == 78:
			self.resetGame()

		# H key
		elif e.keycode == 72:
			if self.selectedCell != None:
				userCell = self.userBoard.get(self.selectedCell.x, self.selectedCell.y)
				solutionCell = self.board.get(self.selectedCell.x, self.selectedCell.y)
				if userCell.value == 0:
					self.markCell(solutionCell, solutionCell.value)
					# userCell.value = solutionCell.value
					# self.labels[userCell.y][userCell.x].config(text=str(userCell.value), font=("Arial", 40), fg='black')

	def mouseClick(self, e):
		x = 0
		y = 0

		if type(e.widget) is tk.Canvas:
			x = e.widget.winfo_x()
			y = e.widget.winfo_y()
		elif type(e.widget) is tk.Label:
			x = e.widget.master.winfo_x()
			y = e.widget.master.winfo_y()
		else:
			x = e.x
			y = e.y

		# placeholder for border logic
		if x == 0:
			x += 1
		if y == 0:
			y += 1

		# print(f"({x},{y})")

		if (x % self.cellWidth == 0) or (y % self.cellHeight == 0):
			print('clicked border')
			return

		column = math.floor(x / self.cellWidth)
		row = math.floor(y / self.cellHeight)

		if (0 <= column < 9) and (0 <= row < 9):
			self.selectCell(column, row)

	def loadBoard(self):
		for i in range(9):
			self.frame.rowconfigure(i, minsize=self.cellHeight)
			self.frame.columnconfigure(i, minsize=self.cellWidth)
			self.frame.propagate(False)
			self.labels.append(list())
			self.zoneTotalLabels.append(list())
			for j in range(9):
				canvas = tk.Canvas(self.frame, width=self.cellWidth, height=self.cellHeight, bg='white')
				canvas.grid(column=j, row=i)
				canvas.propagate(False)

				label = tk.Label(canvas, text='', font=("Arial", 40), bg='white')
				label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

				zoneTotalLabel = tk.Label(canvas, text='', font=("Arial", 12), bg='white')
				zoneTotalLabel.place(relx=0, rely=0, anchor=tk.NW)

				self.labels[i].append(label)
				self.zoneTotalLabels[i].append(zoneTotalLabel)

	def loadZoneTotals(self):
		for z in self.board.zones:
			topLeftMost = z.topLeftMostCell()
			self.zoneTotalLabels[topLeftMost.y][topLeftMost.x].config(text=str(z.total()))
			for c in z.cells:
				self.drawCellBorders(z, c)

	def markSingleCellZones(self):
		for z in self.board.zones:
			if len(z.cells) == 1:
				self.markCell(z.cells[0], z.cells[0].value)

	# Fills in notes for zones that have only one possible combination
	def loadAutoZoneNotes(self):
		# (zone total, zone size, note string)
		singleCombinationZones = [(3, 2, '12'), (4, 2, '13'), (16, 2, '79'), (17, 2, '89'), (6, 3, '123'), (7, 3, '124'), (23, 3, '689'), (24, 3, '789'), (10, 4, '1234'), (11, 4, '1235'), (29, 4, '5789'), (30, 4, '6789'), (15, 5, '12345'), (16, 5, '12346'), (34, 5, '46789'), (35, 5, '56789')]
		for z in self.board.zones:
			zoneTotal = z.total()
			zoneLength = len(z.cells)
			result = [x for x in singleCombinationZones if (x[0] == zoneTotal and x[1] == zoneLength)]
			if len(result) > 0:
				for c in z.cells:
					self.labels[c.y][c.x].config(text=result[0][2], font=("Arial", 16), fg='gray')

	def selectCell(self, x, y):
		if self.selectedCell != None:
			if self.labels[self.selectedCell.y][self.selectedCell.x].cget('bg') != 'red':
				self.setCellColor(self.selectedCell.x, self.selectedCell.y, 'white')

		self.selectedCell = self.board.get(x, y)

		if self.labels[self.selectedCell.y][self.selectedCell.x].cget('bg') != 'red':
			self.setCellColor(x, y, 'cyan')

	def setCellColor(self, x, y, color):
		self.labels[y][x].config(bg=color)
		self.labels[y][x].master.config(bg=color)
		self.zoneTotalLabels[y][x].config(bg=color)

	def drawZoneLine(self, x, y, direction):
		canvas = self.labels[y][x].master
		if direction == 'top':
			canvas.create_line(0, 5, 100, 5, dash=(3, 1), tags='border')
		elif direction == 'right':
			canvas.create_line(95, 0, 95, 100, dash=(3, 1), tags='border')
		elif direction == 'bottom':
			canvas.create_line(0, 95, 100, 95, dash=(3, 1), tags='border')
		elif direction == 'left':
			canvas.create_line(5, 0, 5, 100, dash=(3, 1), tags='border')

	def drawCellBorders(self, zone, cell):
		neighbor = self.board.cellLeft(cell)
		if (neighbor == None) or (not zone.contains(neighbor)):
			self.drawZoneLine(cell.x, cell.y, 'left')

		neighbor = self.board.cellAbove(cell)
		if (neighbor == None) or (not zone.contains(neighbor)):
			self.drawZoneLine(cell.x, cell.y, 'top')

		neighbor = self.board.cellRight(cell)
		if (neighbor == None) or (not zone.contains(neighbor)):
			self.drawZoneLine(cell.x, cell.y, 'right')

		neighbor = self.board.cellBelow(cell)
		if (neighbor == None) or (not zone.contains(neighbor)):
			self.drawZoneLine(cell.x, cell.y, 'bottom')

	def getNoteString(self, oldNote, number):
		numStr = str(number)
		if numStr == '0':
			return ''
		elif len(oldNote) == 0:
			return numStr
		elif numStr in oldNote:
			return oldNote.replace(numStr, '')
		else:
			liststr = list(oldNote)
			length = len(liststr)
			insertIndex = self.noteInsertionIndex(liststr, number)

			if insertIndex < length:
				liststr.insert(insertIndex, numStr)
				return ''.join(liststr)
			else:
				return oldNote + numStr

	def noteInsertionIndex(self, liststr, number):
		length = len(liststr)
		insertIndex = 0
		for i in range(length):
			if int(liststr[i]) > number:
				return i
		return length

	def numKeyPressed(self, number):
		if self.selectedCell == None:
			return

		if not self.noteMode:
			self.markCell(self.selectedCell, number)

		else:
			self.setCellColor(self.selectedCell.x, self.selectedCell.y, 'cyan')
			label = self.labels[self.selectedCell.y][self.selectedCell.x]
			oldNote = ''
			if label.cget("fg") == 'gray':
				oldNote =  label.cget("text")
			noteString = self.getNoteString(oldNote, number)
			label.config(text=noteString, font=("Arial", 16), fg='gray')
			self.userBoard.board[self.selectedCell.y][self.selectedCell.x].value = 0

	def markCell(self, cell, number):
		x = cell.x
		y = cell.y

		self.labels[y][x].config(text=str(number), font=("Arial", 40), fg='black')
		self.userBoard.board[y][x].value = number
		# print(f"number: {number}")

		cellValidity = self.userBoard.isCellValid(self.userBoard.get(x, y))
		zoneValidity = self.checkCellAgainstZone(cell)

		if cellValidity and zoneValidity:
			self.clearNumberFromNotes(self.userBoard.board[y][x])
			if self.labels[y][x].cget('bg') == 'red':
				self.setCellColor(x, y, 'cyan')

			if self.userBoard.isFull() and self.userBoard.checkSolution():
				# print('CONGRATULATIONS!')
				for i in range(self.CARDINALITY):
					for j in range(self.CARDINALITY):
						self.setCellColor(i, j, 'green')

		else:
			self.setCellColor(x, y, 'red')

	# Check if the solution's zone total has been exceeded by the value entered by the user. Used for highlighting an error to the user
	def checkCellAgainstZone(self, cell):
		solutionZone = self.board.getZoneOfCell(cell)
		userTotal = 0
		for cell in solutionZone.cells:
			userTotal += self.userBoard.get(cell.x, cell.y).value

		return userTotal <= solutionZone.total()

	def arrowKeyPressed(self, keycode):
		if self.selectedCell == None:
			return

		newCell = None
		if keycode == 37:
			newCell = self.board.cellLeft(self.selectedCell)
		elif keycode == 38:
			newCell = self.board.cellAbove(self.selectedCell)
		elif keycode == 39:
			newCell = self.board.cellRight(self.selectedCell)
		elif keycode == 40:
			newCell = self.board.cellBelow(self.selectedCell)

		if newCell != None:
			self.selectCell(newCell.x, newCell.y)

	def clearNumberFromNotes(self, cell):
		if cell.value == 0:
			return

		for i in range(self.CARDINALITY):
			if i != cell.x and self.userBoard.board[cell.y][i].value == 0:
				oldNote = self.labels[cell.y][i].cget('text')
				# print(oldNote)
				# print(oldNote.replace(str(cell.value), ''))
				self.labels[cell.y][i].config(text=oldNote.replace(str(cell.value), ''))

			if i != cell.y and self.userBoard.board[i][cell.x].value == 0:
				oldNote = self.labels[i][cell.x].cget('text')
				# print(oldNote)
				# print(oldNote.replace(str(cell.value), ''))
				self.labels[i][cell.x].config(text=oldNote.replace(str(cell.value), ''))

		lowerXBound = math.floor(cell.x / 3) * 3
		lowerYBound = math.floor(cell.y / 3) * 3

		for y in range(lowerYBound, lowerYBound+3):
			for x in range(lowerXBound, lowerXBound + 3):
				if (x != cell.x or y != cell.y) and self.userBoard.board[y][x].value == 0:
					oldNote = self.labels[y][x].cget('text')
					# print(oldNote)
					# print(oldNote.replace(str(cell.value), ''))
					self.labels[y][x].config(text=oldNote.replace(str(cell.value), ''))

		containingZone = self.board.getZoneOfCell(cell)
		for c in containingZone.cells:
			if ((c.x != cell.x) or (c.y != cell.y)) and self.userBoard.board[c.y][c.x].value == 0:
				oldNote = self.labels[c.y][c.x].cget('text')
				self.labels[c.y][c.x].config(text=oldNote.replace(str(cell.value), ''))

	# Some boards have multiple valid solutions due to two (or more) aligned cells having the same numbers in alternating positions.
	# This detects those zones (currently only works on a 2x1 zone) and marks one of them to force a unique solution
	def markIdenticalZones(self):
		for z in self.board.zones:
			zLength = len(z.cells)
			firstZCellUser = self.userBoard.get(z.cells[0].x, z.cells[0].y)

			if zLength == 2 and firstZCellUser.value == 0:
				# vertical 2x1, check all cells in z.cells[1] row for same value as z.cells[0]
				if z.cells[0].x == z.cells[1].x:
					for i in range(self.CARDINALITY):
						checkCell = self.board.get(i, z.cells[1].y)
						secondCheckCell = self.board.get(i, z.cells[0].y)
						if (checkCell.value == z.cells[0].value) and (secondCheckCell.value == z.cells[1].value) and (self.board.sameZone(checkCell, secondCheckCell)):
							self.markCell(z.cells[0], z.cells[0].value)
							self.markCell(z.cells[1], z.cells[1].value)

				# horizontal 2x1, check all cells in z.cells[1] column for same value as z.cells[0]
				elif z.cells[0].y == z.cells[1].y:
					for i in range(self.CARDINALITY):
						checkCell = self.board.get(z.cells[1].x, i)
						secondCheckCell = self.board.get(z.cells[0].x, i)
						if (checkCell.value == z.cells[0].value) and (secondCheckCell.value == z.cells[1].value) and (self.board.sameZone(checkCell, secondCheckCell)):
							self.markCell(z.cells[0], z.cells[0].value)
							self.markCell(z.cells[1], z.cells[1].value)