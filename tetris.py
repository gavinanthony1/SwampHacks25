import pygame
import random

class Tetris:
    def __init__(self, width, height, difficulty, play_width_ratio=0.5, play_height_ratio=0.5):
        self.width = width
        self.height = height
        self.play_width = 300
        self.play_height = 600
        self.grid_size = 30
        self.cols = self.play_width // self.grid_size
        self.rows = self.play_height // self.grid_size
        self.fps = 10 + (difficulty * 4)
        self.difficulty = difficulty

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Tetris')

        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.tetrominoes = [
            [[1, 1, 1, 1]],  # Line
            [[1, 1], [1, 1]],  # Square
            [[0, 1, 0], [1, 1, 1]],  # T-shape
            [[1, 1, 0], [0, 1, 1]],  # Z-shape
            [[0, 1, 1], [1, 1, 0]],  # S-shape
            [[1, 0, 0], [1, 1, 1]],  # L-shape
            [[0, 0, 1], [1, 1, 1]]   # J-shape
        ]
        self.current_piece = self.get_new_piece()
        self.current_pos = [0, self.cols // 2 - len(self.current_piece[0]) // 2]
        self.score = 0
        self.font = pygame.font.SysFont('arial', 25)

    def get_new_piece(self):
        return random.choice(self.tetrominoes)

    def rotate_piece(self):
        rotated = list(zip(*self.current_piece[::-1]))
        if not self.check_collision(offset=(0, 0), piece=rotated):
            self.current_piece = [list(row) for row in rotated]

    def draw_grid(self):
        play_start_x = (self.width - self.play_width) // 2
        play_start_y = (self.height - self.play_height) // 2
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.white, pygame.Rect(
                        play_start_x + x * self.grid_size,
                        play_start_y + y * self.grid_size,
                        self.grid_size, self.grid_size))
                pygame.draw.rect(self.screen, self.black, pygame.Rect(
                    play_start_x + x * self.grid_size,
                    play_start_y + y * self.grid_size,
                    self.grid_size, self.grid_size), 1)

    def draw_piece(self):
        play_start_x = (self.width - self.play_width) // 2
        play_start_y = (self.height - self.play_height) // 2
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, self.white, pygame.Rect(
                        play_start_x + (self.current_pos[1] + x) * self.grid_size,
                        play_start_y + (self.current_pos[0] + y) * self.grid_size,
                        self.grid_size, self.grid_size))

    def draw_walls(self):
        play_start_x = (self.width - self.play_width) // 2
        play_start_y = (self.height - self.play_height) // 2
        pygame.draw.rect(self.screen, self.white, pygame.Rect(
            play_start_x - 5, play_start_y, 5, self.play_height))  # Left wall
        pygame.draw.rect(self.screen, self.white, pygame.Rect(
            play_start_x + self.play_width, play_start_y, 5, self.play_height))  # Right wall
        pygame.draw.rect(self.screen, self.white, pygame.Rect(
            play_start_x - 5, play_start_y + self.play_height, self.play_width + 10, 5))  # Bottom wall

    def check_collision(self, offset=(0, 0), piece=None):
        if piece is None:
            piece = self.current_piece
        off_y, off_x = offset
        for y, row in enumerate(piece):
            for x, cell in enumerate(row):
                if cell:
                    new_y = y + self.current_pos[0] + off_y
                    new_x = x + self.current_pos[1] + off_x
                    if new_x < 0 or new_x >= self.cols or new_y >= self.rows:
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_pos[0] + y][self.current_pos[1] + x] = 1

    def clear_lines(self):
        cleared = 0
        self.grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        cleared = self.rows - len(self.grid)
        self.grid = [[0] * self.cols for _ in range(cleared)] + self.grid
        self.score += cleared

    def game_over(self):
        for cell in self.grid[0]:
            if cell:
                return True
        return False

    def run(self):
        clock = pygame.time.Clock()
        running = True
        fall_time = 0

        while running:
            self.screen.fill(self.black)
            fall_time += clock.get_rawtime()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.rotate_piece()
                    if event.key == pygame.K_LEFT:
                        if not self.check_collision((0, -1)):
                            self.current_pos[1] -= 1
                    if event.key == pygame.K_RIGHT:
                        if not self.check_collision((0, 1)):
                            self.current_pos[1] += 1
                    if event.key == pygame.K_4:
                        running = False
                        return self.difficulty
                    if event.key == pygame.K_ESCAPE:
                        return 'escape'

            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                if not self.check_collision((1, 0)):
                    self.current_pos[0] += 1


            if fall_time > 1000 / self.fps:
                if not self.check_collision((1, 0)):
                    self.current_pos[0] += 1
                else:
                    self.merge_piece()
                    self.clear_lines()
                    if self.game_over():
                        return self.difficulty - 1 if self.score < 5 else self.difficulty + 1
                    self.current_piece = self.get_new_piece()
                    self.current_pos = [0, self.cols // 2 - len(self.current_piece[0]) // 2]
                fall_time = 0

            self.draw_grid()
            self.draw_piece()
            self.draw_walls()

            score_surface = self.font.render(f"Score: {self.score}", True, self.white)
            self.screen.blit(score_surface, (10, 10))
            difficulty_surface = self.font.render(f"Difficulty: {self.difficulty}", True, self.white)
            self.screen.blit(difficulty_surface, (10, 40))

            pygame.display.flip()
            clock.tick(self.fps)
