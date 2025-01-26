import pygame

class SpaceInvaders:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Game settings
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.FPS = 60
        self.player_speed = 5
        self.bullet_speed = 7
        self.alien_speed = 1
        self.num_aliens = 13

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Space Invaders')

        self.font = pygame.font.Font(None, 36)

        # Player settings
        self.player_width, self.player_height = 50, 50
        self.player = pygame.Rect(self.width // 2 - self.player_width // 2, self.height - self.player_height - 10, self.player_width, self.player_height)
        self.player_image = pygame.Surface((self.player_width, self.player_height))
        self.player_image.fill(self.white)

        # Bullets
        self.bullet_width, self.bullet_height = 5, 10
        self.bullets = []

        # Aliens
        self.alien_width, self.alien_height = 40, 40
        self.aliens = []
        for i in range(self.num_aliens):
            alien = pygame.Rect(100 * (i + 1), 50, self.alien_width, self.alien_height)
            self.aliens.append(alien)

        self.alien_image = pygame.Surface((self.alien_width, self.alien_height))
        self.alien_image.fill(self.white)

        self.score = 0

    def move_player(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player.left > 0:
            self.player.x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player.right < self.width:
            self.player.x += self.player_speed

    def shoot_bullet(self):
        bullet = pygame.Rect(self.player.centerx - self.bullet_width // 2, self.player.top, self.bullet_width, self.bullet_height)
        self.bullets.append(bullet)

    def move_bullets(self):
        for bullet in self.bullets[:]:
            bullet.y -= self.bullet_speed
            if bullet.bottom < 0:
                self.bullets.remove(bullet)

    def move_aliens(self):
        for alien in self.aliens:
            alien.y += self.alien_speed

    def check_collisions(self):
        for bullet in self.bullets[:]:
            for alien in self.aliens[:]:
                # Check for collisions
                if bullet.colliderect(alien):
                    self.bullets.remove(bullet)
                    self.aliens.remove(alien)
                    self.score += 1
                    return True
        return False

    def display_score(self):
        score_text = self.font.render(f'Score: {self.score}', True, self.white)
        self.screen.blit(score_text, (10, 10))

    def game_over(self):
        my_font = pygame.font.SysFont('arial', 50)
        GOsurface = my_font.render(f"Game Over! Your Score: {self.score}", True, self.white)
        GOrect = GOsurface.get_rect()
        GOrect.midtop = (self.width // 2, self.height // 4)
        self.screen.blit(GOsurface, GOrect)
        pygame.display.flip()
        pygame.time.wait(1000)  # Wait for 2 seconds before quitting

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.screen.fill(self.black)

            self.move_player()
            self.move_bullets()
            self.move_aliens()
            collision_occurred = self.check_collisions()

            # Draw player and aliens
            self.screen.blit(self.player_image, self.player)
            for bullet in self.bullets:
                pygame.draw.rect(self.screen, self.white, bullet)
            for alien in self.aliens:
                self.screen.blit(self.alien_image, alien)

            self.display_score()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.shoot_bullet()
                    if event.key == pygame.K_2:
                        running = False
                    # To escape the whole program
                    if event.key == pygame.K_ESCAPE:
                        return 'escape'

            if collision_occurred:
                self.alien_speed = 1

            # AI might increase the alien speed if the player is doing well
            if len(self.aliens) < self.num_aliens // 2:
                self.alien_speed = 2

            # If hit by alien
            for alien in self.aliens[:]:
                if self.player.colliderect(alien):
                    self.game_over()
                    running = False

            # Ends game if aliens reach the bottom
            for alien in self.aliens:
                if alien.bottom >= self.height + 40:
                    self.game_over()
                    running = False

            if len(self.aliens) == 0:
                self.game_over()
                running = False

            pygame.display.flip()
            clock.tick(self.FPS)

