from World import *
from collections import deque

class AIPlayerController:

    def __init__(self, world, player, final_pos):
        self.world = world
        self.player = player
        self.final_pos = final_pos
        self.moves = []
        self.used_positions = []
        self.known_good_positions = {}
        self.create_heuristic_static_points()

    def create_heuristic_static_points(self):
        current_heuristic = -200
        queue = deque([self.final_pos])
        self.known_good_positions[self.final_pos] = current_heuristic
        used = [self.final_pos]
        while len(queue) > 0 and current_heuristic < 0:
            t = queue.pop()
            self.known_good_positions[t] = current_heuristic
            neighbours = self.get_possible_moves_for_position(t)
            for n in neighbours:
                if not n in used:
                    queue.append(n)
                    used.append(n)
            current_heuristic = current_heuristic + 1
    
    def heuristic_cost(self, start):
        if start in self.known_good_positions:
            return self.known_good_positions[start]
        result = abs(start[0] - self.final_pos[0]) + abs(start[1] - self.final_pos[1])
        return result

    def get_possible_moves_for_position(self, position):
        result = []
        pos = position
        for d in Player.POSIBLE_DIRECTIONS: 
            new_pos = (d[0]+pos[0], d[1]+pos[1])
            is_new_pos_free = self.world.is_position_free(new_pos)
            if is_new_pos_free:
                result.append(new_pos)
        return result
    
    def get_possible_moves(self):
        result = []
        pos = self.player.position
        for d in Player.POSIBLE_DIRECTIONS: 
            new_pos = (d[0]+pos[0], d[1]+pos[1])
            is_new_pos_free = self.world.is_position_free(new_pos)
            if is_new_pos_free and (not new_pos in self.used_positions):
                result.append(new_pos)
        return result
                        
    def get_best_possible_move(self):
        result = None
        possible_moves = self.get_possible_moves()
        for move in possible_moves:
            if not result:
                result = move
            else:
                cur_heuristic_dist = self.heuristic_cost(result)
                move_heuristic_dist = self.heuristic_cost(move)
                if move_heuristic_dist < cur_heuristic_dist:
                    result = move
        return result
                  
    def move_player(self):
        best_move = self.get_best_possible_move()
        if best_move:
            self.moves.append(self.player.position)
            self.player.move_to_position(best_move)
            self.used_positions.append(best_move)
            return True
        else:
            if len(self.moves) > 0:
                prev_pos = self.moves.pop()
                self.player.move_to_position(prev_pos)

                return True
        return False
