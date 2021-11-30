from object import Object
from miner import Miner
import random, sys, pygame

# PYGAME WINDOW SIZE
windowSize = width,height = 800,800
# COLORS
WHITE = (255, 255, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (200, 200, 200)

class Grid():
	def __init__(self, size):
		# Initialize grid
		self.size = size
		self.screen = pygame.display.set_mode(windowSize)
		pygame.display.set_caption("Gold Miner")
		pygame.init()
		self.grid = [["Empty" for i in range(self.size)] for i in range(self.size)]
		# Initialize objects
		numGold = 1
		numPits = int(self.size * 0.25)
		numBeacons = 1 if (self.size * 0.10) < 1 else int(self.size * 0.10)
		numCount = 0

		# MINER
		self.miner = Miner("Miner", {"x": 0, "y": 0}, self.size)
		self.update_grid(self.miner)

		# GOLD
		while numCount < numGold:
			x = random.randint(0, self.size-1)
			y = random.randint(0, self.size-1)
			gold = Object("Gold", {"x": x, "y": y})
			if self.grid[y][x] == "Empty":
				self.update_grid(gold)
				numCount += 1
			print(gold.coordinates)
		numCount = 0

		# BEACONS
		while numCount < numBeacons:
			x = random.randint(0, self.size-1)
			y = random.randint(0, self.size-1)
			beacon = Object("Beacon", {"x": x, "y": y})
			if self.grid[y][x] == "Empty":
				self.update_grid(beacon)
				numCount += 1
			print(beacon.coordinates)
		numCount = 0

		# PITS
		while numCount < numPits:
			x = random.randint(0, self.size-1)
			y = random.randint(0, self.size-1)
			pit = Object("Pit", {"x": x, "y": y})
			if self.grid[y][x] == "Empty":
				self.update_grid(pit)
				numCount += 1
			print(pit.coordinates)

		self.draw_grid()
		pygame.display.update()

	def update_grid(self, object):
		x = object.coordinates.get("x")
		y = object.coordinates.get("y")

		self.grid[x][y] = object.name[0]

	def draw_grid(self):
		tileSize = width // self.size
		self.screen.fill(LIGHTGREY)

		for i in range(self.size):
			pygame.draw.line(self.screen, DARKGREY, (0, i * tileSize), (width, i * tileSize))
			for j in range(self.size):
				pygame.draw.line(self.screen, DARKGREY, (j * tileSize, 0), (j * tileSize, width))
				x = i * tileSize
				y = j * tileSize

				if self.grid[i][j] == 'P': # Pit
					# pygame.draw.rect(self.screen, RED, [x+3, y+3, tileSize-3, tileSize-3])
					gold_img = pygame.image.load("./icons/manhole.png")
					gold_img = pygame.transform.scale(gold_img, (tileSize, tileSize))
					self.screen.blit(gold_img, (x, y))
				elif self.grid[i][j] == 'B': # Beacon
					# pygame.draw.rect(self.screen, GREEN, [x+3, y+3, tileSize-3, tileSize-3])
					gold_img = pygame.image.load("./icons/lighthouse.png")
					gold_img = pygame.transform.scale(gold_img, (tileSize, tileSize))
					self.screen.blit(gold_img, (x, y))
				elif self.grid[i][j] == 'G': # Gold
					# pygame.draw.rect(self.screen, YELLOW, [x+3, y+3, tileSize-3, tileSize-3])
					gold_img = pygame.image.load("./icons/gold.png")
					gold_img = pygame.transform.scale(gold_img, (tileSize, tileSize))
					self.screen.blit(gold_img, (x, y))
				# else: # Empty
				# 	pygame.draw.rect(self.screen, BLACK, [x+3, y+3, tileSize-3, tileSize-3])

		# Draw Miner position
		gold_img = None
		if self.miner.compass == 'north':
			gold_img = pygame.image.load("./icons/minerN.png")
		elif self.miner.compass == 'east':
			gold_img = pygame.image.load("./icons/minerE.png")
		elif self.miner.compass == 'south':
			gold_img = pygame.image.load("./icons/minerS.png")
		elif self.miner.compass == 'west':
			gold_img = pygame.image.load("./icons/minerW.png")
		gold_img = pygame.transform.scale(gold_img, (tileSize, tileSize))
		self.screen.blit(gold_img, (self.miner.coordinates.get('y')*tileSize, self.miner.coordinates.get('x')*tileSize))

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
			iterator = int(miner_location['x'])
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
			iterator = int(miner_location['x'])
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
			iterator = int(miner_location['y'])
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
			iterator = int(miner_location['y'])
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
			return return_value

		return return_value



	def show_grid(self):
		# Update the grid
		self.draw_grid()
		pygame.display.update()
