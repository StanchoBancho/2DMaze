import pygame
import random
from time import time

class World:

    def __init__(self, size):

        self.maze = Maze(size)
        self.maze.make_random_puzzle()
        
    def draw(self, screen):
        self.maze.draw(screen)              

class Maze:

    def __init__(self, size):
        self.height = size[0]
        self.width = size[1]
        #-1 - unknown
        #0  - empty
        #1  - black
        #2  - first player
        #3  - second player
        self.board = [[0 for j in range(self.height)] for i in range(self.width)]
        self.possible_moves = []

    def link(self, chosen_square):
        i = chosen_square[0]
        j = chosen_square[1]
        links=[]
        if i >= 3:
            if self.board[i - 2][j] == -1:
                self.board[i - 2][j] = 7
                self.possible_moves.append((i - 2, j))
            elif self.board[i - 2][j] == 0:
                links.append((i - 1, j))
                
        if j + 3 <= self.height:
            if self.board[i][j + 2] == -1:
                self.board[i][j + 2] = 7
                self.possible_moves.append((i, j + 2))
            elif self.board[i][j + 2] == 0:
                links.append((i , j + 1))

        if j >= 3:
            if self.board[i][j - 2] == -1:
                self.board[i][j - 2] = 7
                self.possible_moves.append((i , j - 2))
            elif self.board[i][j - 2] == 0:
                links.append((i , j - 1))

        if i + 3 <= self.width:
            if self.board[i + 2][j] == -1:
                self.board[i + 2][j] = 7
                self.possible_moves.append((i + 2, j));
            elif self.board[i + 2][j] == 0:
                links.append((i + 1 , j))

        if len(links) > 0:
            chosed_link = links[random.randrange(0, len(links))]
            self.board[chosed_link[0]][chosed_link[1]] = 0
            if chosed_link in self.possible_moves:
                self.possible_moves.remove(chosed_link);
	    
    def make_random_puzzle(self):
        #make the grid
        for i in range(self.width):
            for j in  range(self.height):
                 self.board[i][j] = 1
        for i in range(1, self.width - 1):
            for j in range(1, self.height -1):
                if i%2 == 1 or j % 2 == 1:
                    self.board[i][j] = 1
                if (i + j) % 2 == 1:
                    self.board[i][j] = 1
        for i in range(1, self.width, 2):
            for j in range(1, self.height, 2):
                self.board[i][j] = -1
               
        #make the puzzle
        self.possible_moves = [(1, 1)]
        self.board[1][1] = 1
        self.board[0][1] = 0
        random.seed()
        while len(self.possible_moves) > 0:   
            chosen_square = self.possible_moves[random.randrange(0, len(self.possible_moves))]
            self.board[chosen_square[0]][chosen_square[1]] = 0
            self.possible_moves.remove(chosen_square)
            self.link(chosen_square)
        
        
    def draw(self, screen):
        for i in range(self.width):
            for j in  range(self.height):
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, (0, 0, 0), ( j * 5,  i * 5, 5, 5))
                if self.board[i][j] == -1:
                    pygame.draw.rect(screen, (0, 255, 0), ( j * 5, i * 5, 5, 5))
