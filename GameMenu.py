import pygame
import pygbutton
import os, sys

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
        

        
    def draw(self):
        r = self.resolution
        background_surface = GameMenu.load_image("maze_background.png")[0]
        scaled_surface = pygame.transform.scale(background_surface, r)
        self.screen.blit(scaled_surface, (0, 0))
         
        pygame.draw.rect(self.screen, (232, 232, 232), (self.origin[0], self.origin[1], 256, 256))
        for b in self.all_buttons:
            b.draw(self.screen)

    def handle_event(self, event):
        if 'click' in self.single_player.handleEvent(event):
            self.state = GameMenu.SINGLE_PLAYER
        if 'click' in self.multy_player.handleEvent(event):
            self.state = GameMenu.MULTY_PLAYER
        if 'click' in self.player_vs_mac.handleEvent(event):
            self.state = GameMenu.PLAYER_VS_MAC
            
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
