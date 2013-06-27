import pygame
from core.Controller import *
class Game:
    running = True
    
    def __init__(self, resolution):
        pygame.init()
        self.resolution = resolution
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("2DMaze Game")
        self.controller = Controller(resolution, self.screen)       

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
            # Limit to 15 frames per second
            clock.tick(15)

if __name__ == '__main__':
    Game((1280, 800)).main()
