import pygame
from pong import main as pong_main
from space_invaders import main as space_invaders_main
from snake import main as snake_main

def game_transition():
    current_game = "Pong"  # Starting game
    while True:
        if current_game == "Pong":
            if pong_main() == 'escape':  # Play Pong
                break
            current_game = "Space Invaders"  # Move to Space Invaders
        elif current_game == "Space Invaders":
            if space_invaders_main() == 'escape':  # Play Pong
                break
            current_game = "Snake"  # Move to Sudoku
        elif current_game == "Snake":
            if snake_main() == 'escape':  # Play Pong
                break
            current_game = "Pong"  # End the experience


if __name__ == "__main__":
    game_transition()

