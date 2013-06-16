import pygame
from World import *
import GameMenu
import GameOverMenu
import pygbutton
import os, sys

class Drawer:
    # Define some colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = ( 255, 0, 0)
    SQUARE_SIZE = 10
    game_menu = None
    
    def __init__(self, screen):
        self.screen = screen

    def draw_maze(self, world):
        s = self.SQUARE_SIZE
        world_map = world.maze.board
        width = world.maze.width
        height = world.maze.height
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
        tr_pos = world.treasure.position
        pygame.draw.rect(self.screen, (0, 0, 255), (tr_pos[1]*s, tr_pos[0]*s, s, s))


    def draw_game_menu(self, game_menu):
        r = game_menu.resolution
        background_surface = Drawer.load_image("maze_background.png")[0]
        scaled_surface = pygame.transform.scale(background_surface, r)
        self.screen.blit(scaled_surface, (0, 0))
        menu_frame = (game_menu.origin[0], game_menu.origin[1], 256, 256)
        pygame.draw.rect(self.screen, (232, 232, 232), menu_frame)
        for b in game_menu.all_buttons:
            b.draw(self.screen)
        
    def draw_game_over_menu(self, game_over_menu):
        r = game_over_menu.resolution
        game_over_menu_frame = (game_over_menu.origin[0], game_over_menu.origin[1], 256, 256)
        pygame.draw.rect(self.screen, (232, 232, 232), game_over_menu_frame)

        game_over_font = pygame.font.SysFont("monospace", 44)
        game_over_label = game_over_font.render("Game Over", 1, (0,0,0))
        game_over_title_origin = (game_over_menu.origin[0] + 10, game_over_menu.origin[1])
        self.screen.blit(game_over_label, game_over_title_origin)

        detail_font = pygame.font.SysFont("monospace", 26)
        detail_text_one = "Congratulations,"
        detail_label_one = detail_font.render(detail_text_one, 1, (0,0,0))
        detail_title_origin = (game_over_menu.origin[0] + 2, game_over_menu.origin[1] + 50)
        self.screen.blit(detail_label_one, detail_title_origin)

        detail_text_two = "{0} you win!".format(game_over_menu.winner_name)
        detail_label_two = detail_font.render(detail_text_two, 1, (0,0,0))
        detail_title_two_origin = (game_over_menu.origin[0] + 2, game_over_menu.origin[1] + 80)
        self.screen.blit(detail_label_two, detail_title_two_origin)
 

        for b in game_over_menu.all_buttons:
            b.draw(self.screen)
 
    def load_image(name, colorkey=None):
        fullname = os.path.join('data', name)
        try:
            image = pygame.image.load(fullname)
        except (pygame.error, message):
            print("Cannot load image:", name)
            raise (SystemExit, message)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()

    def load_sound(name):
        class NoneSound:
            def play(self): pass
        if not pygame.mixer:
            return NoneSound()
        fullname = os.path.join('data', name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except (pygame.error, message):
            print("Cannot load sound:", wav)
        raise (SystemExit, message)
        return sound
