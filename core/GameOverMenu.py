class GameOverMenu:
    NO_OPERATION_CHOSED = 0
    NEW_GAME = 1
    QUIT = 2

    def __init__(self, winner_name):
        self.winner_name = winner_name
        self.state = self.NO_OPERATION_CHOSED
