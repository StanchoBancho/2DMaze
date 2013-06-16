import pygame
from pygame.locals import *

from Drawer import *
from GameMenu import *
from World import *
from GameOverMenu import *

class Controller:
    GAME_MENU_SCREEN = 0
    PLAYING_GAME = 1
    GAME_OVER_SCREEN = 2

    def __init__(self, resolution, screen):
        self.resolution = resolution
        self.screen = screen
        self.game_state = self.GAME_MENU_SCREEN
        self.menu = GameMenu(self.screen, resolution)
        self.drawer = Drawer(screen = self.screen)

    def handle_events(self):
        #handle the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("User asked to quit.")
                pygame.quit()
                return True                    
            if self.game_state == self.GAME_MENU_SCREEN:                                        
                self.menu.handle_event(event)
            if event.type == KEYDOWN:
                if pygame.key.get_pressed()[K_RETURN]:
                    pass
                    
        keys = pygame.key.get_pressed()
        if self.game_state == self.GAME_MENU_SCREEN:
            pass 
        if self.game_state == self.PLAYING_GAME:
            if keys[K_LEFT]:
                self.player_one.move(Player.LEFT)
            if keys[K_RIGHT]:
                self.player_one.move(Player.RIGHT)
            if keys[K_UP]:
                self.player_one.move(Player.DOWN)
            if keys[K_DOWN]:
                self.player_one.move(Player.UP)
            if self.player_two:
                if keys[K_a]:
                    self.player_two.move(Player.LEFT)
                if keys[K_d]:
                    self.player_two.move(Player.RIGHT)
                if keys[K_w]:
                    self.player_two.move(Player.DOWN)
                if keys[K_s]:
                     self.player_two.move(Player.UP)        
        return False
#Check (and change the game state if needed)

    def update_game_status(self):
        if self.game_state == self.GAME_MENU_SCREEN:
            self.check_menu_state()
        elif self.game_state == self.PLAYING_GAME:
            self.check_game_state()
        elif self.game_state == self.GAME_OVER_SCREEN:
            pass

#-check menu status and init a new game if needed
    def check_menu_state(self):
        if self.menu.state == GameMenu.SINGLE_PLAYER:
            self.game_state = self.PLAYING_GAME
            self.init_single_player_game()
        elif self.menu.state == GameMenu.MULTY_PLAYER:
            self.game_state = self.PLAYING_GAME
            self.init_multy_player_game()
        elif self.menu.state == GameMenu.PLAYER_VS_MAC:
            self.game_state = self.PLAYING_GAME
            self.init_player_vs_mac_game()

    def init_new_world(self):
        world_height = int(self.resolution[0] / Drawer.SQUARE_SIZE) - 1 
        world_width = int(self.resolution[1] / Drawer.SQUARE_SIZE) - 1
        self.world = World((world_width, world_height))
        
    def init_single_player_game(self):
        self.init_new_world()
        self.player_one = Player(self.world, (0, 1), "Stancho")
        self.world.add_player(self.player_one)
        self.player_two = None
        tresure_coords = (self.world.width - 1, int(self.world.height/2))
        self.world.add_treasure(Treasure(self.world, tresure_coords))

    def init_multy_player_game(self):
        self.init_new_world()
        self.player_one = Player(self.world, (0, 1), "Stancho")
        self.world.add_player(self.player_one)
        player_two_coords = (0, self.world.height - 2)
        self.player_two = Player(self.world, player_two_coords, "Dobby")
        self.world.add_player(self.player_two)
        tresure_coords = (self.world.width - 1, int(self.world.height/2))
        self.world.add_treasure(Treasure(self.world, tresure_coords))

    def init_player_vs_mac_game(self):
        self.init_new_world()
        self.player_one = Player(self.world, (0, 1), "Stancho")
        self.player_two = Player(self.world, (0, 1), "PC")
        self.world.add_player(self.player_one)
        self.world.add_player(self.player_two)
        tresure_coords = (self.world.width - 2, int(self.world.height / 2))
        self.world.add_treasure(Treasure(self.world, tresure_coords))

#-check game status and show game over screen if needed
    def check_game_state(self):
        if self.world.is_treasure_reached():
            self.game_state == self.GAME_OVER_SCREEN                       

    def init_game_over_screen(self):
        winner_name = self.world.winner.name
        self.game_over_menu = GameOverMenu(self.resolution, winner_name)

#-check game over menu status and start new game of quit
    
       
#Ask the drawer to draw the required part of the game 

    def draw(self):
        if self.game_state == self.GAME_MENU_SCREEN:
            self.drawer.draw_game_menu(self.menu)
        elif self.game_state == self.PLAYING_GAME:
            self.drawer.draw_maze(self.world)
        elif self.game.state == self.GAME_OVER_SCREEN:
            self.drawer.draw_game_over_menu(self.game_over_menu)
           
        
