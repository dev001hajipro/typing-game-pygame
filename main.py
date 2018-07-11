# -*- coding: utf-8 -*-
"""
タイピングゲーム
"""


import random
import sys
from enum import Enum

import pygame
import pygame.mixer

#from pygame.locals import *


def choise_word(words: list) -> str:
    """単語帳から単語をランダムに１つ取得"""
    element_count = len(words) - 1
    rnd = random.randint(0, element_count)
    return words[rnd]


COUNT_MAX = 60


class GameState(Enum):
    """ゲーム状態"""
    TITLE = 1
    PLAY = 2

# タイトルはスコアと"Press space key to start"を表示
# Play状態では、


def main(words: list):
    """ゲーム起動"""
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.mixer.init()
    se_keytype = pygame.mixer.Sound('.\\se\\keytype2.wav')

    pygame.init()
    screen = pygame.display.set_mode((720, 480))
    pygame.display.set_caption("タイピングゲーム")
    screen_width, screen_height = pygame.display.get_surface().get_size()
    game_state = GameState.TITLE

    sysfont72 = pygame.font.SysFont(None, 128)
    sysfont14 = pygame.font.SysFont(None, 24)
    sysfont64 = pygame.font.SysFont(None, 64)

    score = 0
    start_ticks = pygame.time.get_ticks()

    word = choise_word(words)

    while True:
        screen.fill((240, 240, 240))
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000

        if game_state == GameState.TITLE:
            text_score = sysfont72.render("Typing Game", True, (0, 0, 0))
            text_width = text_score.get_rect().width
            text_height = text_score.get_rect().height
            screen.blit(text_score, (screen_width/2 - text_width /
                                     2, screen_height/5))

            text_press_space_key = sysfont64.render(
                "Press Space key", True, (0, 0, 0))
            text_width = text_press_space_key.get_rect().width
            text_height = text_press_space_key.get_rect().height
            screen.blit(text_press_space_key, (screen_width/2 - text_width /
                                               2, screen_height/2 - text_height/2))

            text_score = sysfont64.render(
                "score: " + str(score), True, (0, 0, 0))
            text_width = text_score.get_rect().width
            text_height = text_score.get_rect().height
            screen.blit(text_score, (screen_width/2 - text_width /
                                     2, screen_height/5 * 3))

        else:
            text_word = sysfont72.render(
                word, True, (0, 0, 0))
            remaining_time = COUNT_MAX - int(seconds)
            if remaining_time <= 0:
                game_state = GameState.TITLE

            text_countdown = sysfont14.render(
                "time: " + str(remaining_time), True, (0, 0, 0))
            text_score = sysfont14.render(
                "score: " + str(score), True, (0, 0, 0))
            text_width = text_word.get_rect().width
            text_height = text_word.get_rect().height
            screen.blit(text_word, (screen_width/2 - text_width /
                                    2, screen_height/2 - text_height/2))
            screen.blit(text_countdown, (10, 10))
            screen.blit(text_score, (10, 30))

        pygame.display.update()

        for event in pygame.event.get():
            if game_state == GameState.TITLE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # resetGame()
                        word = choise_word(words)
                        score = 0

                        game_state = GameState.PLAY

            elif game_state == GameState.PLAY:
                if event.type == pygame.KEYDOWN:
                    #print(f"code:{str(event.key)}, char:${chr(event.key)}")
                    # todo: support Shiftkey, Uppercase 'A','B','C'...
                    # se_keytype.stop()
                    # se_keytype.play()
                    if chr(event.key) == word[0]:
                        pygame.mixer.find_channel().play(se_keytype)
                        word = word[1:]
                        score += 1
                        if not word:
                            word = choise_word(words)

            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                sys.exit()


if __name__ == '__main__':

    WORDS = [
        'apple',
        'banana',
        'cherry',
        'grape',
        'kiwi',
        'lime',
        'lemon',
        'mandarin',
        'melon',
        'orange',
        'pear',
        'persimmon',
        'plum',
        'strawberry',
        'vine',
        'watermelon'
    ]

    main(WORDS)
