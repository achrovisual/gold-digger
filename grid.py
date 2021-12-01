from object import Object
from miner import Miner
import random, sys, pygame
import time
# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (200, 200, 200)
RED = (255, 90, 90)

class Grid():
	def __init__(self):
		pygame.init()
		# Prepare pygame window size
		pygameInfo = pygame.display.Info()
		self.screenSize = (min(pygameInfo.current_w, pygameInfo.current_h) - 200)
		self.screen = pygame.display.set_mode((self.screenSize, self.screenSize+50))
		pygame.display.set_caption("Gold Miner")

		# Configurations
		self.solving = 0 # 0 - Idle, 1 - Solving, 2 - Finished
		self.size = -1 # grid size
		self.algo = -1 # 0 - random, 1 - smart
		self.step = -1 # 0 - step-by-step (per keypress), 1 - fast forward (every x seconds)
		self.place = -1 # 0 - random, 1 - manual placement, 2 - done
		self.configGridSize()
		self.configAlgorithm()
		self.configSteps()
		# Initialize grid
		self.grid = [["Empty" for i in range(self.size)] for i in range(self.size)]

		# MINER
		self.miner = Miner("Miner", {"x": 0, "y": 0}, self.size)
		self.update_grid(self.miner)
		
		self.configObjects()
		while self.place != 2:
			continue # wait for objects to be placed
		self.draw_grid()
		pygame.display.update()
		while not self.solving:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
					self.solving = 1
				if event.type == pygame.QUIT:
					pygame.quit()

	def update_grid(self, object):
		x = object.coordinates.get("x")
		y = object.coordinates.get("y")

		self.grid[y][x] = object.name[0]

	def draw_grid(self):
		font = pygame.freetype.SysFont('Montserrat', 40)
		tileSize = self.screenSize // self.size
		self.screen.fill(LIGHTGREY)

		for i in range(self.size):
			pygame.draw.line(self.screen, DARKGREY, (0, i * tileSize), (self.screenSize, i * tileSize))
			for j in range(self.size):
				pygame.draw.line(self.screen, DARKGREY, (j * tileSize, 0), (j * tileSize, self.screenSize))
				y = i * tileSize
				x = j * tileSize

				if self.grid[i][j] == 'P': # Pit
					# pygame.draw.rect(self.screen, RED, [x+3, y+3, tileSize-3, tileSize-3])
					pit_img = pygame.image.load("./icons/manhole.png")
					pit_img = pygame.transform.scale(pit_img, (tileSize, tileSize))
					self.screen.blit(pit_img, (x, y))
				elif self.grid[i][j] == 'B': # Beacon
					# pygame.draw.rect(self.screen, GREEN, [x+3, y+3, tileSize-3, tileSize-3])
					beacon_img = pygame.image.load("./icons/lighthouse.png")
					beacon_img = pygame.transform.scale(beacon_img, (tileSize, tileSize))
					self.screen.blit(beacon_img, (x, y))
				elif self.grid[i][j] == 'G': # Gold
					# pygame.draw.rect(self.screen, YELLOW, [x+3, y+3, tileSize-3, tileSize-3])
					gold_img = pygame.image.load("./icons/gold.png")
					gold_img = pygame.transform.scale(gold_img, (tileSize, tileSize))
					self.screen.blit(gold_img, (x, y))
				# else: # Empty
				# 	pygame.draw.rect(self.screen, BLACK, [x+3, y+3, tileSize-3, tileSize-3])
		pygame.draw.line(self.screen, DARKGREY, (0, (i+1) * tileSize), (self.screenSize, (i+1) * tileSize))

		# Draw Miner position
		miner_img = None
		if self.miner.compass == 'north':
			miner_img = pygame.image.load("./icons/minerN.png")
		elif self.miner.compass == 'east':
			miner_img = pygame.image.load("./icons/minerE.png")
		elif self.miner.compass == 'south':
			miner_img = pygame.image.load("./icons/minerS.png")
		elif self.miner.compass == 'west':
			miner_img = pygame.image.load("./icons/minerW.png")
		miner_img = pygame.transform.scale(miner_img, (tileSize, tileSize))
		self.screen.blit(miner_img, (self.miner.coordinates.get('x')*tileSize, self.miner.coordinates.get('y')*tileSize))

		dashboardRect = pygame.Rect(0, self.screenSize+15, self.screenSize, 50)
		# Draw action counters
		if self.place == 2:
			actions = "Moves: " +  str(self.miner.actions[0]) + " Rotates: " + str(self.miner.actions[1]) + " Scans: " + str(self.miner.actions[2])
			actionsRect = font.get_rect(actions, size = 24)
			actionsRect.top = dashboardRect.top
			actionsRect.left = dashboardRect.width/2 + 10
			font.render_to(self.screen, actionsRect, actions, DARKGREY, size = 24)

		# Draw dialogue box
		dialogue = "Solving..."
		if self.solving == 0:
			dialogue = "Press spacebar to start"
		if self.step == 0:
			dialogue = "Press any key to show next step"
		if self.place == 1:
			dialogue = "Click a tile to place object (Order is Gold -> Beacon -> Pits)"
		if self.solving == 2:
			if self.grid[self.miner.coordinates.get('y')][self.miner.coordinates.get('x')] == 'P':
				dialogue = "Game over!"
			elif self.grid[self.miner.coordinates.get('y')][self.miner.coordinates.get('x')] == 'G':
				dialogue = "Gold found!"
			elif self.grid[self.miner.coordinates.get('y')][self.miner.coordinates.get('x')] == 'B':
				dialogue = "Beacon found!"
		dialogueRect = font.get_rect(dialogue, size = 24)
		dialogueRect.top = dashboardRect.top
		dialogueRect.left = dashboardRect.left + 10
		font.render_to(self.screen, dialogueRect, dialogue, DARKGREY, size = 24)

	def check(self):
		miner_location = self.miner.coordinates
		x  = int(miner_location['x'])
		y = int(miner_location['y'])

		if x < 0 or x >= self.size or y < 0 or y >= self.size:
			return "out"

		if self.grid[y][x] == 'B':
			return "beacon"
		elif self.grid[y][x] == 'P':
			return "pit"
		elif self.grid[y][x] == 'G':
			return "gold"
		else:
			return "null"

	def scan(self):
		miner_location = self.miner.coordinates
		miner_compass = self.miner.compass
		iterator = 0
		anchor_value = 0
		return_value = ''

		#lateral movement
		if miner_compass == 'east':
			iterator = int(miner_location['x'])+1
			anchor_value = int(miner_location['y'])

			while iterator < self.size and return_value == '':
				if self.grid[anchor_value][iterator] == 'B':
					return_value = 'B'
				elif self.grid[anchor_value][iterator] == 'G':
					return_value = 'G'
				elif self.grid[anchor_value][iterator] == 'P':
					return_value = 'P'
				iterator += 1

		elif miner_compass == 'west':
			iterator = int(miner_location['x'])-1
			anchor_value = int(miner_location['y'])

			while iterator >= 0 and return_value == '':
				if self.grid[anchor_value][iterator] == 'B':
					return_value = 'B'
				elif self.grid[anchor_value][iterator] == 'G':
					return_value = 'G'
				elif self.grid[anchor_value][iterator] == 'P':
					return_value = 'P'
				iterator -= 1

		#longitudinal movement
		elif miner_compass == 'south':
			iterator = int(miner_location['y'])+1
			anchor_value = int(miner_location['x'])

			while iterator < self.size and return_value == '':
				if self.grid[iterator][anchor_value] == 'B':
					return_value = 'B'
				elif self.grid[iterator][anchor_value] == 'G':
					return_value = 'G'
				elif self.grid[iterator][anchor_value] == 'P':
					return_value = 'P'
				iterator += 1

		elif miner_compass == 'north':
			iterator = int(miner_location['y'])-1
			anchor_value = int(miner_location['x'])

			while iterator >= 0 and return_value == '':
				if self.grid[iterator][anchor_value] == 'B':
					return_value = 'B'
				elif self.grid[iterator][anchor_value] == 'G':
					return_value = 'G'
				elif self.grid[iterator][anchor_value] == 'P':
					return_value = 'P'
				iterator -= 1
		else:
			self.miner.scan(return_value)
			return return_value
		self.miner.scan(return_value)
		return return_value

	def show_grid(self):
		# Update the grid
		self.draw_grid()
		pygame.display.update()
		nextStep = False
		while not nextStep:
			if self.step == 0: # Step-by-Step
				for event in pygame.event.get():
					if event.type == pygame.QUIT: # Catch exit button (top-right)
						pygame.quit()
					if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN: # Catch mouse clicks and keyboard press
						nextStep = True
			elif self.step == 1: # Fast forward
				nextStep = True
				time.sleep(0.1)
				for event in pygame.event.get():
					if event.type == pygame.QUIT: # Catch exit button (top-right)
						pygame.quit()
					if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN: # Catch mouse clicks and keyboard press
						break

	def configGridSize(self):
		font = pygame.freetype.SysFont('Montserrat', 40)
		active = True
		infoText = 'Enter grid size (8-64)'
		inputText = ''
		errorText = ''
		inputBox = pygame.Rect(0, 0, 100, 24)
		color = WHITE

		while self.size == -1:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if inputBox.collidepoint(event.pos):
						active = True
						color = WHITE
					else:
						active = False
						color = LIGHTGREY
				if event.type == pygame.KEYDOWN:
					if active:
						if event.key == pygame.K_RETURN:
							if inputText.isnumeric() and (int(inputText) >= 8 and int(inputText) <= 64):
								self.size = int(inputText)
							else:
								errorText = 'Please input a number between 8 and 64 (inclusive) only'
						elif event.key == pygame.K_BACKSPACE:
							inputText = inputText[:-1]
							errorText = ''
						else:
							inputText += event.unicode
				if event.type == pygame.QUIT:
					pygame.quit()

			self.screen.fill(DARKGREY)
			# Instructions
			infoBox = font.get_rect(infoText, size=24)
			infoBox.center = (self.screenSize/2, (self.screenSize/2)-30)
			font.render_to(self.screen, infoBox, infoText, LIGHTGREY, size=24)
			# Input box
			textBox = font.get_rect(inputText, size=24)
			textBox.center = (self.screenSize/2, self.screenSize/2)
			inputBox.center = (self.screenSize/2, self.screenSize/2)
			inputBox.width = max(100, textBox.width)
			pygame.draw.rect(self.screen, color, inputBox)
			font.render_to(self.screen, textBox, inputText, (0,0,0), size=24)
			# Error box
			errorBox = font.get_rect(errorText, size=14)
			errorBox.center = (self.screenSize/2, (self.screenSize/2)+30)
			font.render_to(self.screen, errorBox, errorText, RED, size=14)
			# Update GUI
			pygame.display.update()

	def configAlgorithm(self):
		font = pygame.freetype.SysFont('Montserrat', 40)
		active = True
		infoText = 'Enter agent rationality (random or smart)'
		inputText = ''
		errorText = ''
		inputBox = pygame.Rect(0, 0, 150, 24)
		color = WHITE

		while self.algo == -1:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if inputBox.collidepoint(event.pos):
						active = True
						color = WHITE
					else:
						active = False
						color = LIGHTGREY
				if event.type == pygame.KEYDOWN:
					if active:
						if event.key == pygame.K_RETURN:
							if inputText == 'random':
								self.algo = 0
							elif inputText == 'smart':
								self.algo = 1
							else:
								errorText = 'Please choose between random or smart agent'
						elif event.key == pygame.K_BACKSPACE:
							inputText = inputText[:-1]
							errorText = ''
						else:
							inputText += event.unicode
				if event.type == pygame.QUIT:
					pygame.quit()

			self.screen.fill(DARKGREY)
			# Instructions
			infoBox = font.get_rect(infoText, size=24)
			infoBox.center = (self.screenSize/2, (self.screenSize/2)-30)
			font.render_to(self.screen, infoBox, infoText, LIGHTGREY, size=24)
			# Input box
			textBox = font.get_rect(inputText, size=24)
			textBox.center = (self.screenSize/2, self.screenSize/2)
			inputBox.center = (self.screenSize/2, self.screenSize/2)
			inputBox.width = max(150, textBox.width)
			pygame.draw.rect(self.screen, color, inputBox)
			font.render_to(self.screen, textBox, inputText, (0,0,0), size=24)
			# Error box
			errorBox = font.get_rect(errorText, size=14)
			errorBox.center = (self.screenSize/2, (self.screenSize/2)+30)
			font.render_to(self.screen, errorBox, errorText, RED, size=14)
			# Update GUI
			pygame.display.update()

	def configSteps(self):
		font = pygame.freetype.SysFont('Montserrat', 40)
		active = True
		infoText = 'Enter miner movement speed (step-by-step or fast forward)'
		inputText = ''
		errorText = ''
		inputBox = pygame.Rect(0, 0, 200, 24)
		color = WHITE

		while self.step == -1:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if inputBox.collidepoint(event.pos):
						active = True
						color = WHITE
					else:
						active = False
						color = LIGHTGREY
				if event.type == pygame.KEYDOWN:
					if active:
						if event.key == pygame.K_RETURN:
							if inputText == 'step-by-step':
								self.step = 0
							elif inputText == 'fast forward':
								self.step = 1
							else:
								errorText = 'Please choose between step-by-step or fast forward'
						elif event.key == pygame.K_BACKSPACE:
							inputText = inputText[:-1]
							errorText = ''
						else:
							inputText += event.unicode
				if event.type == pygame.QUIT:
					pygame.quit()

			self.screen.fill(DARKGREY)
			# Instructions
			infoBox = font.get_rect(infoText, size=24)
			infoBox.center = (self.screenSize/2, (self.screenSize/2)-30)
			font.render_to(self.screen, infoBox, infoText, LIGHTGREY, size=24)
			# Input box
			textBox = font.get_rect(inputText, size=24)
			textBox.center = (self.screenSize/2, self.screenSize/2)
			inputBox.center = (self.screenSize/2, self.screenSize/2)
			inputBox.width = max(200, textBox.width)
			pygame.draw.rect(self.screen, color, inputBox)
			font.render_to(self.screen, textBox, inputText, (0,0,0), size=24)
			# Error box
			errorBox = font.get_rect(errorText, size=14)
			errorBox.center = (self.screenSize/2, (self.screenSize/2)+30)
			font.render_to(self.screen, errorBox, errorText, RED, size=14)
			# Update GUI
			pygame.display.update()

	def configObjects(self):
		font = pygame.freetype.SysFont('Montserrat', 40)
		active = True
		infoText = 'Enter object placement preference (manual or random)'
		inputText = ''
		errorText = ''
		inputBox = pygame.Rect(0, 0, 200, 24)
		color = WHITE
		
		while self.place == -1:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					if inputBox.collidepoint(event.pos):
						active = True
						color = WHITE
					else:
						active = False
						color = LIGHTGREY
				if event.type == pygame.KEYDOWN:
					if active:
						if event.key == pygame.K_RETURN:
							if inputText == 'manual':
								self.place = 1
							elif inputText == 'random':
								self.place = 0
							else:
								errorText = 'Please choose between manual or random'
						elif event.key == pygame.K_BACKSPACE:
							inputText = inputText[:-1]
							errorText = ''
						else:
							inputText += event.unicode
				if event.type == pygame.QUIT:
					pygame.quit()
					
			self.screen.fill(DARKGREY)
			# Instructions
			infoBox = font.get_rect(infoText, size=24)
			infoBox.center = (self.screenSize/2, (self.screenSize/2)-30)
			font.render_to(self.screen, infoBox, infoText, LIGHTGREY, size=24)
			# Input box
			textBox = font.get_rect(inputText, size=24)
			textBox.center = (self.screenSize/2, self.screenSize/2)
			inputBox.center = (self.screenSize/2, self.screenSize/2)
			inputBox.width = max(200, textBox.width)
			pygame.draw.rect(self.screen, color, inputBox)
			font.render_to(self.screen, textBox, inputText, (0,0,0), size=24)
			# Error box
			errorBox = font.get_rect(errorText, size=14)
			errorBox.center = (self.screenSize/2, (self.screenSize/2)+30)
			font.render_to(self.screen, errorBox, errorText, RED, size=14)
			# Update GUI
			pygame.display.update()
		
		# Initialize objects
		numGold = 1
		numPits = int(self.size * 0.25)
		numBeacons = 1 if (self.size * 0.10) < 1 else int(self.size * 0.10)
		numCount = 0

		if self.place == 0: # random placement
			# GOLD
			while numCount < numGold:
				x = random.randint(0, self.size-1)
				y = random.randint(0, self.size-1)
				gold = Object("Gold", {"x": x, "y": y})
				if self.grid[y][x] == "Empty":
					self.update_grid(gold)
					numCount += 1
				# print(gold.coordinates)
			numCount = 0

			# BEACONS
			while numCount < numBeacons:
				x = random.randint(0, self.size-1)
				y = random.randint(0, self.size-1)
				beacon = Object("Beacon", {"x": x, "y": y})
				if self.grid[y][x] == "Empty":
					self.update_grid(beacon)
					numCount += 1
				# print(beacon.coordinates)
			numCount = 0

			# PITS
			while numCount < numPits:
				x = random.randint(0, self.size-1)
				y = random.randint(0, self.size-1)
				pit = Object("Pit", {"x": x, "y": y})
				if self.grid[y][x] == "Empty":
					self.update_grid(pit)
					numCount += 1
				# print(pit.coordinates)
			self.place = 2

		elif self.place == 1: # manual placement
			tileSize = self.screenSize // self.size
			# GOLD
			while numCount < numGold:
				self.draw_grid()
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						if self.screen.get_rect().collidepoint(event.pos):
							print(event.pos, tileSize)
							print('(' + str(event.pos[0]//tileSize) + ', ' + str(event.pos[1]//tileSize) + ')')
							x = event.pos[0]//tileSize
							y = event.pos[1]//tileSize
							if self.grid[y][x] == "Empty":
								gold = Object("Gold", {"x": x, "y": y})
								self.update_grid(gold)
								numCount += 1
								print(gold.coordinates)
					if event.type == pygame.KEYDOWN:
						continue
			numCount = 0
			# BEACON
			while numCount < numBeacons:
				self.draw_grid()
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						if self.screen.get_rect().collidepoint(event.pos):
							print(event.pos, tileSize)
							print('(' + str(event.pos[0]//tileSize) + ', ' + str(event.pos[1]//tileSize) + ')')
							x = event.pos[0]//tileSize
							y = event.pos[1]//tileSize
							if self.grid[y][x] == "Empty":
								beacon = Object("Beacon", {"x": x, "y": y})
								self.update_grid(beacon)
								numCount += 1
								print(beacon.coordinates)
					if event.type == pygame.KEYDOWN:
						continue
			numCount = 0
			# PITS
			while numCount < numPits:
				self.draw_grid()
				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						pygame.quit()
					if event.type == pygame.MOUSEBUTTONDOWN:
						if self.screen.get_rect().collidepoint(event.pos):
							print(event.pos, tileSize)
							print('(' + str(event.pos[0]//tileSize) + ', ' + str(event.pos[1]//tileSize) + ')')
							x = event.pos[0]//tileSize
							y = event.pos[1]//tileSize
							if self.grid[y][x] == "Empty":
								pit = Object("Pit", {"x": x, "y": y})
								self.update_grid(pit)
								numCount += 1
								print(pit.coordinates)
					if event.type == pygame.KEYDOWN:
						continue
			self.place = 2
