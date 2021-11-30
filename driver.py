from grid import Grid
from bfs import BFS
from gbfs import gbfs
import pygame

game = Grid(8)

start = False
while not start:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
			start = True

# random = BFS(game)
smart = gbfs(game)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            pygame.quit()