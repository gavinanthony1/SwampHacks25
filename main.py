# Code created with the assistance of ChatGPT, OpenAI's language model
# ChatGPT helped with getting started on new files, mostly with setting up the look of the games

import pygame
from pong import Pong
from space_invaders import SpaceInvaders
from snake import Snake
from tetris import Tetris
import random
from Screens import game_screens

def game_transition(difficulty=5, player_name = "Player"):
    screens = game_screens()
    pygame.init()
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h

    games = [Pong, SpaceInvaders, Snake, Tetris]
    random.shuffle(games)


    running = True
    while running:
        for game_order in games:
            game = game_order(width, height, difficulty)
            result = game.run()

            if result == 'escape':
                running = False
                break
            else:
                # updates difficulty
                difficulty = result

        random.shuffle(games)  # shuffles the games

    # displays leaderboard and does some other stuff
    screen = pygame.display.set_mode((width, height))
    screen.fill((0, 0, 0))
    screens.update_leaderboard(player_name, difficulty)
    screens.display_leaderboard(screen, width, height)
    pygame.display.flip()
    screens.save_leaderboard()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                waiting = False


if __name__ == "__main__":
    screens = game_screens()
    player_name = screens.welcome_screen()
    game_transition(5, player_name)
