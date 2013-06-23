import pygame
from World import *
import GameMenu
import GameOverMenu
import pygbutton
import os, sys
from AnimatedSprite import AnimatedSprite

class Drawer:
    # Define some colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = ( 255, 0, 0)
    SQUARE_SIZE = 20
    X_OFFSET = 10
    Y_OFFSET = 10
    
    def __init__(self, screen):
        self.screen = screen
        self.players = {}

    def init_players_sprite(self, players):
        for player in players:
            player_one_images_right = self.load_sliced_sprites(20, 20, "player_one_sprite_right.png")
            player_one_images_left = self.load_sliced_sprites(20, 20, "player_one_sprite_left.png")
            player_sprite = AnimatedSprite(player_one_images_left, player_one_images_right) 
            player_sprite.is_direction_left = 1
            self.players[player.name] = player_sprite
        
    def draw_maze(self, world):
        s = self.SQUARE_SIZE
        world_map = world.maze.board
        width = world.maze.width
        height = world.maze.height
        for i in range(width):
            for j in  range(height):
                square_rect = ( j * s + self.X_OFFSET,  i * s + self.Y_OFFSET, s, s)
                if world_map[i][j] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), square_rect)
                
        for player in world.players:
            self.draw_player(player)
        self.draw_treasure(world.treasure)
        
    def draw_treasure(self, treasure):
        tr_pos = treasure.position
        s = self.SQUARE_SIZE
        treasure_rect = (tr_pos[1]*s + self.X_OFFSET, tr_pos[0]*s + self.Y_OFFSET, s, s)
        treasure_surface = Drawer.load_image("chest_gold.png")[0]
        self.screen.blit(treasure_surface, treasure_rect)        
        
    def draw_player(self, player):
        sprite = self.players[player.name]
        if player.direction == Player.LEFT:
            sprite.is_direction_left = True
        if player.direction == Player.RIGHT:
            sprite.is_direction_left = False
        sprite.is_moving = player.is_moving
        sprite.update(pygame.time.get_ticks())
        s = self.SQUARE_SIZE
        square_rect = (player.position[1] * s + self.X_OFFSET, player.position[0] * s + self.Y_OFFSET, s, s)
        self.screen.blit(sprite.image, square_rect)
        
    
    def draw_game_menu(self, game_menu):
        r = game_menu.resolution
        background_surface = Drawer.load_image("maze_background.png")[0]
        scaled_surface = pygame.transform.scale(background_surface, r)
        self.screen.blit(scaled_surface, (0, 0))
        m_size = game_menu.MENU_SIZE
        menu_frame = (game_menu.origin[0], game_menu.origin[1], m_size, m_size)
        pygame.draw.rect(self.screen, (232, 232, 232), menu_frame)

        game_name_font = pygame.font.SysFont("monospace", 44)
        game_name_label = game_name_font.render("Pathfinder", 1, (0,0,0))
        game_name_title_origin = (game_menu.origin[0] + 60, game_menu.origin[1])
        self.screen.blit(game_name_label, game_name_title_origin)


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
 
    def load_sliced_sprites(self, w, h, filename):
        '''
        Specs :
        	Master can be any height.
        	Sprites frames width must be the same width
        	Master width must be len(frames)*frame.width
        Assuming you ressources directory is named "ressources"
        '''
        images = []
        master_image = pygame.image.load(os.path.join('data', filename)).convert_alpha()
    
        master_width, master_height = master_image.get_size()
        for i in range(int(master_width/w)):
            images.append(master_image.subsurface((i*w,0,w,h)))
        return images


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
