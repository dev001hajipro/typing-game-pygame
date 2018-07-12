""" コード行数を抑えたタイピングゲーム実装 """
import random
import sys

import pygame
import pygame.mixer


def run():
    """タイピングゲーム"""

    words = []
    with open('words.txt') as csvfile:
        words = list(map(lambda s: s.rstrip(), list(csvfile.readlines())))
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.mixer.init()
    pygame.init()
    pygame.display.set_caption("タイピングゲーム")
    se_keytype = pygame.mixer.Sound('.\\se\\keytype2.wav')
    fonts = [pygame.font.SysFont(None, 24), pygame.font.SysFont(None, 128)]
    screen = pygame.display.set_mode((720, 480))
    playing, start_ticks, timer, score, word = (
        False, pygame.time.get_ticks(), 10, 0, 'press space key.')
    while True:
        screen.fill((240, 240, 240))
        if playing:
            timer = 10 - int((pygame.time.get_ticks() - start_ticks) / 1000)
            if timer <= 0:
                playing, word = (False, 'press space key.')
        screen.blit(fonts[0].render(
            f"time:{timer} score:{score}", True, (0, 0, 0)), (10, 10))
        text_word = fonts[1].render(f"{word}", True, (0, 0, 0))
        screen.blit(text_word, (screen.get_size()[0]/2 - text_word.get_size()[0] /
                                2, screen.get_size()[1]/2 - text_word.get_size()[1]/2))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                change_word_flag = False
                if not playing and event.key == pygame.K_SPACE:
                    playing, start_ticks, timer, score, change_word_flag = (
                        True, pygame.time.get_ticks(), 10, 0, True)
                elif playing and chr(event.key) == word[0]:
                    pygame.mixer.find_channel().play(se_keytype)
                    score += 1
                    word = word[1:]
                    change_word_flag = not word
                if change_word_flag:
                    word = words[random.randint(0, len(words) - 1)]
            elif event.type == pygame.QUIT:
                sys.exit()


run()
