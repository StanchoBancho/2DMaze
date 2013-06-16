import pygame
from pygame import event
import World
import GameMenu
import GameOverMenu
import Drawer
from Controller import *

class Game:
    running = True
    should_show_menu = True
    player_one = None
    player_two = None
    
    def __init__(self, resolution):
        pygame.init()
        self.resolution = resolution
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("2DMaze Game")
        self.controller = Controller(resolution, self.screen)       

#        self.menu = GameMenu.GameMenu(self.screen, resolution)
#        self.square_size = 10
#        self.world_height = int(resolution[0] / self.square_size) - 1 
#        self.world_widht = int(resolution[1] / self.square_size) - 1
#        print(self.world_height, self.world_widht)
#        self.world = World.World((self.world_widht, self.world_height))
#        self.drawer = Drawer.Drawer(self.world, self.menu, self.screen)

    def show_game_over_menu(self):
        name = self.world
        self.game_over_menu = GameOverMenu.GameOverMenu(self.resolution)

    def main(self):
        clock = pygame.time.Clock()
        self.screen.fill(Drawer.white)
        while self.running:
            #handle the events
            should_quit = self.controller.handle_events()
            if should_quit:
                break
            #Run calculations to determine where objects move,
            #what happens when objects colli6de, etc.
            self.controller.update_game_status()

            #Clear the screen
            self.screen.fill(Drawer.white)

            #Draw everything
            self.controller.draw()
            
            pygame.display.flip()
            # Limit to 20 frames per second
            clock.tick(20)

if __name__ == '__main__':
    Game((800, 600)).main()
