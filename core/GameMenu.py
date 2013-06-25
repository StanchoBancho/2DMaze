class GameMenu:
    NO_MODE_CHOSED = 0
    SINGLE_PLAYER = 1
    MULTY_PLAYER = 2
    PLAYER_VS_MAC = 3

    PLAY_MUSIC = 0
    DO_NOT_PLAY_MUSIC = 1

    AI_NORMAL = 0
    AI_NIGHTMARE = 1
    AI_INFERNO = 2
    
    def __init__(self):
        self.state = GameMenu.NO_MODE_CHOSED
        self.should_quit = False
        self.game_mode = GameMenu.AI_NORMAL
        self.should_play_sound = True
                  



