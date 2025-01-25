import random
import pygame

pygame.init()

screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h
white = (255, 255, 255)
black = (0, 0, 0)
fps = 15
grid_size = 20  # cell size for snake and food

cols = width // grid_size
rows = height // grid_size

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')

# Snake and food settings
snake_pos = [[100, 60], [90, 60], [80, 60]]
snake_direction = 'RIGHT'
# Prevents reverse movement
change_to = snake_direction
food_pos = [random.randrange(1, cols) * grid_size, random.randrange(1, rows) * grid_size]
food_spawn = True
score = 0

font = pygame.font.SysFont('arial', 25)


def draw_snake(snake_body):
    # retro snake
    for block in snake_body:
        pygame.draw.rect(screen, white, pygame.Rect(block[0], block[1], grid_size, grid_size))


def draw_food(food_pos):
    # white cube pretending to be food
    pygame.draw.rect(screen, white, pygame.Rect(food_pos[0], food_pos[1], grid_size, grid_size))


def game_over():
    my_font = pygame.font.SysFont('arial', 50)
    GOsurface = my_font.render(f"Game Over! Your Score: {score}", True, white)
    GOrect = GOsurface.get_rect()
    GOrect.midtop = (width // 2, height // 4)
    screen.blit(GOsurface, GOrect)
    pygame.display.flip()
    pygame.time.wait(2000)  # wait for 2 seconds before quitting



def main():
    global snake_pos, snake_direction, food_pos, food_spawn, score, change_to

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # snake controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_2:
                    running = False
                # to escape the whole program
                if event.key == pygame.K_ESCAPE:
                    return 'escape'

        # Prevents the snake from reversing on itself
        if change_to == 'UP' and snake_direction != 'DOWN':
            snake_direction = 'UP'
        if change_to == 'DOWN' and snake_direction != 'UP':
            snake_direction = 'DOWN'
        if change_to == 'LEFT' and snake_direction != 'RIGHT':
            snake_direction = 'LEFT'
        if change_to == 'RIGHT' and snake_direction != 'LEFT':
            snake_direction = 'RIGHT'

        # move snake
        if snake_direction == 'UP':
            new_head = [snake_pos[0][0], snake_pos[0][1] - grid_size]
        if snake_direction == 'DOWN':
            new_head = [snake_pos[0][0], snake_pos[0][1] + grid_size]
        if snake_direction == 'LEFT':
            new_head = [snake_pos[0][0] - grid_size, snake_pos[0][1]]
        if snake_direction == 'RIGHT':
            new_head = [snake_pos[0][0] + grid_size, snake_pos[0][1]]

        snake_pos.insert(0, new_head)

        # Snake eats food
        if snake_pos[1] == food_pos:
            food_spawn = False
            score += 1
        else:
            snake_pos.pop()


        # Food respawn
        if not food_spawn:
            food_pos = [random.randrange(1, cols) * grid_size, random.randrange(1, rows) * grid_size]
        food_spawn = True

        # Check for collision with boundaries or itself
        if snake_pos[0][0] < 0 or snake_pos[0][0] >= width or snake_pos[0][1] < 0 or snake_pos[0][1] >= height:
            game_over()
            running = False
        for block in snake_pos[1:]:
            if block == snake_pos[0]:
                game_over()
                running = False

        # Draw everything
        screen.fill(black)
        draw_snake(snake_pos)
        draw_food(food_pos)

        score_surface = font.render(f"Score: {score}", True, white)
        screen.blit(score_surface, (10, 10))

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    main()
