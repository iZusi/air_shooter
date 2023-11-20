# Air Shooter: My CS50P Final Project

Air Shooter is a simple 2D shooting game built in Python using the Pygame library. The game features a player-controlled spaceship, obstacles to avoid, bullets to shoot, and a scoring system.

## Table of Contents
- [Features](#features)
- [Run Locally](#run-locally)
- [Usage](#usage)
- [Game Controls](#game-controls)
- [Video Demo](#video-demo)
- [Code Explanation](#code-explanation)
- [Testing](#testing)
- [Acknowledgments](#acknowledgments)

## Features

- Player-controlled spaceship with up and down movement.
- Shooting bullets to destroy obstacles and earn points.
- Obstacles to avoid, including various images such as birds, emeralds, and boxes.
- Scoring system with points awarded for each obstacle destroyed.
- Lives system with the ability to reset the game.
- Play button to start or restart the game.

## Run Locally

To run the Air Shooter game, you need to have Python and Pygame installed. Follow these steps:

- Clone the repository:
   ```bash
   git clone https://github.com/iZusi/air-shooter.git
   cd air-shooter

- Install required dependencies
```bash
pip install pygame
```

## Usage

Run the game by executing the following command in the project directory:
```bash
python air_shooter.py
```

## Game Controls

- `Up Arrow Key:`  Move the spaceship up.
- `Down Arrow Key:`  Move the spaceship down.
- `Space key:`  Fire bullets to destroy obstacles.

## Video Demo

[![Watch the video demo](https://img.youtube.com/vi/ZmBNUDnxiQs/0.jpg)](https://youtube.com/watch?v=ZmBNUDnxiQs)

## Code Explanation
To make things a bit easy for me, I broke the code into two main sections: 'Game Classes' and 'Game Functions.'

#### Game Classes

- **Settings:**  The `Settings` class serves as the central hub for managing various parameters and configurations in the game. Designed to handle the game settings, it encapsulates attributes related to the screen dimensions, background color, ship characteristics (speed and lives), bullet properties (speed, dimensions, and color), obstacle speed, overall game speed, and scoring system. This class provides a convenient and organized way to store and access these settings, making it easier for developers to tweak and modify the game's behavior without directly manipulating individual variables scattered throughout the code. By placing these parameters within a class, the code becomes more modular, readable, and maintainable. An instance of this class can be created to access or modify specific game settings based on their design preferences or user input.
- **Ship:**  The `Ship` class is designed to manage the player's ship or aircraft in the game, incorporating functionality to handle its positioning, movement, and appearance. It inherits from the `Sprite` class. The `Ship` class is initialized with parameters such as game settings and the game screen. The class includes methods to update the ship's position based on user input, reset its position, and draw it on the screen. The ship's image is loaded from a file, and its initial position is set at the center of the screen vertically and slightly to the left horizontally. The class tracks the ship's movement direction (up or down) and adjusts its position accordingly. This class allows for easy integration of the ship into the game environment, promoting modularity and maintainability in the overall game code.
- **Bullet:**  This class is responsible for managing the creation, movement, and appearance of bullets associated with the player's ship in the game. It inherits from the `Sprite` class, just like the `Ship` class. The class is initialized with parameters such as game settings, the game screen, and the ship object to which the bullets are linked. The bullet is represented as a rectangular object, and its initial position is set at the same vertical position as the spaceship and aligned with its center horizontally. The class includes methods to update the bullet's position as it moves across the screen and to draw the bullet with a specified color on the game screen.
- **Obstacles:**  The `Obstacles` class manages the addition and behavior of obstacles in the game. It inherits from the `Sprite` class, much like the `Ship` and `Bullet` classes. The obstacle's initial position is set off-screen with a random horizontal and vertical placement. The class includes methods to update the obstacle's position as it moves across the screen and to draw the obstacle on the game screen. If an obstacle moves beyond the left edge of the screen, it is repositioned with a random horizontal placement, creating a continuous cycle of obstacles.
- **Clouds:**  With this class I am able to introduce and manage clouds within the game environment. Clouds are positioned off-screen with random horizontal and vertical placement. The class includes methods to update the cloud's position as it moves across the screen and to draw the cloud on the game screen. If a cloud goes beyond the left edge of the screen, much like the `Obstacles` class, it is repositioned with a new random horizontal placement, creating a continuous cycle of drifting clouds.
- **GameStats:**  The `GameStats` class is responsible for tracking and managing the game statistics. Upon initialization, it takes game settings as a parameter and initializes key attributes such as the number of remaining lives and the player's score. The class includes a method, `reset_stats()`, which initializes statistics that can change during the game, such as the remaining lives and score. The game starts in an inactive state, as indicated by the `game_active` attribute being set to `False`. This class serves as a centralized hub for monitoring and updating the crucial game statistics, contributing to a well-organized and easily maintainable code structure. It provides a convenient mechanism for resetting statistics when needed, promoting efficient management of the game state information.
- **Button:**  This class manages the play button in the game interface. The class defines dimensions, colors, and font properties for the button, and it constructs the button's rectangular object, centering it on the screen. The `prep_msg()` method renders the button message into an image, ensuring it is centered on the button. The `draw()` method is responsible for drawing the button with a filled background and the rendered message on the game screen.
- **Scoreboard:**  The `Scoreboard` class is responsible for reporting scoring information and displaying the remaining ships in the game. The class defines font settings and prepares the initial score image, positioning it at the top right of the screen. The `prep_ships()` method creates a group of ship instances based on the number of remaining lives, displaying them on the screen. The `draw()` method is then responsible for rendering and displaying both the score and the remaining ships on the game screen.

#### Game Functions

- **run_game:**  The `run_game()` function orchestrates various aspects of the game, handling game events and updating the game state. It initializes key game elements such as settings, the game window, the player's ship, game statistics, scoreboard, bullets, obstacles, clouds, and a play button. The function enters a while loop that continuously checks for events, updating the screen and game elements accordingly. The game is limited to 60 frames per second, and events are processed through helper functions like `key_mouse_events()`, `update_screen()`, `update_bullets()`, `update_obstacles()`, and individual updates for the ship and clouds. This function handles the core logic for running the game and maintaining its state.
- **key_mouse_events:**  The `key_mouse_events()` function manages keypresses and mouse clicks in the game. It iterates through the events, handling actions such as quitting the game when the window is closed. Mouse clicks are processed to check for interactions with the play button. Ship control is managed through keydown and keyup events, allowing the player to move the ship up and down and fire bullets using the space key.
- **update_screen:**  This function manages the visual elements on the game screen, handling the display of the background, player's ship, bullets, obstacles, clouds, and the game score. It first fills the screen with the specified background color, then draws the ship, clouds, obstacles, bullets, and the score on the screen. If the game is not active, it also draws the play button. Finally, it updates the display to reflect the changes.
- **update_bullets:**  The `update_bullets()` function manages the behavior of bullets in the game. It first updates the position of each bullet and removes any bullets that have reached the left edge of the screen. The function then checks for collisions between bullets and obstacles, removing both the bullet and obstacle upon collision. If a collision occurs, the player's score is updated, and the scoreboard is refreshed. If there are no remaining obstacles, existing bullets are cleared, and new obstacles are added to the game.
- **update_obstacles:**  The `update_obstacles()` function is responsible for updating the position of obstacles and checking for collisions between the player's ship and obstacles. First, it updates the positions of all obstacles on the screen. If a collision is detected between the player's ship and any obstacle, it responds by decrementing the remaining lives, updating the scoreboard, clearing the lists of bullets and obstacles, adding new obstacles, resetting the ship's position, and introducing a brief pause for effect. If the player runs out of lives, the game state is set to inactive, and the mouse cursor is made visible.
- **add_new_obstacles:**  The `add_new_obstacles()` function does the simple job of adding new obstacles to the game screen every time an obstacle is shot. It appends instances of the `Obstacles` class with specific filenames to the existing group of obstacles, ensuring a continuous stream of challenges for the player.
- **check_play_button:**  The `check_play_button()` function handles mouse clicks to initiate the game. It checks if the play button has been clicked, and if the game is not already active. If these conditions are met, it hides the mouse cursor, resets game statistics, sets the game state to active, clears the lists of bullets and obstacles, adds new obstacles, resets the ship's position, and updates the scoreboard images.

## Testing

I have included a set of unit tests to ensure the functionality of some components in the project. You can run these tests to validate the behavior of various functions. To run the tests, execute the following commands in your project directory:

- Install pytest if you don't already have it
```bash
pip install pygame
```

- Now execute this command to run the test
```bash
pytest test_air_shooter.py
```

- **test_key_mouse_events:**  This test checks the functionality of the `key_mouse_events` function, which handles keypress and mouse click events in the game. It simulates various events and asserts the expected behavior.
- **test_update_screen:**  This test, although I can't seem to get the code to work yet, verifies the behavior of the `update_screen` function, which manages activities on the game screen. It checks the rendering of game elements under both active and inactive game states.
- **test_update_bullets:**  The `update_bullets` function is tested to ensure proper handling of bullet updates, removals, and collisions with obstacles.
- **test_add_new_obstacles:**  This test confirms that the `add_new_obstacles` function correctly adds a specified number of obstacles to the game.
- **test_update_obstacles:**  The `update_obstacles` function is tested for its response to ship-obstacle collisions, including updating game statistics, resetting the ship's position, and continuing or ending the game.

## Acknowledgments

This project was developed with inspiration and guidance from the book "Python Crash Course" by Eric Matthes. The structure and concepts of the game, as well as some code snippets, were adapted from the "Alien Invasion" project in the book.

- **Book:** [Python Crash Course by Eric Matthes](https://nostarch.com/pythoncrashcourse)

A special thanks to Eric Matthes for providing valuable insights and resources in learning Python game development.

Additionally, I would like to acknowledge maxontech for their chrome-dinosaur project, which served as a reference for introducing moving clouds, simulating the ship movement, and the random popping of obstacles from the opposite side of the screen.

- **Project:** [maxontech/chrome-dinosaur](https://github.com/maxontech/chrome-dinosaur)

Deep gratitude to Harvard professor David Malan for his exceptional teaching and enlightening lectures. His dedication and expertise have been instrumental in fostering my understanding and confidence in Python programming.

I also extend my sincere appreciation to the CS50 staff for their tremendous work in creating an outstanding learning environment. Their support and resources have played a pivotal role in shaping my programming journey.
