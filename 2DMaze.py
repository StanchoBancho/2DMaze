import pygame
from pygame.locals import *
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
    player_one = None
    player_two = None
    

    
    def __init__(self, resolution):
        pygame.init()
        self.screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption("2DMaze Game")
        self.menu = GameMenu.GameMenu(self.screen, resolution)
        self.world_height = int(resolution[0] / 5) - 1 
        self.world_widht = int(resolution[1] / 5) - 1
        print(self.world_height, self.world_widht)
        self.world = World.World((self.world_height, self.world_widht))

    def init_single_player_game(self):
        self.player_one = World.Player(self.world, (0, 1), "Stancho")
        self.world.add_player(self.player_one)
        self.player_two = None
        print("init single player game")

    def init_multy_player_game(self):
        self.player_one = World.Player(self.world, (0, 1), "Stancho")
        self.world.add_player(self.player_one)
        player_two_coords = (0, self.world_height - 2)
        self.player_two = World.Player(self.world, player_two_coords, "Dobby")
        self.world.add_player(self.player_two)

    def init_player_vs_mac_game(self):
        self.player_one = World.Player(self.world, (0, 1), "Stancho")
        self.player_two = World.Player(self.world, (0, 1), "PC")
        self.world.add_player(self.player_one)
        self.world.add_player(self.player_two)

    def check_menu_state(self):
        if self.menu.state == GameMenu.GameMenu.SINGLE_PLAYER:
            self.should_show_menu = False
            self.init_single_player_game()
        if self.menu.state == GameMenu.GameMenu.MULTY_PLAYER:
            self.should_show_menu = False
            self.init_multy_player_game()
        if self.menu.state == GameMenu.GameMenu.PLAYER_VS_MAC:
            self.should_show_menu = False
            self.init_player_vs_mac_game()
        
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
                if self.should_show_menu:                                        
                    self.menu.handle_event(event)
                if event.type == KEYDOWN:
                    if pygame.key.get_pressed()[K_RETURN]:
                        pass
                    
            keys = pygame.key.get_pressed()
            if self.should_show_menu:
                pass 
            else:
                if keys[K_LEFT]:
                    self.player_one.move(World.Player.LEFT)
                if keys[K_RIGHT]:
                    self.player_one.move(World.Player.RIGHT)
                if keys[K_UP]:
                    self.player_one.move(World.Player.DOWN)
                if keys[K_DOWN]:
                    self.player_one.move(World.Player.UP)
                if self.player_two:
                    if keys[K_a]:
                        self.player_two.move(World.Player.LEFT)
                    if keys[K_d]:
                        self.player_two.move(World.Player.RIGHT)
                    if keys[K_w]:
                        self.player_two.move(World.Player.DOWN)
                    if keys[K_s]:
                        self.player_two.move(World.Player.UP)
                    

            #Run calculations to determine where objects move,
            #what happens when objects colli6de, etc.
            prev_should_show_menu = self.should_show_menu
            if self.should_show_menu:
                self.check_menu_state()
                
            

            #Clear the screen
            self.screen.fill(self.white)

            #Draw everything
            if self.should_show_menu or prev_should_show_menu:
                self.menu.draw()
            else:
                self.world.draw(self.screen)

            pygame.display.flip()
            # Limit to 20 frames per second
            clock.tick(20)

if __name__ == '__main__':
    Game((800, 600)).main()
