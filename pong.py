import pygame
import random

pygame.init()

screen_info = pygame.display.Info()
fullscreen_width, fullscreen_height = screen_info.current_w, screen_info.current_h  # Get current screen dimensions

# only part of the screen is played on
width, height = 400, 300

white = (255, 255, 255)
FPS = 60
paddle_width, paddle_height = 10, 60
ball_size = 10
ai_speed = 7
score_limit = 2

screen = pygame.display.set_mode((fullscreen_width, fullscreen_height))  # Full-screen mode
pygame.display.set_caption('Pong')

#  position for the  game area
game_area_x = (fullscreen_width - width) // 2
game_area_y = (fullscreen_height - height) // 2

# Game objects (Player and AI paddles, ball)
player = pygame.Rect(game_area_x + 30, game_area_y + height // 2 - paddle_height // 2, paddle_width, paddle_height)
ai = pygame.Rect(game_area_x + width - 30 - paddle_width, game_area_y + height // 2 - paddle_height // 2, paddle_width, paddle_height)
ball = pygame.Rect(game_area_x + width // 2 - ball_size // 2, game_area_y + height // 2 - ball_size // 2, ball_size, ball_size)
ball_dx, ball_dy = random.choice((1, -1)), random.choice((1, -1))  # Ball direction

player_score = 0
ai_score = 0


def reset_ball():
    """Reset the ball to the center."""
    global ball_dx, ball_dy
    ball.center = (game_area_x + width // 2, game_area_y + height // 2)
    ball_dx, ball_dy = random.choice((1, -1)), random.choice((1, -1))

def move_ai():
    """Move the AI paddle to follow the ball."""
    if ai.centery < ball.centery:
        ai.y += ai_speed
    if ai.centery > ball.centery:
        ai.y -= ai_speed

    # keeps AI paddle within the screen bounds
    if ai.top < game_area_y:
        ai.top = game_area_y
    if ai.bottom > game_area_y + height:
        ai.bottom = game_area_y + height

def display_score():
    """Display the scores on the screen."""
    # render left score
    font_score = pygame.font.Font(None, 100)
    left_text = font_score.render(str(player_score), True, white)
    left_text_rect = left_text.get_rect(center=(fullscreen_width // 4, fullscreen_height // 2))
    screen.blit(left_text, left_text_rect)

    # renders right score
    right_text = font_score.render(str(ai_score), True, white)
    right_text_rect = right_text.get_rect(center=(3 * fullscreen_width // 4, fullscreen_height // 2))
    screen.blit(right_text, right_text_rect)

def render_title():
    # instructions
    font_instructions = pygame.font.Font(None, 30)

    text = font_instructions.render("Spacebar to reset", True, white)
    text_rect = text.get_rect(center=(fullscreen_width // 2, fullscreen_height // 10))
    screen.blit(text, text_rect)

    text = font_instructions.render("U to unpause", True, white)
    text_rect = text.get_rect(center=(fullscreen_width // 2, fullscreen_height // 10 + 50))
    screen.blit(text, text_rect)

    text = font_instructions.render("P to pause", True, white)
    text_rect = text.get_rect(center=(fullscreen_width // 2, fullscreen_height // 10 + 100))
    screen.blit(text, text_rect)

    text = font_instructions.render("Esc to exit", True, white)
    text_rect = text.get_rect(center=(fullscreen_width // 2, fullscreen_height // 10 + 150))
    screen.blit(text, text_rect)


def game_over(winner):
    my_font = pygame.font.SysFont('arial', 50)
    if(winner == "AI"):
        GOsurface = my_font.render(f"You Lose! Your Score: {player_score}", True, white)
    else:
        GOsurface = my_font.render(f"You Win! Your Score: {player_score}", True, white)
    GOrect = GOsurface.get_rect()
    GOrect.midtop = (fullscreen_width // 2, fullscreen_height // 4 + 20)
    screen.blit(GOsurface, GOrect)
    pygame.display.flip()
    pygame.time.wait(2000)  # wait for 2 seconds before quitting
def main():
    global player_score, ai_score, ball_dx, ball_dy

    paused = True
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill((0, 0, 0))

        # draws the white outline for the game area
        pygame.draw.rect(screen, white, (game_area_x, game_area_y, width, height), 5)

        # draws the  instructions
        render_title()

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
            if keys[pygame.K_u]:
                paused = False
        else:
            if keys[pygame.K_UP] and player.top > game_area_y:
                player.y -= 5
            if keys[pygame.K_DOWN] and player.bottom < game_area_y + height:
                player.y += 5

            if keys[pygame.K_p]:
                paused = True

            if keys[pygame.K_SPACE]:
                reset_ball()
            # Move ai paddle
            move_ai()

            # ball movement
            ball.x += ball_dx * 5
            ball.y += ball_dy * 5

            # ball collision with top and bottom walls
            if ball.top <= game_area_y or ball.bottom >= game_area_y + height:
                ball_dy *= -1

            # ball collision with paddles
            if ball.colliderect(player) or ball.colliderect(ai):
                ball_dx *= -1

            # scoring system
            if ball.left <= game_area_x:  # AI scores
                ai_score += 1
                if ai_score >= score_limit:
                    game_over("AI")
                    running = False
                reset_ball()
            if ball.right >= game_area_x + width:  # Player scores
                player_score += 1
                if player_score >= score_limit:
                    game_over("player")
                    running = False
                reset_ball()

        # draws paddles, ball, and score
        pygame.draw.rect(screen, white, player)
        pygame.draw.rect(screen, white, ai)
        pygame.draw.ellipse(screen, white, ball)

        display_score()

        # no idea what this does but breaks it if it doesn't have it
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
