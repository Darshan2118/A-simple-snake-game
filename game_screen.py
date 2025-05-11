import tkinter as tk
import random

# --- Game Constants ---
GAME_WIDTH = 580        # Width of the game canvas
GAME_HEIGHT = 380       # Height of the game canvas
SNAKE_ITEM_SIZE = 20    # Size of each snake segment and food item
GAME_SPEED = 200        # Game loop refresh rate in milliseconds

class GameScreen(tk.Frame):
    """Manages the actual snake gameplay, drawing, and logic."""
    def __init__(self, master, show_home_screen_callback, save_high_score_callback):
        super().__init__(master, bg="black")
        self.master = master
        self.show_home_screen_callback = show_home_screen_callback
        self.save_high_score_callback = save_high_score_callback # Callback to save score

        self.score = 0
        self.direction = "Right"  # Initial snake direction
        self.snake_positions = [(100, 100), (80, 100), (60, 100)]  # Initial snake segments
        self.food_position = self.create_food()
        self.game_over_flag = False

        # UI Elements
        self.score_label = tk.Label(self, text=f"Score: {self.score}", fg="white", bg="black", font=("Arial", 16, "bold"))
        self.score_label.pack(pady=(10,0)) # Padding: top=10, bottom=0

        self.canvas = tk.Canvas(self, bg="black", width=GAME_WIDTH, height=GAME_HEIGHT, highlightthickness=0)
        self.canvas.pack(pady=(5,0)) # Padding: top=5, bottom=0

        back_button = tk.Button(self, text="Back to Home", font=("Arial", 12), command=self.go_to_home, relief=tk.FLAT, bg="#333", fg="white")
        back_button.pack(pady=10, side=tk.BOTTOM)

        self.bind_keys()
        self.draw_elements()
        self.game_loop()

    def create_food(self):
        """Generates a new food item at a random position not occupied by the snake."""
        while True:
            x = random.randrange(0, GAME_WIDTH // SNAKE_ITEM_SIZE) * SNAKE_ITEM_SIZE
            y = random.randrange(0, GAME_HEIGHT // SNAKE_ITEM_SIZE) * SNAKE_ITEM_SIZE
            if (x, y) not in self.snake_positions:
                return (x, y)

    def draw_elements(self):
        """Clears the canvas and redraws the snake and food."""
        self.canvas.delete(tk.ALL)
        # Draw snake segments
        for x, y in self.snake_positions:
            self.canvas.create_rectangle(x, y, x + SNAKE_ITEM_SIZE, y + SNAKE_ITEM_SIZE, fill="green", outline="darkgreen")
        # Draw food item
        self.canvas.create_oval(self.food_position[0], self.food_position[1],
                                self.food_position[0] + SNAKE_ITEM_SIZE, self.food_position[1] + SNAKE_ITEM_SIZE,
                                fill="red", outline="darkred")

    def move_snake(self):
        """Moves the snake according to the current direction and checks for collisions."""
        if self.game_over_flag:
            return

        head_x, head_y = self.snake_positions[0]
        if self.direction == "Left":
            new_head_position = (head_x - SNAKE_ITEM_SIZE, head_y)
        elif self.direction == "Right":
            new_head_position = (head_x + SNAKE_ITEM_SIZE, head_y)
        elif self.direction == "Up":
            new_head_position = (head_x, head_y - SNAKE_ITEM_SIZE)
        elif self.direction == "Down":
            new_head_position = (head_x, head_y + SNAKE_ITEM_SIZE)
        else: # Should not occur
            return

        self.snake_positions.insert(0, new_head_position) # Add new head

        # Check for food consumption
        if new_head_position == self.food_position:
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            self.food_position = self.create_food()
        else:
            self.snake_positions.pop() # Remove tail if no food eaten

        # Check for game over conditions
        if self.check_collision_with_self() or self.check_collision_with_walls(new_head_position):
            self.game_over()

    def check_collision_with_self(self):
        """Checks if the snake's head has collided with its body."""
        return self.snake_positions[0] in self.snake_positions[1:]

    def check_collision_with_walls(self, head_pos):
        """Checks if the snake's head has collided with the game boundaries."""
        x, y = head_pos
        return not (0 <= x < GAME_WIDTH and 0 <= y < GAME_HEIGHT)

    def game_over(self):
        """Handles the game over sequence: displays message, saves score, and schedules return to home."""
        self.game_over_flag = True
        self.canvas.delete(tk.ALL) # Clear canvas for game over message

        is_new_high_score = self.save_high_score_callback(self.score) # Attempt to save score

        game_over_msg_text = "GAME OVER"
        if is_new_high_score:
            game_over_msg_text += "\nNEW HIGH SCORE!"

        # Display game over messages
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 40,
                                text=game_over_msg_text,
                                fill="red", font=("Arial", 36, "bold"), justify="center", anchor="center")
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 30,
                                text=f"Final Score: {self.score}",
                                fill="white", font=("Arial", 20), justify="center", anchor="center")

        # Unbind arrow keys
        if hasattr(self.master, '_keys_bound') and self.master._keys_bound:
            self.master.unbind("<KeyPress-Left>")
            self.master.unbind("<KeyPress-Right>")
            self.master.unbind("<KeyPress-Up>")
            self.master.unbind("<KeyPress-Down>")
            self.master._keys_bound = False # Reset flag

        self.master.after(3000, self.go_to_home) # Redirect to home screen after 3 seconds

    def change_direction(self, new_direction):
        """Changes the snake's direction if the new direction is valid."""
        if self.game_over_flag:
            return
        # Prevent immediate reversal of direction
        if new_direction == "Left" and self.direction != "Right":
            self.direction = new_direction
        elif new_direction == "Right" and self.direction != "Left":
            self.direction = new_direction
        elif new_direction == "Up" and self.direction != "Down":
            self.direction = new_direction
        elif new_direction == "Down" and self.direction != "Up":
            self.direction = new_direction

    def game_loop(self):
        """Main game loop, responsible for moving, drawing, and scheduling next update."""
        if not self.game_over_flag:
            self.move_snake()
            if not self.game_over_flag: # Re-check, as move_snake might trigger game_over
                self.draw_elements()
            self.master.after(GAME_SPEED, self.game_loop) # Schedule next iteration

    def go_to_home(self):
        """Cleans up and calls the callback to show the home screen."""
        self.game_over_flag = True # Ensure game loop stops
        # Unbind keys if they were bound by this screen
        if hasattr(self.master, '_keys_bound') and self.master._keys_bound:
            self.master.unbind("<KeyPress-Left>")
            self.master.unbind("<KeyPress-Right>")
            self.master.unbind("<KeyPress-Up>")
            self.master.unbind("<KeyPress-Down>")
            self.master._keys_bound = False
        self.show_home_screen_callback()

    def bind_keys(self):
        """Binds arrow key presses to change_direction method."""
        # Bind to master window to ensure events are captured globally for this screen
        if not hasattr(self.master, '_keys_bound') or not self.master._keys_bound:
            self.master.bind("<KeyPress-Left>", lambda event: self.change_direction("Left"))
            self.master.bind("<KeyPress-Right>", lambda event: self.change_direction("Right"))
            self.master.bind("<KeyPress-Up>", lambda event: self.change_direction("Up"))
            self.master.bind("<KeyPress-Down>", lambda event: self.change_direction("Down"))
            self.master._keys_bound = True # Flag to indicate keys are currently bound

if __name__ == '__main__':
    # This section is for testing game_screen.py independently
    root = tk.Tk()
    root.title("Test Game Screen")
    # Adjusted geometry for testing to fit all elements
    # Canvas: 580x380. Score label and button add vertical space.
    # Approx height needed: 30 (score) + 10 (pad) + 380 (canvas) + 10 (pad) + 30 (button) + 10 (pad) = ~470px
    root.geometry(f"{GAME_WIDTH + 20}x{GAME_HEIGHT + 90}") # +20 width for window borders
    
    def _show_home_test():
        print("Test: Going back to home screen")
        root.quit()
    
    def _save_hs_test(score):
        print(f"Test: Game over with score {score}. Simulating new high score.")
        return True # Simulate new high score for testing display

    game_frame = GameScreen(root, _show_home_test, _save_hs_test) # Pass dummy callbacks
    game_frame.pack(fill="both", expand=True)
    root.mainloop()
