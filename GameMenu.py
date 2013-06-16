import pygame
import pygbutton

class GameMenu:
    NO_MODE_CHOSED = 0
    SINGLE_PLAYER = 1
    MULTY_PLAYER = 2
    PLAYER_VS_MAC = 3
        
    def __init__(self, screen, resolution):
        self.screen = screen
        self.resolution = resolution
        self.origin = ((resolution[0] - 256) / 2, (resolution[1] - 256) / 2)
        self.single_player = pygbutton.PygButton((self.origin[0] + 64, self.origin[1] + 40, 128, 32), 'Single Player')
        self.multy_player = pygbutton.PygButton((self.origin[0] + 64, self.origin[1] + 112, 128, 32), 'Multy Player')
        self.player_vs_mac = pygbutton.PygButton((self.origin[0] + 64, self.origin[1] + 184, 128, 32), 'Player vs MAC')
        self.all_buttons = [self.single_player, self.multy_player, self.player_vs_mac]
        self.state = GameMenu.NO_MODE_CHOSED

    def handle_event(self, event):
        if 'click' in self.single_player.handleEvent(event):
            self.state = GameMenu.SINGLE_PLAYER
        if 'click' in self.multy_player.handleEvent(event):
            self.state = GameMenu.MULTY_PLAYER
        if 'click' in self.player_vs_mac.handleEvent(event):
            self.state = GameMenu.PLAYER_VS_MAC
