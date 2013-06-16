import pygame
import pygbutton

class GameOverMenu:
    NO_OPERATION_CHOSED = 0
    NEW_GAME = 1
    QUIT = 2
            
    def __init__(self, resolution, winner_name):
        self.resolution = resolution
        self.origin = ((resolution[0] - 256) / 2, (resolution[1] - 256) / 2)
        self.winner_name = winner_name

        self.new_game_button = pygbutton.PygButton((self.origin[0] + 64, self.origin[1] + 40, 128, 32), 'New Game')
        self.quit_button = pygbutton.PygButton((self.origin[0] + 64, self.origin[1] + 112, 128, 32), 'Quit')      
        self.all_buttons = [self.new_game_button, self.quit_button]
        self.state = self.NO_OPERATION_CHOSED

    def handle_event(self, event):
        if 'click' in self.new_game_button.handleEvent(event):
            self.state = GameMenu.NEW_GAME
        if 'click' in self.quit_button.handleEvent(event):
            self.state = GameMenu.QUIT
