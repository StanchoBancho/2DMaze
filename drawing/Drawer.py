import pygame
import os
import sys

from core.WorldObjects import *
from GameMenuViewController import *
from AnimatedSprite import AnimatedSprite


class Drawer:
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = (255, 0, 0)
    SQUARE_SIZE = 20
    X_OFFSET = 10
    Y_OFFSET = 10

    def __init__(self, screen):
        self.screen = screen
        self.players = {}

    def init_players_sprite(self, players):
        for player in players:
            right_images_file = "player_{}_sprite_right.png".format(player.pid)
            right_images = self.load_sliced_sprites(20, 20, right_images_file)
            left_images_file = "player_{}_sprite_left.png".format(player.pid)
            left_images = self.load_sliced_sprites(20, 20, left_images_file)
            player_sprite = AnimatedSprite(left_images, right_images)
            player_sprite.is_direction_left = True
            self.players[player.name] = player_sprite

    def draw_world(self, world):
        s = self.SQUARE_SIZE
        world_map = world.maze.board
        width = world.maze.width
        height = world.maze.height
        for i in range(width):
            for j in range(height):
                sqr_rect = (j*s + self.X_OFFSET,  i*s + self.Y_OFFSET, s, s)
                if world_map[i][j] == 1:
                    pygame.draw.rect(self.screen, (0, 0, 0), sqr_rect)
        for player in world.players:
            self.draw_player(player)
        self.draw_treasure(world.treasure)

    def draw_treasure(self, treasure):
        tr_pos = treasure.position
        s = self.SQUARE_SIZE
        treasure_rect = (tr_pos[1]*s + self.X_OFFSET,
                         tr_pos[0]*s + self.Y_OFFSET, s, s)
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
        square_rect = (player.position[1] * s + self.X_OFFSET,
                       player.position[0] * s + self.Y_OFFSET, s, s)
        self.screen.blit(sprite.image, square_rect)

    def draw_game_menu(self, game_menu_vc):
        r = game_menu_vc.resolution
        background_surface = Drawer.load_image("background.png")[0]
        self.screen.blit(background_surface, (0, 0))
        m_size = game_menu_vc.MENU_SIZE
        menu_frame = (game_menu_vc.origin[0], game_menu_vc.origin[1], m_size,
                      m_size)
        pygame.draw.rect(self.screen, (232, 232, 232), menu_frame)
        game_name_font = pygame.font.SysFont("monospace", 44)
        game_name_label = game_name_font.render("Pathfinder", 1, self.black)
        game_name_title_origin = (game_menu_vc.origin[0] + 60,
                                  game_menu_vc.origin[1])
        self.screen.blit(game_name_label, game_name_title_origin)
        for b in game_menu_vc.all_buttons:
            b.draw(self.screen)

    def draw_game_over_menu(self, game_over_menu_vc):
        r = game_over_menu_vc.resolution
        #draw maze background
        background_surface = Drawer.load_image("background.png")[0]
        self.screen.blit(background_surface, (0, 0))
        #draw gray menu frame
        menu_size = game_over_menu_vc.MENU_SIZE
        game_over_menu_frame = (game_over_menu_vc.origin[0],
                                game_over_menu_vc.origin[1], menu_size,
                                menu_size)
        pygame.draw.rect(self.screen, (232, 232, 232),
                         game_over_menu_frame)
        #draw game over label
        game_over_font = pygame.font.SysFont("monospace", 44)
        game_over_label = game_over_font.render("Game Over", 1,
                                                self.black)
        game_over_title_origin = (game_over_menu_vc.origin[0] + 10,
                                  game_over_menu_vc.origin[1])
        self.screen.blit(game_over_label, game_over_title_origin)
        #draw Congratulations label
        detail_font = pygame.font.SysFont("monospace", 26)
        detail_text_one = "Congratulations,"
        detail_label_one = detail_font.render(detail_text_one, 1, self.black)
        detail_title_origin = (game_over_menu_vc.origin[0] + 10,
                               game_over_menu_vc.origin[1] + 50)
        self.screen.blit(detail_label_one, detail_title_origin)
        #draw Player signatures label
        winner_name = game_over_menu_vc.game_over_menu.winner_name
        detail_text_two = "{0} you win!".format(winner_name)
        detail_label_two = detail_font.render(detail_text_two, 1, self.black)
        detail_title_two_origin = (game_over_menu_vc.origin[0] + 10,
                                   game_over_menu_vc.origin[1] + 80)
        self.screen.blit(detail_label_two, detail_title_two_origin)
        #draw button
        for b in game_over_menu_vc.all_buttons:
            b.draw(self.screen)

    def load_sliced_sprites(self, w, h, filename):
        '''
        Specs :Master can be any height.
        Sprites frames width must be the same width
        Master width must be len(frames)*frame.width
        '''
        images = []
        path = os.path.join('images', filename)
        master_image = pygame.image.load(path).convert_alpha()
        master_width, master_height = master_image.get_size()
        for i in range(int(master_width/w)):
            images.append(master_image.subsurface((i*w, 0, w, h)))
        return images

    def load_image(name, colorkey=None):
        fullname = os.path.join('images', name)
        try:
            image = pygame.image.load(fullname)
        except (pygame.error, message):
            print("Cannot load image:", name)
            raise (SystemExit, message)
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
        return image, image.get_rect()
