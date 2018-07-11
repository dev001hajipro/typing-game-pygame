# -*- coding: utf-8 -*-
"""
タイピングゲーム
"""

import random
import sys
from enum import Enum

import pygame
import pygame.mixer


class SceneState(Enum):
    """シーンの状態"""
    TITLE = 0
    PLAY = 1


class CommonState():
    """状態"""
    REMAINING_TIME_MAX = 60

    def __init__(self, screen_w, screen_h, words):
        self.screen = {'w': screen_w, 'h': screen_h}
        self.count = 0
        self.score = 0
        self.state = SceneState.TITLE
        self.start_ticks = pygame.time.get_ticks()
        self.words = words
        self.word = ""

    def choise_word(self):
        """単語帳から単語をランダムに１つ取得"""
        if not self.word:
            element_count = len(self.words) - 1
            rnd = random.randint(0, element_count)
            self.word = self.words[rnd]

    def firstletter(self):
        """ 先頭文字取得"""
        return self.word[0]

    def remove_firstletter(self):
        """ 先頭文字削除 """
        self.word = self.word[1:]

    def get_seconds(self):
        """ ミリ秒を秒にして開始時刻からの経過秒数を返す """
        return (pygame.time.get_ticks() - self.start_ticks) / 1000


class Scene():
    """シーン共通のベースクラス"""

    def __init__(self, screen, common_state, util):
        """ constructor """
        self.screen = screen
        self.common_state = common_state
        self.screen_w = common_state.screen['w']
        self.screen_h = common_state.screen['h']
        self.util = util

    def render(self):
        """ ダミー、abstruct class 作るの面倒なので空のデフォルト実装"""
        pass

    def input(self):
        """ ダミー、abstruct class 作るの面倒なので空のデフォルト実装"""
        pass

    def process(self):
        """ テンプレートメソッド """
        self.screen.fill((240, 240, 240))
        self.render()
        pygame.display.update()
        self.input()


def check_quit(event_type):
    """ 閉じるボタンの検知 """
    if event_type == pygame.QUIT:
        pygame.mixer.quit()
        pygame.quit()
        sys.exit()


class TitleScene(Scene):
    """title scene"""

    def __init__(self, screen, common_state, util):
        """ constructor """
        Scene.__init__(self, screen, common_state, util)

    def input(self):
        """ handle key event """
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.util.play_se_keytype()
                    self.common_state.choise_word()
                    self.common_state.score = 0
                    self.common_state.state = SceneState.PLAY
            check_quit(event.type)

    def render(self):
        """ render """
        utl = self.util
        text_score = utl.render_128("Typing Game")
        text_width = text_score.get_rect().width
        text_height = text_score.get_rect().height
        self.screen.blit(text_score, (self.screen_w/2 - text_width /
                                      2, self.screen_h/5))

        text_press_space_key = utl.render_64("Press Space key")
        text_width = text_press_space_key.get_rect().width
        text_height = text_press_space_key.get_rect().height
        self.screen.blit(text_press_space_key, (self.screen_w/2 - text_width /
                                                2, self.screen_h/2 - text_height/2))

        text_score = utl.render_64(f"score: {str(self.common_state.score)}")
        text_width = text_score.get_rect().width
        text_height = text_score.get_rect().height
        self.screen.blit(text_score, (self.screen_w/2 - text_width /
                                      2, self.screen_h/5 * 3))


class GameScene(Scene):
    """game scene"""

    def __init__(self, screen, common_state, util):
        """ constructor """
        Scene.__init__(self, screen, common_state, util)

    def __get_remaining_time(self):
        seconds = self.common_state.get_seconds()
        return CommonState.REMAINING_TIME_MAX - int(seconds)

    def input(self):
        """ handle key event """

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # print(f"code:{str(event.key)}, char:${chr(event.key)}")
                # todo: support Shiftkey, Uppercase 'A','B','C'...
                if chr(event.key) == self.common_state.firstletter():
                    self.util.play_se_keytype()
                    self.common_state.remove_firstletter()
                    self.common_state.score += 1
                    self.common_state.choise_word()
            check_quit(event.type)

    def render(self):
        """ render """
        utl = self.util

        text_word = utl.render_128(self.common_state.word)

        remaining_time = self.__get_remaining_time()
        if remaining_time <= 0:
            self.common_state.state = SceneState.TITLE

        text_countdown = utl.render_24(f"time: {str(remaining_time)}")
        text_score = utl.render_24(f"score: {str(self.common_state.score)}")
        text_width = text_word.get_rect().width
        text_height = text_word.get_rect().height
        self.screen.blit(text_word, (self.screen_w/2 - text_width /
                                     2, self.screen_h/2 - text_height/2))
        self.screen.blit(text_countdown, (10, 10))
        self.screen.blit(text_score, (10, 30))


class Utility():
    """ Helper """

    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.mixer.init()
        pygame.init()

        self.se_keytype = pygame.mixer.Sound('.\\se\\keytype2.wav')
        self.font128 = pygame.font.SysFont(None, 128)
        self.font64 = pygame.font.SysFont(None, 64)
        self.font24 = pygame.font.SysFont(None, 24)

    def play_se_keytype(self):
        """ タイプ音を鳴らす """
        pygame.mixer.find_channel().play(self.se_keytype)

    def render_128(self, msg):
        """ 大きな文字 """
        return self.font128.render(msg, True, pygame.Color("black"))

    def render_64(self, msg):
        """ タイトル画面のスコア """
        return self.font64.render(msg, True, pygame.Color("black"))

    def render_24(self, msg):
        """ ゲーム画面のタイマー、スコア """
        return self.font24.render(msg, True, pygame.Color("black"))


def main(words: list):
    """ゲーム起動"""

    util = Utility()
    screen = pygame.display.set_mode((720, 480))
    pygame.display.set_caption("タイピングゲーム")
    screen_w, screen_h = pygame.display.get_surface().get_size()

    common_state = CommonState(screen_w, screen_h, words)

    scenes = {
        SceneState.TITLE: TitleScene(screen, common_state, util),
        SceneState.PLAY: GameScene(screen, common_state, util)
    }

    while True:
        scenes[common_state.state].process()


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
