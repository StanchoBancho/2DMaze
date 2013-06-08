import pygame
import World

class Game:


    # Define some colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = ( 255, 0, 0)
    running = True

    def __init__(self, resolution):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("2DMaze Game")

        world_height = int(resolution[0] / 5) - 1 
        world_widht = int(resolution[1] / 5) - 1
        self.world = World.World((world_height, world_widht))
    

    def main(self):
        clock = pygame.time.Clock()
        self.screen.fill(self.white)
        while self.running:
            #handle the events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("User asked to quit.")
                    pygame.quit()
                    return                    
                if event.type == pygame.KEYDOWN:
                    print("User pressed a key.")

            #Run calculations to determine where objects move,
            #what happens when objects collide, etc.

            #Clear the screen
            self.screen.fill(self.white)

            #Draw everything
            self.world.draw(self.screen)
            pygame.draw.rect(self.screen, self.green, (50,60,50,50))

            pygame.display.flip()
            # Limit to 20 frames per second
            clock.tick(20)

if __name__ == '__main__':
    Game((800, 600)).main()
