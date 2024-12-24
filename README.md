# Dino Game

#### Video [Demo](https://youtu.be/vNVWjTpqZkY)

### Description

**Dino Game** is a simple 2D arcade-style game implemented using Python and the `pygame` library. Inspired by the classic browser-based "Dino Game" from Google Chrome, this project allows users to control a dinosaur character and avoid incoming obstacles to achieve the highest score. The game features basic mechanics such as player movement, collision detection, scoring, and high score saving.

### Project Overview

In this game, the player controls a red dinosaur that can jump to avoid enemies coming from the right side of the screen. The goal is to survive for as long as possible while avoiding these obstacles, which increase in difficulty over time. The game tracks the player’s score, which is based on how long the player survives, and saves the highest score to a CSV file. Players can input their name after they are hit by an obstacle, and their score will be recorded in a file with a timestamp.

### Files in this Project

1. **`project.py`**
   This is the main file containing the game logic. It initializes the game environment using `pygame`, manages game states (starting, running, paused, exit), and handles player input. The file includes the game loop that runs continuously until the player exits. This file also contains the `Player` and `Enemy` classes, which define the game's character and obstacle behaviors, respectively.

   - The `Player` class handles the dinosaur's movement, jumping mechanics.
   - The `Enemy` class defines the behavior of obstacles, including their spawn and movement towards the player.

2. **`constants.py`**
   This file contains all the necessary constants that define the game’s settings. It includes constants for screen width and height, the player's movement speed, the gravity effect, enemy spawn rates, and other configuration settings like the file path for storing scores. By separating these settings into a constants file, the game becomes easier to modify and maintain.

3. **`score.csv`** (Generated during gameplay)
   This CSV file stores the scores. Each entry contains the timestamp when the score was achieved, the player's name, and their final score. This file is updated every time a new score is recorded.

### Features and Game Mechanics

- **Jumping Mechanism**: The player controls the dinosaur's vertical movement using the `Space`, `Up Arrow`, or `W` keys. The dinosaur can only jump when it is on the ground, and gravity pulls it back down to the ground after each jump.
- **Obstacles**: Randomly generated rectangular obstacles appear on the screen and move from right to left. The player must avoid these obstacles to stay alive. If the dinosaur collides with an obstacle, the game ends.
- **Score Tracking**: The game keeps track of the player's score, which increases over time based on how long they survive. When the game ends, the player is prompted to input their name and score, which is then saved in the `score.csv` file.
- **High Score**: The highest score achieved is displayed during the game. The game also keeps track of the top score across sessions by reading from the CSV file.
- **Pause and Resume**: The game can be paused at any time by pressing the `Escape` key. The game can be resumed by pressing `Escape` again.

### Design Choices

- **Collision Detection**: The game uses a rectangular bounding box for both the player and enemies to check for collisions. This approach simplifies the detection process and avoids the complexity of pixel-perfect collision detection, making the game run efficiently.

- **Game Loop and State Management**: The game operates in a state-driven manner, where it toggles between different states such as `STARTING`, `RUNNING`, `PAUSE`, and `EXIT`. This makes it easier to manage different aspects of the game, such as displaying the starting screen, handling the game mechanics, and dealing with pauses.

- **Input Handling**: The game processes keyboard input via `pygame.key.get_pressed()` to allow the player to jump and pause the game. The player’s name is taken after the game ends via a simple input loop where the user types their name and hits `Enter`.

- **File Handling**: Scores are saved in a CSV file, with each entry containing the date and time, player name, and score. This allows for easy retrieval of past high scores and promotes data persistence across game sessions.

### Running the Game

To install all the required packages, run

```bash
pip install requirements.txt
```

Once you have `pygame` installed, you can run the game by executing:

```bash
python project.py
```

### Future Improvements

- **Improved Graphics**: The game currently uses basic rectangles for the player and enemies. Future improvements could include using images or sprites to make the game visually more appealing.
- **Sound Effects and Music**: Adding sound effects for jumping, collisions, and background music could enhance the gaming experience.
- **Difficulty Levels**: As the game progresses, the speed of enemies could increase to make the game more challenging.

### Conclusion

This Dino Game provides a simple but engaging experience, and its design allows for easy modifications and future enhancements. The project demonstrates how to use `pygame` to build a game with basic physics, collision detection, and file management.
