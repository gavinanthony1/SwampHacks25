import pygame
import random


class Pong:
    def __init__(self, fullscreen_width, fullscreen_height):
        self.fullscreen_width = fullscreen_width
        self.fullscreen_height = fullscreen_height
        # only part of the screen is played on
        self.width = 400
        self.height = 300

        self.white = (255, 255, 255)
        self.FPS = 60
        self.paddle_width = 10
        self.paddle_height = 60
        self.ball_size = 10
        self.ai_speed = 7
        self.score_limit = 10
        self.player_score = 0
        self.ai_score = 0
        #  position for the  game area
        self.game_area_x = (self.fullscreen_width - self.width) // 2
        self.game_area_y = (self.fullscreen_height - self.height) // 2

        # Game objects (Player and AI paddles, ball)
        self.player = pygame.Rect(self.game_area_x + 30, self.game_area_y + self.height // 2 - self.paddle_height // 2,
                                  self.paddle_width,
                                  self.paddle_height)
        self.ai = pygame.Rect(self.game_area_x + self.width - 30 - self.paddle_width,
                              self.game_area_y + self.height // 2 - self.paddle_height // 2,
                              self.paddle_width, self.paddle_height)
        self.ball = pygame.Rect(self.game_area_x + self.width // 2 - self.ball_size // 2,
                                self.game_area_y + self.height // 2 - self.ball_size // 2,
                                self.ball_size, self.ball_size)
        self.ball_dx = random.choice((1, -1))
        self.ball_dy = random.choice((1, -1))  # Ball direction

    def reset_ball(self):
        self.ball.center = (self.game_area_x + self.width // 2, self.game_area_y + self.height // 2)
        self.ball_dx, self.ball_dy = random.choice((1, -1)), random.choice((1, -1))

    def move_ai(self):
        if self.ai.centery < self.ball.centery:
            self.ai.y += self.ai_speed
        if self.ai.centery > self.ball.centery:
            self.ai.y -= self.ai_speed

        # keeps AI paddle within the screen bounds
        if self.ai.top < self.game_area_y:
            self.ai.top = self.game_area_y
        if self.ai.bottom > self.game_area_y + self.height:
            self.ai.bottom = self.game_area_y + self.height

    def display_score(self):
        # render left score
        font_score = pygame.font.Font(None, 100)
        left_text = font_score.render(str(self.player_score), True, self.white)
        left_text_rect = left_text.get_rect(center=(self.fullscreen_width // 4, self.fullscreen_height // 2))
        self.screen.blit(left_text, left_text_rect)

        # renders right score
        right_text = font_score.render(str(self.ai_score), True, self.white)
        right_text_rect = right_text.get_rect(center=(3 * self.fullscreen_width // 4, self.fullscreen_height // 2))
        self.screen.blit(right_text, right_text_rect)

    def render_title(self):
        # instructions
        font_instructions = pygame.font.Font(None, 30)

        text = font_instructions.render("Spacebar to start/reset", True, self.white)
        text_rect = text.get_rect(center=(self.fullscreen_width // 2, self.fullscreen_height // 10))
        self.screen.blit(text, text_rect)

    def game_over(self, winner):
        my_font = pygame.font.SysFont('arial', 50)
        if (winner == "AI"):
            GOsurface = my_font.render(f"You Lose! Your Score: {self.player_score}", True, self.white)
        else:
            GOsurface = my_font.render(f"You Win! Your Score: {self.player_score}", True, self.white)
        GOrect = GOsurface.get_rect()
        GOrect.midtop = (self.fullscreen_width // 2, self.fullscreen_height // 4 + 20)
        self.screen.blit(GOsurface, GOrect)
        pygame.display.flip()
        pygame.time.wait(2000)  # wait for 2 seconds before quitting

    def run(self):
        self.screen = pygame.display.set_mode((self.fullscreen_width, self.fullscreen_height))  # Full-screen mode
        pygame.display.set_caption('Pong')

        #  position for the  game area
        self.game_area_x = (self.fullscreen_width - self.width) // 2
        self.game_area_y = (self.fullscreen_height - self.height) // 2

        paused = True
        clock = pygame.time.Clock()
        running = True
        while running:
            self.screen.fill((0, 0, 0))

            # draws the white outline for the game area
            pygame.draw.rect(self.screen, self.white, (self.game_area_x, self.game_area_y, self.width, self.height), 5)

            # draws the  instructions
            self.render_title()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            # to escape to the next game
            if keys[pygame.K_1]:
                running = False

            # to escape the whole program
            if keys[pygame.K_ESCAPE]:
                return 'escape'

            if paused:
                if keys[pygame.K_SPACE]:
                    paused = False
            else:
                if keys[pygame.K_UP] and self.player.top > self.game_area_y:
                    self.player.y -= 5
                if keys[pygame.K_DOWN] and self.player.bottom < self.game_area_y + self.height:
                    self.player.y += 5

                if keys[pygame.K_SPACE]:
                    self.reset_ball()
                # Move ai paddle
                self.move_ai()

                # ball movement
                self.ball.x += self.ball_dx * 5
                self.ball.y += self.ball_dy * 5

                # ball collision with top and bottom walls
                if self.ball.top <= self.game_area_y or self.ball.bottom >= self.game_area_y + self.height:
                    self.ball_dy *= -1

                # ball collision with paddles
                if self.ball.colliderect(self.player) or self.ball.colliderect(self.ai):
                    self.ball_dx *= -1

                # scoring system
                if self.ball.left <= self.game_area_x:  # AI scores
                    self.ai_score += 1
                    if self.ai_score >= self.score_limit:
                        self.game_over("AI")
                        running = False
                    self.reset_ball()
                if self.ball.right >= self.game_area_x + self.width:  # Player scores
                    self.player_score += 1
                    if self.player_score >= self.score_limit:
                        self.game_over("player")
                        running = False
                    self.reset_ball()

            # draws paddles, ball, and score
            pygame.draw.rect(self.screen, self.white, self.player)
            pygame.draw.rect(self.screen, self.white, self.ai)
            pygame.draw.ellipse(self.screen, self.white, self.ball)

            self.display_score()

            # no idea what this does but breaks it if it doesn't have it
            pygame.display.flip()
            clock.tick(self.FPS)

