# Snake Game

A classic Snake game implemented in Python using the Tkinter library.

## Objective

The main objective of the game is to control a snake to eat food items that appear on the screen. Each food item eaten makes the snake grow longer and increases your score. The game ends if the snake collides with the game boundaries or with its own body. Try to get the highest score!

## How to Run the Game

1.  Ensure you have Python installed (version 3.x recommended). Tkinter is usually included with standard Python installations.
2.  Navigate to the directory containing the game files (`main.py`, `home_screen.py`, `game_screen.py`).
3.  Run the game using the following command in your terminal:
    ```bash
    python main.py
    ```

## Gameplay

### 1. Home Screen
Upon starting the game, you'll see the home screen:
*   **High Score**: Displays the current top high score and the player who achieved it.
*   **Enter Your Name**: Input your desired username in the text field. This name will be associated with your score if you achieve a new high score.
*   **Start Game**: Click this button to begin playing.
*   **Exit**: Click this button to close the game.

### 2. Playing the Game
*   **Controls**: Use the **Arrow Keys** (Up, Down, Left, Right) on your keyboard to change the direction of the snake.
    *   You cannot immediately reverse the snake's direction (e.g., if moving Right, you cannot immediately press Left).
*   **Eating Food**: Navigate the snake to eat the **red** food items that appear on the screen.
*   **Scoring**: Each piece of food eaten increases your score by 10 points. Your current score is displayed at the top of the game screen.
*   **Growing**: The snake grows longer with each piece of food eaten.

### 3. Game Over
The game ends if:
*   The snake's head collides with any of the four walls of the game area.
*   The snake's head collides with any part of its own body.

When the game is over:
*   A "GAME OVER" message will be displayed, along with your final score.
*   If your score makes it into the top 5 high scores, a "NEW HIGH SCORE!" message will also appear.
*   After a few seconds, you will be automatically returned to the home screen.

### 4. High Scores
*   The game stores the top 5 high scores in a file named `highscores.json`.
*   The #1 high score is displayed on the home screen.

### 5. Exiting During Gameplay
*   You can return to the home screen at any time during gameplay by clicking the "Back to Home" button at the bottom of the game screen.

Enjoy playing Snake!

If there's any issues with this project or repo don't feel shy to drop a text in my dm. 