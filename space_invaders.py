import pygame
from ai_module import get_ai_response

pygame.init()

screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h  # Get current screen dimensions


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space Invaders')

# game settings
white = (255, 255, 255)
black = (0, 0, 0)
FPS = 60
player_speed = 5
bullet_speed = 7
alien_speed = 1
num_aliens = 13

font = pygame.font.Font(None, 36)

# player settings
player_width, player_height = 50, 50
player = pygame.Rect(width // 2 - player_width // 2, height - player_height - 10, player_width, player_height)
player_image = pygame.Surface((player_width, player_height))
player_image.fill(white)

# bullets
bullet_width, bullet_height = 5, 10
bullets = []

# aliens
alien_width, alien_height = 40, 40
aliens = []

score = 0
for i in range(num_aliens):
    alien = pygame.Rect(100 * (i + 1), 50, alien_width, alien_height)
    aliens.append(alien)

alien_image = pygame.Surface((alien_width, alien_height))
alien_image.fill(white)

def move_player():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < width:
        player.x += player_speed

def shoot_bullet():
    bullet = pygame.Rect(player.centerx - bullet_width // 2, player.top, bullet_width, bullet_height)
    bullets.append(bullet)

def move_bullets():
    global bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)

def move_aliens():
    global aliens
    for alien in aliens:
        alien.y += alien_speed

def check_collisions():
    global bullets, aliens, score
    for bullet in bullets[:]:
        for alien in aliens[:]:
            # check for collisions
            if bullet.colliderect(alien):
                bullets.remove(bullet)
                aliens.remove(alien)
                score += 1
                return True
    return False

def get_ai_advice():
    """Ask the AI for advice on the game (hopefully)."""
    ai_response = get_ai_response({"game": "Space Invaders", "aliens": len(aliens), "bullets": len(bullets)})
    return ai_response

def display_score():
    score_text = font.render(f'Score: {score}', True, white)
    screen.blit(score_text, (10, 10))



def game_over():
    my_font = pygame.font.SysFont('arial', 50)
    GOsurface = my_font.render(f"Game Over! Your Score: {score}", True, white)
    GOrect = GOsurface.get_rect()
    GOrect.midtop = (width // 2, height // 4)
    screen.blit(GOsurface, GOrect)
    pygame.display.flip()
    pygame.time.wait(1000)  # wait for 2 seconds before quitting

def main():
    global bullets, aliens
    clock = pygame.time.Clock()
    running = True
    while running:
        screen.fill(black)

        move_player()
        move_bullets()
        move_aliens()
        collision_occurred = check_collisions()

        # Draw player and aliens
        screen.blit(player_image, player)
        for bullet in bullets:
            pygame.draw.rect(screen, white, bullet)
        for alien in aliens:
            screen.blit(alien_image, alien)

        display_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_bullet()
                if event.key == pygame.K_2:
                    running = False
                # to escape the whole program
                if event.key == pygame.K_ESCAPE:
                    return 'escape'

        if collision_occurred:
            global alien_speed
            alien_speed = 1
        # AI might increase the alien speed if player is doing good (maybe probably not going to work)
        if len(aliens) < num_aliens // 2:
            alien_speed = 2

        # if hit by alien
        for alien in aliens[:]:
            # check for collisions
            if player.colliderect(alien):
                game_over()
                running = False
        # ends game if aliens reach the bottom
        for alien in aliens:
            if alien.bottom >= height + 40:
                game_over()
                running = False

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
