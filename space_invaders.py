import pygame

class SpaceInvaders:
    def __init__(self, width, height, difficulty):
        self.width = width
        self.height = height
        # Game settings
        self.difficulty = difficulty
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.FPS = 60
        self.player_speed = difficulty
        self.bullet_speed = 7
        self.alien_speed = 1
        self.num_aliens = difficulty * 3

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
        self.alien_padding = 20  # Space between aliens
        self.aliens = []
        self.create_alien_formation()

        self.alien_image = pygame.Surface((self.alien_width, self.alien_height))
        self.alien_image.fill(self.white)

        self.score = 0

    def create_alien_formation(self):
        self.aliens = []  # Clear existing aliens
        max_aliens_per_row = 20  # Maximum aliens in a single row
        alien_spacing_x = 30  # Horizontal space between aliens
        alien_spacing_y = 30  # Vertical space between rows

        # Number of rows and columns required
        num_rows = (self.num_aliens + max_aliens_per_row - 1) // max_aliens_per_row
        remaining_aliens = self.num_aliens

        for row in range(num_rows):
            # Determine how many aliens go in this row
            aliens_in_row = min(remaining_aliens, max_aliens_per_row)
            remaining_aliens -= aliens_in_row

            # Calculate the total width of this row of aliens
            row_width = (aliens_in_row * self.alien_width) + ((aliens_in_row - 1) * alien_spacing_x)

            # Center the row horizontally
            start_x = (self.width - row_width) // 2
            start_y = 50 + row * (self.alien_height + alien_spacing_y)

            for col in range(aliens_in_row):
                x = start_x + col * (self.alien_width + alien_spacing_x)
                y = start_y
                alien = pygame.Rect(x, y, self.alien_width, self.alien_height)
                self.aliens.append(alien)

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
        score_text = self.font.render(f'Difficulty: {self.difficulty}', True, self.white)
        self.screen.blit(score_text, (10, 40))

    def game_over(self):
        my_font = pygame.font.SysFont('arial', 50)
        GOsurface = my_font.render(f"Game Over! Your Score: {self.score}", True, self.white)
        GOrect = GOsurface.get_rect()
        GOrect.midtop = (self.width // 2, self.height // 4)
        self.screen.blit(GOsurface, GOrect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds before quitting
        if self.score == self.num_aliens:
            return self.difficulty + 1
        else:
            return self.difficulty - 1

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
                        return self.difficulty
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
                    running = False
                    return self.game_over()

            # Ends game if aliens reach the bottom
            for alien in self.aliens:
                if alien.bottom >= self.height + 40:
                    running = False
                    return self.game_over()

            if len(self.aliens) == 0:
                running = False
                return self.game_over()

            pygame.display.flip()
            clock.tick(self.FPS)
