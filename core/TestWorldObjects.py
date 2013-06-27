import unittest
from WorldObjects import *

class TestWorldObjects(unittest.TestCase):

    def setUp(self):
        world_height = int(1280 / 10) - 1
        world_width = int(800 / 10) - 1
        self.world = World((world_width, world_height)) 
        self.player_one = Player(self.world, (0, 1), "Stancho")
        self.world.add_player(self.player_one)
        
        
    def test_player_movement(self):
        for i in range (10):
            for direction in Player.POSIBLE_DIRECTIONS:
                new_x = self.player_one.position[0] + direction[0]
                new_y = self.player_one.position[1] + direction[1]
                new_position = (new_x, new_y)
                if self.world.is_position_free(new_position):
                    self.player_one.move(direction)
                    self.assertEqual(self.player_one.position[0], new_x)
                    self.assertEqual(self.player_one.position[1], new_y)
                    break

    
