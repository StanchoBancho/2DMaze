import pygame
from pygame import event
import World
import GameMenu

class Game:


    # Define some colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    red = ( 255, 0, 0)
    running = True
    should_show_menu = True
    
    def __init__(self, resolution):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("2DMaze Game")
        self.menu = GameMenu.GameMenu(self.screen, resolution)
        world_height = int(resolution[0] / 5) - 1 
        world_widht = int(resolution[1] / 5) - 1
        self.world = World.World((world_height, world_widht))

    def init_single_player_game(self):
        self.player_one = World.Player(self.world, (0, 1), "Stancho")
        self.world.add_player(self.player_one)

    def init_multy_player_game(self):
        self.player_one = World.Player(self.world, (0, 1), "Stancho")
        self.player_two = World.Player(self.world, (0, 1), "Dobby")
        self.world.add_player(self.player_one)
        self.world.add_player(self.player_two)

    def init_player_vs_mac_game(self):
        self.player_one = World.Player(self.world, (0, 1), "Stancho")
        self.player_two = World.Player(self.world, (0, 1), "PC")
        self.world.add_player(self.player_one)
        self.world.add_player(self.player_two)

        
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
                    if self.should_show_menu:
                        pass 
                    else:
                        if event.key == pygame.K_LEFT:
                           self.player_one.move(World.Player.LEFT)
                        if event.key == pygame.K_RIGHT:
                           self.player_one.move(World.Player.RIGHT)
                        if event.key == pygame.K_UP:
                           self.player_one.move(World.Player.DOWN)
                        if event.key == pygame.K_DOWN:
                           self.player_one.move(World.Player.UP)

                if self.should_show_menu:                                        
                    self.menu.handle_event(event)
            #Run calculations to determine where objects move,
            #what happens when objects colli6de, etc.

            
                
            

            #Clear the screen
            self.screen.fill(self.white)

            #Draw everything
            if self.should_show_menu:
                self.menu.draw()
                if self.menu.state == GameMenu.GameMenu.SINGLE_PLAYER:
                    self.should_show_menu = False
                    self.init_single_player_game()
            else:
                self.world.draw(self.screen)

            pygame.display.flip()
            # Limit to 20 frames per second
            clock.tick(20)

if __name__ == '__main__':
    Game((800, 600)).main()
