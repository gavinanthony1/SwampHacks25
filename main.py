import pygame
from pong import Pong
from space_invaders import SpaceInvaders
from snake import Snake
from tetris import Tetris
import random


def game_transition(difficulty=5):
    pygame.init()
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h

    games = [Pong, SpaceInvaders, Snake, Tetris]

    # shuffle games at the start
    games_shuffled = games[:]
    random.shuffle(games_shuffled)

    while True:
        for game_order in games_shuffled:
            game = game_order(width, height, difficulty)
            result = game.run()

            # handle escape or difficulty change
            if result == 'escape':
                return
            else:
                difficulty = result

        # reshuffle after all games have been played
        random.shuffle(games_shuffled)


if __name__ == "__main__":
    game_transition(5)
