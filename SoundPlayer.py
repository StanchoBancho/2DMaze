import pygame

class SoundPlayer:
    def __init__(self):
        self.is_playing = False
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)


    def stop_playing_music(self):
        self.is_playing = False
        pygame.mixer.music.stop()

    def play_theme_music(self):
        self.is_playing = True
        pygame.mixer.music.load('sound/Contra - Stage 2.wav')
        pygame.mixer.music.play(-1)

    def play_end_of_game(self):
        self.is_playing = False
        pygame.mixer.music.stop()
        pygame.mixer.music.load('sound/Contra - Stage Clear.wav')
        pygame.mixer.music.play(0)
        
