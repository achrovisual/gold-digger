from grid import Grid
from bfs import BFS
from gbfs import gbfs
import pygame

game = Grid()

if game.algo == 0:
	random = BFS(game)
elif game.algo == 1:
	smart = gbfs(game)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            pygame.quit()