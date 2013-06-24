import pygame
import random

from time import time

class World:
    treasure = None
    is_treasure_reached_once = False
    winner = None
    
    def __init__(self, size):
        self.width = size[0]
        self.height = size[1]
        self.maze = Maze(size)
        self.maze.make_random_puzzle()
        self.players = []

    def add_player(self, player):
        self.players.append(player)
        self.maze.board[player.position[0]][player.position[1]] = 1 + len(self.players)
        player.pid = len(self.players)

    def add_treasure(self, treasure):
        self.treasure = treasure
        self.maze.board[treasure.position[0]][treasure.position[1]] = 0

    def is_treasure_reached(self):
        if self.is_treasure_reached_once:
            return True
        for player in self.players:
            if player.position == self.treasure.position:
                self.is_treasure_reached_once = True
                self.winner = player
                return True
        return False
    
    def is_position_free(self, position):
        is_position_in_maze_widht = position[0] > 0 and position[0] < self.maze.size[0]
        is_position_in_maze_height = position[1] > 0 and position[1] < self.maze.size[1] 
        if not (is_position_in_maze_widht and is_position_in_maze_height):
            return False
        position_value = self.maze.board[position[0]][position[1]]
        is_position_free = position_value != 1
        return is_position_free

    def move_player_to_position(self, player, position):
        is_position_free = self.is_position_free(position)
        if is_position_free:
            self.maze.board[player.position[0]][player.position[1]] = 0
            self.maze.board[position[0]][position[1]] = player.pid
            player.position = position
            return True
        return False
        
class Maze:

    def __init__(self, size):
        self.size = size
        self.height = size[1]
        self.width = size[0]
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
        #make the world black
        for i in range(self.width):
            for j in  range(self.height):
                 self.board[i][j] = 1

        #make the grid
        for i in range(1, self.width, 2):
            for j in range(1, self.height, 2):
                self.board[i][j] = -1
        
        #make the puzzle
        self.possible_moves = [(1, 1)]
        self.board[1][1] = 1
        self.board[0][1] = 0
        self.board[0][self.height-2] = 0
        random.seed()
        while len(self.possible_moves) > 0:   
            chosen_square = self.possible_moves[random.randrange(0, len(self.possible_moves))]
            self.board[chosen_square[0]][chosen_square[1]] = 0
            self.possible_moves.remove(chosen_square)
            self.link(chosen_square)


class Player:
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (1, 0)
    DOWN = (-1, 0)
    POSIBLE_DIRECTIONS = [LEFT, RIGHT, UP, DOWN]
    
    def __init__(self, world, position, name):
        self.world = world
        self.prev_position = position
        self.position = position
        self.is_moving = False
        self.name = name
        self.pid = 0
        self.direction = Player.DOWN

    def move(self, direction):
        next_prev_pos = self.position
        self.direction = direction
        new_position = (self.position[0] + direction[0], self.position[1] + direction[1])
        if self.world.move_player_to_position(self, new_position):
            self.prev_position = next_prev_pos

    def move_to_position(self, new_position):
        next_prev_pos = self.position
        for direction in self.POSIBLE_DIRECTIONS:
            x_cond = self.position[0] + direction[0] == new_position[0]
            y_cond = self.position[1] + direction[1] == new_position[1]
            if x_cond and y_cond:
                self.direction = direction              
        if self.world.move_player_to_position(self, new_position):
            self.prev_position = next_prev_pos            
        
class Treasure:
    def __init__(self, world, position):
        self.world = world
        self.position = position
