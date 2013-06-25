import pygame
from drawing.pygbutton import PygButton

class GameOverMenu:
    NO_OPERATION_CHOSED = 0
    NEW_GAME = 1
    QUIT = 2
            
    def __init__(self, resolution, winner_name):
        self.resolution = resolution
        self.origin = ((resolution[0] - 256) / 2, (resolution[1] - 256) / 2)
        self.winner_name = winner_name

        self.new_game_button = PygButton((self.origin[0] + 64, self.origin[1] + 144, 128, 32), 'New Game')
        self.quit_button = PygButton((self.origin[0] + 64, self.origin[1] + 192, 128, 32), 'Quit')      
        self.all_buttons = [self.new_game_button, self.quit_button]
        self.state = self.NO_OPERATION_CHOSED

    def handle_event(self, event):
        if 'click' in self.new_game_button.handleEvent(event):
            self.state = GameOverMenu.NEW_GAME
        if 'click' in self.quit_button.handleEvent(event):
            self.state = GameOverMenu.QUIT
