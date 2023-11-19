import os
import sys
import random
from time import sleep
import pygame
from pygame.sprite import Sprite, Group


# Game Classes
class Settings:
    """A class to handle the game settings."""
    def __init__(self):
        # screen
        self.screen_width = 1100
        self.screen_height = 600
        self.bg_color = (103, 178, 255)

        # ship
        self.ship_speed = 7
        self.ship_lives = 3

        # bullet
        self.bullet_speed = 8
        self.bullet_width = 20
        self.bullet_height = 7
        self.bullet_color = (255, 60, 60)

        # obstacles
        self.obs_speed = 6

        # game settings
        self.game_speed = 10

        # scoring
        self.points = 10


class Ship(Sprite):
    """Add ship to game and handle its positioning."""
    def __init__(self, settings, screen):
        super().__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load(os.path.join("images/ship", "ship.png"))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centery = self.screen_rect.centery
        self.rect.centerx = self.screen_rect.centerx / 2
        self.speed = self.settings.ship_speed
        self.move_down = False
        self.move_up = False

        self.center = float(self.rect.centery)

    def update(self):
        if self.move_down and (self.rect.bottom < self.screen_rect.bottom):
            self.center += self.speed
        if self.move_up and (self.rect.top > 0):
            self.center -= self.speed

        self.rect.centery = self.center

    def reset_ship_pos(self):
        self.center = self.screen_rect.centery

    def draw(self):
        self.screen.blit(self.image, self.rect)


class Bullet(Sprite):
    """Create bullets for the ship."""
    def __init__(self, settings, screen, ship):
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.centery = ship.rect.centery
        self.rect.centerx = ship.rect.centerx
        self.x = float(self.rect.x)
        self.color = settings.bullet_color
        self.speed = settings.bullet_speed

    def update(self):
        self.x += self.speed
        self.rect.x = self.x

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)


class Obstacles(Sprite):
    """Add obstacles to the game and handle them."""
    def __init__(self, settings, screen, filename):
        super().__init__()
        self.settings = settings
        self.screen = screen
        self.x = settings.screen_width + random.randint(2000, 3000)
        self.y = random.randint(250, 450)
        self.image = pygame.image.load(os.path.join("images/obstacles", filename))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.width = self.image.get_width()
        self.speed = settings.obs_speed

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x
        if self.x < -self.width:
            self.x = self.settings.screen_width + random.randint(2000, 3000)
            self.y = random.randint(250, 450)

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))


class Clouds:
    """A class to add and handle clouds in the game."""
    def __init__(self, settings, screen, filename):
        self.settings = settings
        self.screen = screen
        self.x = settings.screen_width + random.randint(1000, 2000)
        self.y = random.randint(20, 50)
        self.image = pygame.image.load(os.path.join("images/cloud", filename))
        self.width = self.image.get_width()
        self.speed = settings.game_speed

    def update(self):
        self.x -= self.settings.game_speed
        if self.x < -self.width:
            self.x = self.settings.screen_width + random.randint(1000, 2000)
            self.y = random.randint(20, 50)

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))


class GameStats:
    """Track the game statistics."""
    def __init__(self, settings):
        """Initialize statistics."""
        self.settings = settings
        self.reset_stats()

        # start game in an inactive state.
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_lives
        self.score = 0


