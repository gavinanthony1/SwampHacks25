import pygame
from pong import Pong
from space_invaders import SpaceInvaders
from snake import Snake
import random
def game_transition():
    pygame.init()
    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h

    next_game = random.randrange(3)  # Starting game
    while True:
        if next_game == 0: # Pong
            current_game = next_game # two placeholders to prevent same game back-to-back
            game = Pong(width, height)
            if game.run() == 'escape':
                break
            while next_game == current_game:
                next_game = random.randrange(3)  # Move to next random game

        elif next_game == 1:  # SpaceInvaders
            current_game = next_game # two placeholders to prevent same game back-to-back
            game = SpaceInvaders(width, height)
            if game.run() == 'escape':
                break
            while next_game == current_game:
                next_game = random.randrange(3)  # Move to next random game

        elif next_game == 2: # Snake
            current_game = next_game  # two placeholders to prevent same game back-to-back
            game = Snake(width, height)
            if game.run() == 'escape':
                break
            while next_game == current_game:
                next_game = random.randrange(3)  # Move to next random game


if __name__ == "__main__":
    game_transition()

