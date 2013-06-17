from World import *

class AIPlayerController:

    def __init__(self, world, player, final_pos):
        self.world = world
        self.player = player
        self.final_pos = final_pos
        self.initiate_moving_program(player.position, final_pos)

    def initiate_moving_program(self, start, goal):
        self.closed_set = []
        self.open_set = [start]
        self.came_from = []
        # Cost from start along best known path.
        self.g_score = [{'pos':start, 'val':0}]
        # Estimated total cost from start to goal through y.
        estimated_cost = 0 + self.heuristic_cost(start, goal)
        self.f_score = [{'pos':start, 'val':estimated_cost}]

    def heuristic_cost(self, start, goal):
        result = abs(start[0] - goal[0]) + abs(start[1] - goal[1])
        return result
                        
    def get_lowest_from_f_score(self):
        new_f_score = sorted(self.f_score, key=lambda k: k['val'])
        self.f_score = new_f_score;
        #print(">>>>>>>>>The result of funk is", self.f_score[0])
        #print(">>>>>>>>>The open set is ",self.open_set)
        for a_f_score in self.f_score:
            #print('>>>>>>>>>abs for', a_f_score, ' is ', self.heuristic_cost(self.player.position, a_f_score['pos']))
            #is_it_neighbour = self.heuristic_cost(self.player.position, a_f_score['pos']) < 2
            if a_f_score['pos'] in self.open_set:# and is_it_neighbour:
                return a_f_score
        return self.f_score[0]

    def get_possible_moves(self):
        result = []
        pos = self.player.position
        for d in Player.POSIBLE_DIRECTIONS: 
            new_pos = (d[0]+pos[0], d[1]+pos[1])
            if self.world.is_position_free(new_pos):
                result.append(new_pos)
        return result
                        
    def get_g_score_for_position(self, position):
        positions = [score for score in self.g_score if score['pos']==position]
        return positions[0]
                        
    def move_player(self):
        if len(self.open_set) > 0:
            #change the current position
            self.current = self.get_lowest_from_f_score()
            self.player.move_to_position(self.current['pos'])
            if self.current['pos'] == self.final_pos:
                return
            print("remove",self.current['pos'], " from ", self.open_set)
            if self.current['pos'] in self.open_set: 
                self.open_set.remove(self.current['pos'])
            self.closed_set.append(self.current['pos'])
            possible_moves = self.get_possible_moves()
            for p in possible_moves:
                current_g_score = self.get_g_score_for_position(self.current['pos'])
                tentative_g_score = current_g_score['val']
                if p in self.closed_set:
                    p_g_score = self.get_g_score_for_position(p)['val']
                    if tentative_g_score >= p_g_score:
                        continue
                if not p in self.open_set or tentative_g_score < self.get_g_score_for_position(p):
                    self.g_score.append({'pos':p, 'val':tentative_g_score})
                    f_score_val = tentative_g_score + self.heuristic_cost(p, self.final_pos)
                    self.f_score.append({'pos':p, 'val':f_score_val})
                    if not p in self.open_set:
                        self.open_set.append(p)
