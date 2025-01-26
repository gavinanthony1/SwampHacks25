import random
import pygame

class Snake:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.fps = 15
        self.grid_size = 20  # cell size for snake and food

        self.cols = self.width // self.grid_size
        self.rows = self.height // self.grid_size

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake')

        # Snake and food settings
        self.snake_pos = [[100, 60], [90, 60], [80, 60]]
        self.snake_direction = 'RIGHT'
        self.change_to = self.snake_direction  # Prevents reverse movement
        self.food_pos = [random.randrange(1, self.cols) * self.grid_size, random.randrange(1, self.rows) * self.grid_size]
        self.food_spawn = True
        self.score = 0

        self.font = pygame.font.SysFont('arial', 25)

    def draw_snake(self):
        # Retro snake
        for block in self.snake_pos:
            pygame.draw.rect(self.screen, self.white, pygame.Rect(block[0], block[1], self.grid_size, self.grid_size))

    def draw_food(self):
        # White cube pretending to be food
        pygame.draw.rect(self.screen, self.white, pygame.Rect(self.food_pos[0], self.food_pos[1], self.grid_size, self.grid_size))

    def game_over(self):
        my_font = pygame.font.SysFont('arial', 50)
        GOsurface = my_font.render(f"Game Over! Your Score: {self.score}", True, self.white)
        GOrect = GOsurface.get_rect()
        GOrect.midtop = (self.width // 2, self.height // 4)
        self.screen.blit(GOsurface, GOrect)
        pygame.display.flip()
        pygame.time.wait(2000)  # wait for 2 seconds before quitting

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Snake controls
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        self.change_to = 'RIGHT'
                    if event.key == pygame.K_2:
                        running = False
                    # To escape the whole program
                    if event.key == pygame.K_ESCAPE:
                        return 'escape'

            # Prevents the snake from reversing on itself
            if self.change_to == 'UP' and self.snake_direction != 'DOWN':
                self.snake_direction = 'UP'
            if self.change_to == 'DOWN' and self.snake_direction != 'UP':
                self.snake_direction = 'DOWN'
            if self.change_to == 'LEFT' and self.snake_direction != 'RIGHT':
                self.snake_direction = 'LEFT'
            if self.change_to == 'RIGHT' and self.snake_direction != 'LEFT':
                self.snake_direction = 'RIGHT'

            # Move snake
            if self.snake_direction == 'UP':
                new_head = [self.snake_pos[0][0], self.snake_pos[0][1] - self.grid_size]
            if self.snake_direction == 'DOWN':
                new_head = [self.snake_pos[0][0], self.snake_pos[0][1] + self.grid_size]
            if self.snake_direction == 'LEFT':
                new_head = [self.snake_pos[0][0] - self.grid_size, self.snake_pos[0][1]]
            if self.snake_direction == 'RIGHT':
                new_head = [self.snake_pos[0][0] + self.grid_size, self.snake_pos[0][1]]

            self.snake_pos.insert(0, new_head)

            # Snake eats food
            if self.snake_pos[0] == self.food_pos:
                self.food_spawn = False
                self.score += 1
            else:
                self.snake_pos.pop()

            # Food respawn
            if not self.food_spawn:
                self.food_pos = [random.randrange(1, self.cols) * self.grid_size, random.randrange(1, self.rows) * self.grid_size]
            self.food_spawn = True

            # Check for collision with boundaries or itself
            if (self.snake_pos[0][0] < 0 or self.snake_pos[0][0] >= self.width or
                    self.snake_pos[0][1] < 0 or self.snake_pos[0][1] >= self.height):
                self.game_over()
                running = False

            for block in self.snake_pos[1:]:
                if block == self.snake_pos[0]:
                    self.game_over()
                    running = False

            # Draw everything
            self.screen.fill(self.black)
            self.draw_snake()
            self.draw_food()

            score_surface = self.font.render(f"Score: {self.score}", True, self.white)
            self.screen.blit(score_surface, (10, 10))

            pygame.display.flip()
            clock.tick(self.fps)


