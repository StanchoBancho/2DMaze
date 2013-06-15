import pygame
from World import *

class Drawer:
    SQUARE_SIZE = 10

    def __init__(self, world, screen):
        self.world = world
        self.screen = screen

    def draw(self):
        s = self.SQUARE_SIZE
        world_map = self.world.maze.board
        width = self.world.maze.width
        height = self.world.maze.height
        for i in range(width):
            for j in  range(height):
                if world_map[i][j] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), ( j * s,  i * s, s, s))
                if world_map[i][j] == 2:
                    pygame.draw.rect(self.screen, (255, 0, 0), ( j * s, i * s, s, s))
                if world_map[i][j] == 3:
                    pygame.draw.rect(self.screen, (0, 255, 0), ( j * s, i * s, s, s))
                if world_map[i][j] == -1:
                    pygame.draw.rect(self.screen, (0, 0, 0), ( j * s, i * s, s, s))          
        tr_pos = self.world.treasure.position
        pygame.draw.rect(self.screen, (0, 0, 255), (tr_pos[0]*s, tr_pos[1] * s, s, s))
