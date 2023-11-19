import pygame
from project import *
from unittest.mock import MagicMock
pygame.init()


# create mock events for each arguments of each function to test
class SettingsMock:
    def __init__(self):
        self.screen_width = 1100
        self.screen_height = 600
        self.bg_color = (103, 178, 255)
        self.ship_speed = 7
        self.ship_lives = 3
        self.bullet_speed = 8
        self.bullet_width = 20
        self.bullet_height = 7
        self.bullet_color = (255, 60, 60)
        self.obs_speed = 6
        self.game_speed = 9
        self.points = True

class ScreenMock:
    def __init__(self):
        self.fill_called_with = None

    def fill(self, color):
        self.fill_called_with = color

class ShipMock:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.move_down = False
        self.move_up = False

    def reset_ship_pos(self):
        pass

    def draw(self):
        self.draw_called = True

class BulletsMock:
    def __init__(self):
        self.sprites = []

    def add(self, bullet):
        self.add_called = True
        self.add_called_with = bullet
        self.sprites.append(bullet)  # mimic the behavior of adding to the sprite group

    def draw(self):
        self.draw_called = True

class ObstacleMock:
    def draw(self):
        self.draw_called = True

class CloudsMock:
    def __init__(self):
        self.clouds = []

    def add(self, cloud):
        self.clouds.append(cloud)

    def __iter__(self):
        return iter(self.clouds)

    def draw_called(self):
        return any(cloud.draw_called() for cloud in self.clouds)

class CloudMock:
    def draw(self):
        self.draw_called = True

class ScoreboardMock:
    def __init__(self):
        self.prep_score_called = True
        self.prep_ships_called_with = None

    def prep_ships(self, image_path):
        self.prep_ships_called_with = image_path

    def draw(self):
        self.draw_called = True

class GameStatsMock:
    def __init__(self):
        self.game_active = True
        self.score = True
        self.ships_left = 3

class ButtonMock:
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 200, 50)

    def draw(self):
        self.draw_called = True

class ScoreMock:
    def draw(self):
        self.draw_called = True



# Tests for game functions
def test_key_mouse_events():
    # create mock objects for testing
    settings = SettingsMock()
    screen = ScreenMock()
    ship = ShipMock()
    bullets = BulletsMock()
    obstacles = ObstacleMock()
    stats = GameStatsMock()
    play_button = ButtonMock()
    sb = ScoreboardMock()

    # call function to be tested and add assertions
    ## Test MOUSEBUTTONDOWN event
    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN))

    ## Test KEYDOWN event
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN))
    key_mouse_events(settings, screen, ship, bullets, obstacles, stats, play_button, sb)
    assert ship.move_down is True

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP))
    key_mouse_events(settings, screen, ship, bullets, obstacles, stats, play_button, sb)
    assert ship.move_up is True

    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    key_mouse_events(settings, screen, ship, bullets, obstacles, stats, play_button, sb)
    assert bullets.add_called

    ## Test KEYUP event
    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_DOWN))
    key_mouse_events(settings, screen, ship, bullets, obstacles, stats, play_button, sb)
    assert ship.move_down is False

    pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_UP))
    key_mouse_events(settings, screen, ship, bullets, obstacles, stats, play_button, sb)
    assert ship.move_up is False


def test_update_screen():
    # create mock objects for testing
    settings = SettingsMock()
    screen = ScreenMock()
    ship = ShipMock()
    bullets = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    clouds = CloudsMock()

    # add clouds to the mock
    cloud1 = CloudMock()
    cloud2 = CloudMock()
    clouds.add(cloud1)
    clouds.add(cloud2)

    stats = GameStatsMock()
    score = ScoreMock()
    play_button = ButtonMock()

    # set the game to be active for the initial test
    stats.game_active = True

    # call function to be tested
    update_screen(settings, screen, ship, bullets, obstacles, clouds, stats, score, play_button)

    # add assertions based on the expected behavior of update_screen when game is active
    assert screen.fill_called_with == settings.bg_color
    assert ship.draw_called
    assert clouds.draw_called
    assert obstacles.draw()
    assert bullets.draw()
    assert score.draw_called
    assert not play_button.draw_called  # because game is active

    # reset for the second test where the game is not active
    stats.game_active = False

    # call function to be tested
    update_screen(settings, screen, ship, bullets, obstacles, clouds, stats, score, play_button)

    # add assertions based on the expected behavior of update_screen when the game is not active
    assert screen.fill_called_with == settings.bg_color
    assert ship.draw_called
    assert clouds.draw_called
    assert obstacles.draw()
    assert bullets.draw()
    assert score.draw_called
    assert play_button.draw_called


def test_update_bullets():
    # create mock objects for testing
    settings = SettingsMock()
    screen = ScreenMock()
    bullets = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    stats = GameStatsMock()
    sb = ScoreboardMock()

    # call function to be tested and add assertions
    # based on the expected behavior of the update_bullets function
    update_bullets(settings, screen, bullets, obstacles, stats, sb)

    for bullet in bullets.copy():
        if bullet.rect.left <= 0:
            assert bullets.remove(bullet)


def test_add_new_obstacles():
    settings = SettingsMock()
    screen = ScreenMock()
    obstacles = pygame.sprite.Group()

    add_new_obstacles(settings, screen, obstacles)
    assert len(obstacles) == 4    # since we're adding 4 obstacles in the function


def test_update_obstacles():
    settings = SettingsMock()
    screen = ScreenMock()
    ship = ShipMock()
    obstacles = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    stats = GameStatsMock()
    sb = ScoreboardMock()

    # store the initial value of stats.ships_left
    initial_ships_left = stats.ships_left

    # test when ship is hit by an obstacle
    pygame.sprite.spritecollideany = MagicMock(return_value=True)

    update_obstacles(settings, screen, ship, obstacles, bullets, stats, sb)

    # assertions for the expected behavior after the ship is hit
    assert stats.ships_left == initial_ships_left - 1
    assert sb.prep_ships_called_with == "heart.png"

    # test when ship is not hit by an obstacle
    pygame.sprite.spritecollideany = MagicMock(return_value=False)

    update_obstacles(settings, screen, ship, obstacles, bullets, stats, sb)

    # assertion for the expected behavior when the ship is not hit
    assert stats.ships_left