class Button:
    """A class to handle the play button in the game."""
    def __init__(self, screen, msg):
        """Initialize button"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # set the dimensions and properties of the button.
        self.width = 200
        self.height = 50
        self.button_color = (0, 30, 100)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once.
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)


class Scoreboard:
    """A class to report scoring information."""
    def __init__(self, settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        # font settings for scoring information.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # prepare the initial score image.
        self.prep_score()

        self.prep_ships("heart.png")

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color,
                                            self.settings.bg_color)

        # display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_ships(self, filename):
        """Show how many ships are left."""
        self.ships = Group()

        ship_image = pygame.image.load(os.path.join("images/ship", filename))

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            ship.image = ship_image
            self.ships.add(ship)

    def draw(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.ships.draw(self.screen)


# Game Functions
def run_game():
    """Handle all game events."""
    settings = Settings()

    pygame.init()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Air Shooter")
    clock = pygame.time.Clock()

    ship = Ship(settings, screen)
    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)
    bullets = Group()
    obstacles = Group(
        Obstacles(settings, screen, "bird.png"),
        Obstacles(settings, screen, "emerald.png"),
        Obstacles(settings, screen, "bird1.png"),
        Obstacles(settings, screen, "box.png")
    )

    clouds = [
        Clouds(settings, screen, "cloud1.png"),
        Clouds(settings, screen, "cloud2.png")
    ]

    play_button = Button(screen, "Start")

    # event loop
    running = True

    while running:
        clock.tick(60)  # limit game to 60 fps

        key_mouse_events(settings, screen, ship, bullets, obstacles, stats, play_button, sb)
        update_screen(settings, screen, ship, bullets, obstacles, clouds, stats, sb, play_button)

        if stats.game_active:
            ship.update()
            update_bullets(settings, screen, bullets, obstacles, stats, sb)
            obstacles.update()
            update_obstacles(settings, screen, ship, obstacles, bullets, stats, sb)
            bullets.update()

            for cloud in clouds:
                cloud.update()


def key_mouse_events(settings, screen, ship, bullets, obstacles, stats, play_button, sb):
    """Function to handle all keypresses and mouse clicks."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, ship, bullets, obstacles,
                              stats, play_button, mouse_x, mouse_y, sb)

        # handle ship control
        ## keydown events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                ship.move_down = True
            elif event.key == pygame.K_UP:
                ship.move_up = True
            elif event.key == pygame.K_SPACE:
                # fire bullets
                bullet = Bullet(settings, screen, ship)
                bullets.add(bullet)

        ## keyup events
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                ship.move_down = False
            elif event.key == pygame.K_UP:
                ship.move_up = False


def update_screen(settings, screen, ship, bullets, obstacles, clouds, stats, score, play_button):
    """Function to handle game screen activity."""
    screen.fill(settings.bg_color)
    ship.draw()

    for cloud in clouds:
        cloud.draw()

    for obstacle in obstacles.sprites():
        obstacle.draw()

    for bullet in bullets.sprites():
        bullet.draw()

    score.draw()

    if not stats.game_active:
        play_button.draw()

    pygame.display.flip()


def update_bullets(settings, screen, bullets, obstacles, stats, sb):
    """Function to handle bullets activity."""
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.left <= 0:
            bullets.remove(bullet)

    # check for and get rid of bullet-obstacle collision
    collisions = pygame.sprite.groupcollide(bullets, obstacles, True, True)

    if collisions:
        stats.score += settings.points
        sb.prep_score()

    if len(obstacles) == 0:
        # remove existing bullets and add new obstacles
        bullets.empty()
        add_new_obstacles(settings, screen, obstacles)


def update_obstacles(settings, screen, ship, obstacles, bullets, stats, sb):
    """Update position of obstacles and check for ship-obstacle collision."""
    obstacles.update()
    if pygame.sprite.spritecollideany(ship, obstacles):
        # respond to ship being being hit by obstacle
        if stats.ships_left > 0:
            # decrement ships left after being hit
            stats.ships_left -= 1

            # update scoreboard
            sb.prep_ships("heart.png")

            # empty the list of bullets and obstacles
            bullets.empty()
            obstacles.empty()

            # add new obstacles and reset ship's position
            add_new_obstacles(settings, screen, obstacles)
            ship.reset_ship_pos()

            # pause for effect
            sleep(0.3)
        else:
            stats.game_active = False
            pygame.mouse.set_visible(1)  # show mouse cursor


def add_new_obstacles(settings, screen, obstacles):
    """Add new obstacles to game screen for every obstacle shot."""
    obstacles.add(Obstacles(settings, screen, "bird.png"))
    obstacles.add(Obstacles(settings, screen, "emerald.png"))
    obstacles.add(Obstacles(settings, screen, "bird1.png"))
    obstacles.add(Obstacles(settings, screen, "box.png"))


def check_play_button(settings, screen, ship, bullets, obstacles,
                      stats, play_button, mouse_x, mouse_y, sb):
    """Function to handle mouse clicks to start the game."""

    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        pygame.mouse.set_visible(0)  # hide the mouse cursor
        stats.reset_stats()  # reset game stats
        stats.game_active = True

        # empty the list of bullets and obstacles
        bullets.empty()
        obstacles.empty()

        # add new obstacles and reset ship's position
        add_new_obstacles(settings, screen, obstacles)
        ship.reset_ship_pos()

        # reset the scoreboard images
        sb.prep_score()
        sb.prep_ships("heart.png")


def main():
    run_game()


if __name__ == "__main__":
    main()
