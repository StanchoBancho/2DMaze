from pygbutton import PygButton
import pygame

from core.GameMenu import *


class GameMenuViewController:
    MENU_SIZE = 384
    BUTTON_SIZE = (276, 32)
    MODE_BUTTON_SIZE = (90, 32)

    def __init__(self, screen, resolution):
        self.screen = screen
        self.resolution = resolution
        self.origin = ((resolution[0] - self.MENU_SIZE) / 2,
                       (resolution[1] - self.MENU_SIZE) / 2)
        self.init_buttons(resolution)
        self.game_menu = GameMenu()

    def init_buttons(self, resolution):
        self.all_buttons = []
        #main game option buttons
        space_from_border = (self.MENU_SIZE - self.BUTTON_SIZE[0])/2
        button_origin_x = self.origin[0] + space_from_border
        b_width = self.BUTTON_SIZE[0]
        b_height = self.BUTTON_SIZE[1]

        s_p_button_frame = (button_origin_x, self.origin[1] + 60, b_width,
                            b_height)
        self.single_player = PygButton(s_p_button_frame, 'Single Player')
        self.all_buttons.append(self.single_player)

        m_p_button_frame = (button_origin_x, self.origin[1] + 120, b_width,
                            b_height)
        self.multy_player = PygButton(m_p_button_frame, 'Multy Player')
        self.all_buttons.append(self.multy_player)

        p_v_a_i_button_frame = (button_origin_x, self.origin[1] + 180, b_width,
                                b_height)
        self.player_vs_ai = PygButton(p_v_a_i_button_frame, 'Player vs AI')
        self.all_buttons.append(self.player_vs_ai)

        #AI difficulty buttons
        b_width = self.MODE_BUTTON_SIZE[0]
        b_height = self.MODE_BUTTON_SIZE[1]

        normal_button_frame = (button_origin_x, self.origin[1] + 220, b_width,
                               b_height)
        self.normal = PygButton(normal_button_frame, 'Normal')
        self.normal.bgcolor = (128, 128, 128)
        self.chosed_mode_button = self.normal
        self.all_buttons.append(self.normal)

        nightmare_button_frame = (button_origin_x + 92, self.origin[1] + 220,
                                  b_width, b_height)
        self.nightmare = PygButton(nightmare_button_frame, 'Nightmare')
        self.all_buttons.append(self.nightmare)

        inferno_button_frame = (button_origin_x + 184, self.origin[1] + 220,
                                b_width, b_height)
        self.inferno = PygButton(inferno_button_frame, 'Inferno')
        self.all_buttons.append(self.inferno)
        #Sound and Help buttons
        b_width = (self.BUTTON_SIZE[0] - 2)/2
        b_height = (self.BUTTON_SIZE[1] - 2)
        sound_button_frame = (button_origin_x, self.origin[1] + 280, b_width,
                              b_height)
        self.sound = PygButton(sound_button_frame, 'Sound')
        self.all_buttons.append(self.sound)
#        help_button_frame = (button_origin + b_width + 2 ,
#                              self.origin[1] + 280, b_width, b_height)
#        self.help = PygButton(help_button_frame, 'Help')
#        self.all_buttons.append(self.help)

        #Quit button
        b_width = self.BUTTON_SIZE[0]
        b_height = self.BUTTON_SIZE[1]
        quit_button_frame = (button_origin_x, self.origin[1] + 340, b_width,
                             b_height)
        self.quit = PygButton(quit_button_frame, 'Quit')
        self.all_buttons.append(self.quit)

    def handle_event(self, event):
        if 'click' in self.single_player.handleEvent(event):
            self.game_menu.state = GameMenu.SINGLE_PLAYER
        if 'click' in self.multy_player.handleEvent(event):
            self.game_menu.state = GameMenu.MULTY_PLAYER
        if 'click' in self.player_vs_ai.handleEvent(event):
            self.game_menu.state = GameMenu.PLAYER_VS_MAC
        if 'click' in self.quit.handleEvent(event):
            self.game_menu.should_quit = True
        #handle game difficulty
        if 'click' in self.normal.handleEvent(event):
            self.game_menu.game_mode = GameMenu.AI_NORMAL
            self.chosed_mode_button.bgcolor = (212, 208, 200)
            self.normal.bgcolor = (128, 128, 128)
            self.chosed_mode_button = self.normal
        if 'click' in self.nightmare.handleEvent(event):
            self.game_menu.game_mode = GameMenu.AI_NIGHTMARE
            self.chosed_mode_button.bgcolor = (212, 208, 200)
            self.nightmare.bgcolor = (128, 128, 128)
            self.chosed_mode_button = self.nightmare
        if 'click' in self.inferno.handleEvent(event):
            self.game_menu.game_mode = GameMenu.AI_INFERNO
            self.chosed_mode_button.bgcolor = (212, 208, 200)
            self.inferno.bgcolor = (128, 128, 128)
            self.chosed_mode_button = self.inferno
        #handle sound
        if 'click' in self.sound.handleEvent(event):
            should_play_sound = self.game_menu.should_play_sound
            self.game_menu.should_play_sound = not should_play_sound
            if self.game_menu.should_play_sound:
                self.sound.bgcolor = (212, 208, 200)
                self.sound.caption = 'Sound'
            else:
                self.sound.bgcolor = (128, 128, 128)
                self.sound.caption = 'No Sound'
