import pygame
from pygame.locals import *

from Drawer import *
from GameMenu import *
from World import *
from GameOverMenu import *
from AIPlayerController import AIPlayerController

class Controller:
    GAME_MENU_SCREEN = 0
    PLAYING_GAME = 1
    GAME_OVER_SCREEN = 2
    SHOULD_QUIT = 3

    GAME_MODE_NONE = -1
    GAME_MODE_TRAINING = 0
    GAME_MODE_TWO_PLAYERS = 1
    GAME_MODE_PLAYER_VS_COMPUTER = 2
    
    def __init__(self, resolution, screen):
        self.resolution = resolution
        self.screen = screen
        self.game_state = self.GAME_MENU_SCREEN
        self.game_mode = self.GAME_MODE_NONE
        self.menu = GameMenu(self.screen, resolution)
        self.drawer = Drawer(screen = self.screen)
    
    def handle_events(self):
        if self.game_state == self.SHOULD_QUIT:
            print("User pressed quit.")
            pygame.quit()
            return True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("User asked to quit.")
                pygame.quit()
                return True                    
            if self.game_state == self.GAME_MENU_SCREEN:                                        
                self.menu.handle_event(event)
            if self.game_state == self.GAME_OVER_SCREEN:
                self.game_over_menu.handle_event(event)
            if event.type == KEYDOWN:
                if pygame.key.get_pressed()[K_RETURN]:
                    pass                   
        keys = pygame.key.get_pressed()
        if self.game_state == self.GAME_MENU_SCREEN:
            pass 
        if self.game_state == self.PLAYING_GAME:
            #move the player one
            if keys[K_LEFT]:
                self.player_one.move(Player.LEFT)
            if keys[K_RIGHT]:
                self.player_one.move(Player.RIGHT)
            if keys[K_UP]:
                self.player_one.move(Player.DOWN)
            if keys[K_DOWN]:
                self.player_one.move(Player.UP)
            #move the second player
            if self.game_mode == self.GAME_MODE_TWO_PLAYERS:
                if keys[K_a]:
                    self.player_two.move(Player.LEFT)
                if keys[K_d]:
                    self.player_two.move(Player.RIGHT)
                if keys[K_w]:
                    self.player_two.move(Player.DOWN)
                if keys[K_s]:
                     self.player_two.move(Player.UP)
            #move the computer
            if self.game_mode == self.GAME_MODE_PLAYER_VS_COMPUTER:
                self.player_controller.move_player()
        return False
#Check (and change the game state if needed)

    def update_game_status(self):
        if self.game_state == self.GAME_MENU_SCREEN:
            self.check_menu_state()
        elif self.game_state == self.PLAYING_GAME:
            self.check_world_state()
        elif self.game_state == self.GAME_OVER_SCREEN:
            self.check_geme_over_menu_state()

#-check menu status and init a new game if needed
    def check_menu_state(self):
        if self.menu.state == GameMenu.SINGLE_PLAYER:
            self.game_state = self.PLAYING_GAME
            self.init_single_player_game()
            self.menu.state = GameMenu.NO_MODE_CHOSED
        elif self.menu.state == GameMenu.MULTY_PLAYER:
            self.game_state = self.PLAYING_GAME
            self.init_multy_player_game()
            self.menu.state = GameMenu.NO_MODE_CHOSED
        elif self.menu.state == GameMenu.PLAYER_VS_MAC:
            self.game_state = self.PLAYING_GAME
            self.init_player_vs_mac_game()
            self.menu.state = GameMenu.NO_MODE_CHOSED
        

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
        self.game_mode = self.GAME_MODE_TRAINING

    def init_multy_player_game(self):
        self.init_new_world()
        self.player_one = Player(self.world, (0, 1), "Stancho")
        self.world.add_player(self.player_one)
        player_two_coords = (0, self.world.height - 2)
        self.player_two = Player(self.world, player_two_coords, "Dobby")
        self.world.add_player(self.player_two)
        tresure_coords = (self.world.width - 1, int(self.world.height/2))
#        tresure_coords = (1, 2)
        self.world.add_treasure(Treasure(self.world, tresure_coords))
        self.game_mode = self.GAME_MODE_TWO_PLAYERS

    def init_player_vs_mac_game(self):
        self.init_new_world()

        tresure_coords = (self.world.width - 2, int(self.world.height / 2))
        self.world.add_treasure(Treasure(self.world, tresure_coords))

        self.player_one = Player(self.world, (0, 1), "Stancho")
        self.world.add_player(self.player_one)

        self.player_two = Player(self.world, (0, self.world.height - 2), "PC")
        self.world.add_player(self.player_two)
        self.player_controller = AIPlayerController(self.world, self.player_two, tresure_coords)
    
        self.game_mode = self.GAME_MODE_PLAYER_VS_COMPUTER

#-check game status and show game over screen if needed
    def check_world_state(self):
        is_treasure_reached = self.world.is_treasure_reached()
        if is_treasure_reached:
            self.game_state = self.GAME_OVER_SCREEN                       
            self.init_game_over_screen()
            
    def init_game_over_screen(self):
        winner_name = self.world.winner.name
        self.game_over_menu = GameOverMenu(self.resolution, winner_name)

#-check game over menu status and start new game of quit
    def check_geme_over_menu_state(self):
        if self.game_over_menu.state == GameOverMenu.NEW_GAME:
            self.game_state = self.GAME_MENU_SCREEN
        elif self.game_over_menu.state == GameOverMenu.QUIT:
            self.game_state = self.SHOULD_QUIT
             
#Ask the drawer to draw the required part of the game 

    def draw(self):
        if self.game_state == self.GAME_MENU_SCREEN:
            self.drawer.draw_game_menu(self.menu)
        elif self.game_state == self.PLAYING_GAME:
            self.drawer.draw_maze(self.world)
        elif self.game_state == self.GAME_OVER_SCREEN:
            self.drawer.draw_game_over_menu(self.game_over_menu)
           
        
