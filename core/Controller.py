import pygame
from pygame.locals import *

from drawing.Drawer import Drawer
from drawing.GameMenuViewController import *
from drawing.GameOverMenuViewController import *
from sound.SoundPlayer import SoundPlayer
from WorldObjects import *
from AIPlayerController import *

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
        self.main_menu_vc = GameMenuViewController(self.screen, resolution)
        self.menu = self.main_menu_vc.game_menu
        self.drawer = Drawer(screen = self.screen)
        self.sound_player = SoundPlayer()
        
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
                self.main_menu_vc.handle_event(event)
            if self.game_state == self.GAME_OVER_SCREEN:
                self.game_over_menu_vc.handle_event(event)
            if event.type == KEYDOWN:
                if pygame.key.get_pressed()[K_RETURN]:
                    pass                   
        keys = pygame.key.get_pressed()
        if self.game_state == self.GAME_MENU_SCREEN:
            pass 
        if self.game_state == self.PLAYING_GAME:
            self.player_one.is_moving = False
            #move the player one
            if keys[K_LEFT]:
                self.player_one.move(Player.LEFT)
                self.player_one.is_moving = True
            if keys[K_RIGHT]:
                self.player_one.move(Player.RIGHT)
                self.player_one.is_moving = True
            if keys[K_UP]:
                self.player_one.move(Player.DOWN)
                self.player_one.is_moving = True
            if keys[K_DOWN]:
                self.player_one.move(Player.UP)
                self.player_one.is_moving = True
            #move the second player
            if self.game_mode == self.GAME_MODE_TWO_PLAYERS:
                self.player_two.is_moving = False
                if keys[K_a]:
                    self.player_two.move(Player.LEFT)
                    self.player_two.is_moving = True
                if keys[K_d]:
                    self.player_two.move(Player.RIGHT)
                    self.player_two.is_moving = True
                if keys[K_w]:
                    self.player_two.move(Player.DOWN)
                    self.player_two.is_moving = True
                if keys[K_s]:
                     self.player_two.move(Player.UP)
                     self.player_two.is_moving = True
            #move the computer
            if self.game_mode == self.GAME_MODE_PLAYER_VS_COMPUTER:
                self.player_two.is_moving = True
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
            self.init_player_vs_ai_game()
            self.menu.state = GameMenu.NO_MODE_CHOSED
        if self.menu.should_play_sound:
            if not self.sound_player.is_playing:
                self.sound_player.play_theme_music()
        else:
            if self.sound_player.is_playing:
               self.sound_player.stop_playing_music()                
        if self.menu.should_quit:
            self.game_state = self.SHOULD_QUIT

    def init_new_world(self):
        world_height = int(self.resolution[0] / Drawer.SQUARE_SIZE) - 1
        world_width = int(self.resolution[1] / Drawer.SQUARE_SIZE) - 1
        self.world = World((world_width, world_height))
        
    def init_single_player_game(self):
        self.init_new_world()
        self.player_one = Player(self.world, (0, 1), "Stancho")
        self.world.add_player(self.player_one)
        self.player_twadd_playero = None
        self.drawer.init_players_sprite(self.world.players)
        tresure_coords = (self.world.width - 1, int(self.world.height/2))
        self.world.add_treasure(Treasure(self.world, tresure_coords))
        self.game_mode = self.GAME_MODE_TRAINING
    

    def init_multy_player_game(self):
        self.init_new_world()
        self.player_one = Player(self.world, (0, 1), "Player 1")
        self.world.add_player(self.player_one)
        player_two_coords = (0, self.world.height - 2)
        self.player_two = Player(self.world, player_two_coords, "Player 2")
        self.world.add_player(self.player_two)
        self.drawer.init_players_sprite(self.world.players)
        tresure_coords = (self.world.width - 1, int(self.world.height/2))
        self.world.add_treasure(Treasure(self.world, tresure_coords))
        self.game_mode = self.GAME_MODE_TWO_PLAYERS

    def init_player_vs_ai_game(self):
        self.init_new_world()

        tresure_coords = (self.world.width - 2, int(self.world.height / 2))
        self.world.add_treasure(Treasure(self.world, tresure_coords))

        self.player_one = Player(self.world, (0, 1), "Player 1")
        self.world.add_player(self.player_one)

        self.player_two = Player(self.world, (0, self.world.height - 2), "Player 2")
        self.world.add_player(self.player_two)
        game_difficult = self.menu.game_mode
        self.player_controller = AIPlayerController(self.world, self.player_two, tresure_coords, game_difficult)

        self.drawer.init_players_sprite(self.world.players)

        self.game_mode = self.GAME_MODE_PLAYER_VS_COMPUTER

#-check game status and show game over screen if needed
    def check_world_state(self):
        is_treasure_reached = self.world.is_treasure_reached()
        if is_treasure_reached:
            self.game_state = self.GAME_OVER_SCREEN                       
            self.init_game_over_screen()
            self.sound_player.play_end_of_game()
            
    def init_game_over_screen(self):
        winner_name = self.world.winner.name
        self.game_over_menu_vc = GameOverMenuViewController(self.resolution, winner_name)
        self.game_over_menu = self.game_over_menu_vc.game_over_menu

#-check game over menu status and start new game of quit
    def check_geme_over_menu_state(self):
        if self.game_over_menu.state == GameOverMenu.NEW_GAME:
            self.game_state = self.GAME_MENU_SCREEN
        elif self.game_over_menu.state == GameOverMenu.QUIT:
            self.game_state = self.SHOULD_QUIT
             
#Ask the drawer to draw the required part of the game 
    def draw(self):
        if self.game_state == self.GAME_MENU_SCREEN:
            self.drawer.draw_game_menu(self.main_menu_vc)
        elif self.game_state == self.PLAYING_GAME:
            self.drawer.draw_world(self.world)
        elif self.game_state == self.GAME_OVER_SCREEN:
            self.drawer.draw_game_over_menu(self.game_over_menu_vc)
