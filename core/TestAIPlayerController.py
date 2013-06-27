import unittest
from AIPlayerController import *


class TestAIPlayerController(unittest.TestCase):

    def setUp(self):
        world_height = int(1280 / 10) - 1
        world_width = int(800 / 10) - 1
        self.world = World((world_width, world_height))
        self.player_one = Player(self.world, (0, 1), "Stancho")
        self.world.add_player(self.player_one)
        tresure_coords = (self.world.width - 1, int(self.world.height/2))
        self.world.add_treasure(Treasure(self.world, tresure_coords))
#        difficult = GameMenu.AI_NORMAL
#        difficult = GameMenu.AI_NIGHTMARE
        difficult = GameMenu.AI_INFERNO
        self.player_controller = AIPlayerController(self.world,
                                                    self.player_one,
                                                    tresure_coords, difficult)

    def test_finding_game_treasure_movement(self):
        worst_case_turns = 1280 * 800
        for i in range(worst_case_turns + 1):
            if self.world.is_treasure_reached():
                self.assertEqual(1, 1)
                return
            self.player_controller.move_player()
        self.assertEqual(0, 1)
