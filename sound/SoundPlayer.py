import pygame
import os
import sys


class SoundPlayer:

    def __init__(self):
        self.is_playing = False
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)

    def stop_playing_music(self):
        self.is_playing = False
        pygame.mixer.music.stop()

    def play_theme_music(self):
        self.is_playing = True
        pygame.mixer.music.stop()
        fullname = os.path.join('sound', 'Contra - Stage 1.wav')
        pygame.mixer.music.load(fullname)
        pygame.mixer.music.play(-1)

    def play_end_of_game(self):
        if self.is_playing:
            self.is_playing = False
            pygame.mixer.music.stop()
            fullname = os.path.join('sound', 'Contra - Stage Clear.wav')
            pygame.mixer.music.load(fullname)
            pygame.mixer.music.play(0)
