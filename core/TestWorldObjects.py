import unittest
from WorldObjects import *


class TestWorldObjects(unittest.TestCase):

    def setUp(self):
        world_height = int(1280 / 10) - 1
        world_width = int(800 / 10) - 1
        self.world = World((world_width, world_height))
        self.player_one = Player(self.world, (0, 1), "Stancho")
        self.world.add_player(self.player_one)

    def test_add_player(self):
        self.assertIn(self.player_one, self.world.players)

    def test_add_treasure(self):
        tresure_coords = (self.world.width - 1, int(self.world.height/2))
        t = Treasure(self.world, tresure_coords)
        self.world.add_treasure(t)
        self.assertEqual(t, self.world.treasure)

    def test_player_movement(self):
        for i in range(10):
            for direction in Player.POSIBLE_DIRECTIONS:
                new_x = self.player_one.position[0] + direction[0]
                new_y = self.player_one.position[1] + direction[1]
                new_position = (new_x, new_y)
                if self.world.is_position_free(new_position):
                    self.player_one.move(direction)
                    self.assertEqual(self.player_one.position[0], new_x)
                    self.assertEqual(self.player_one.position[1], new_y)
                    break

    def test_if_position_free(self):
        position = (0, 0)  # part of the wall => black
        result = self.world.is_position_free(position)
        self.assertFalse(result)
        result = self.world.is_position_free(self.player_one.position)
        self.assertTrue(result)

    def test_is_treasure_reached(self):
        t = Treasure(self.world, self.player_one.position)
        self.world.add_treasure(t)
        result = self.world.is_treasure_reached()
        self.assertTrue(result)
