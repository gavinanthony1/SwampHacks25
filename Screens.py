import pygame
import sys
import os


class game_screens:
    def __init__(self, leaderboard_file="leaderboard.txt"):
        self.leaderboard_file = leaderboard_file
        self.leaderboard = self.load_leaderboard()

    # loads leaderbaord from file
    def load_leaderboard(self):
        if not os.path.exists(self.leaderboard_file):
            return []
        with open(self.leaderboard_file, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]

    def save_leaderboard(self):
        with open(self.leaderboard_file, "w") as file:
            for name, score in self.leaderboard:
                file.write(f"{name},{score}\n")

    def update_leaderboard(self, player_name, score):
        self.leaderboard.append((player_name, score))
        self.leaderboard.sort(key=lambda x: int(x[1]), reverse=True)
        self.leaderboard = self.leaderboard[:20]  # Keep only top 20 scores

    def display_leaderboard(self, screen, width, height):
        font = pygame.font.Font(None, 50)
        title = font.render("Leaderboard", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(width // 2, 50)))

        font = pygame.font.Font(None, 30)
        for i, (name, score) in enumerate(self.leaderboard):
            text = font.render(f"{i + 1}. {name} - {score}", True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=(width // 2, 100 + i * 40)))

    def welcome_screen(self):
        pygame.init()
        screen_info = pygame.display.Info()
        width, height = screen_info.current_w, screen_info.current_h
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Welcome Screen")

        font_title = pygame.font.Font(None, 80)
        font_text = pygame.font.Font(None, 50)
        font_input = pygame.font.Font(None, 40)

        clock = pygame.time.Clock()
        input_active = False
        player_name = "Player"
        input_text = ""

        while True:
            screen.fill((0, 0, 0))

            title = font_title.render("Welcome to Four Quarters!", True, (255, 255, 0))
            screen.blit(title, title.get_rect(center=(width // 2, 100)))

            instructions = [
                "Controls:",
                "Arrow Keys - Move",
                "Spacebar - Action",
                "Esc - Exit",
                "Available Games:",
                "Pong, Space Invaders, Snake, Tetris",
                "",
                "**The title is called that because arcade games take quarters",
                "and there's four games and it was 4 in the morning when I wrote this**"
            ]

            for i, line in enumerate(instructions):
                text = font_text.render(line, True, (255, 255, 255))
                screen.blit(text, text.get_rect(center=(width // 2, 200 + i * 50)))

            # name box
            name_prompt = font_text.render("Enter Your Name: ", True, (255, 255, 255))
            screen.blit(name_prompt, (width // 2 - 300, height - 200))

            input_color = (0, 255, 0) if input_active else (255, 255, 255)
            input_box = pygame.Rect(width // 2, height - 210, 400, 50)
            pygame.draw.rect(screen, input_color, input_box, 2)

            name_surface = font_input.render(input_text or player_name, True, (255, 255, 255))
            screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

            # game instructions to proceed
            start_text = font_text.render("Press Enter to Start", True, (255, 255, 255))
            screen.blit(start_text, start_text.get_rect(center=(width // 2, height - 100)))

            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if input_active:
                        if event.key == pygame.K_RETURN:
                            if input_text.strip():
                                player_name = input_text.strip()
                            return player_name
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        elif len(input_text) < 20:  # limited to 20 characters
                            input_text += event.unicode
                    else:
                        if event.key == pygame.K_RETURN:
                            return player_name

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        input_active = not input_active

            clock.tick(30)



