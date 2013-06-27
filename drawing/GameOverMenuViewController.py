import pygame
from pygbutton import PygButton
from core.GameOverMenu import GameOverMenu


class GameOverMenuViewController:
    MENU_SIZE = 284
    BUTTON_SIZE = (128, 32)

    def __init__(self, resolution, winner_name):
        self.resolution = resolution
        self.origin = ((resolution[0] - self.MENU_SIZE)/2,
                       (resolution[1] - self.MENU_SIZE)/2)
        space_from_border = (self.MENU_SIZE - self.BUTTON_SIZE[0])/2
        button_origin_x = self.origin[0] + space_from_border
        self.new_game_button = PygButton((button_origin_x,
                                          self.origin[1] + 144,
                                          self.BUTTON_SIZE[0],
                                          self.BUTTON_SIZE[1]), 'New Game')
        self.quit_button = PygButton((button_origin_x, self.origin[1] + 192,
                                      self.BUTTON_SIZE[0],
                                      self.BUTTON_SIZE[1]),
                                     'Quit')
        self.all_buttons = [self.new_game_button, self.quit_button]
        self.game_over_menu = GameOverMenu(winner_name)

    def handle_event(self, event):
        if 'click' in self.new_game_button.handleEvent(event):
            self.game_over_menu.state = GameOverMenu.NEW_GAME
        if 'click' in self.quit_button.handleEvent(event):
            self.game_over_menu.state = GameOverMenu.QUIT
