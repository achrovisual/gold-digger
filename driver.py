from grid import Grid
from bfs import BFS
from gbfs import gbfs
import pygame

game = Grid(8)

start = False
while not start:
	for event in pygame.event.get():
		if event.type == pygame.KEYDOWN:
			start = True

smart = BFS(game)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            pygame.quit()