import tkinter as tk
import random

# Game constants
GAME_WIDTH = 580
GAME_HEIGHT = 380
SNAKE_ITEM_SIZE = 20
GAME_SPEED = 200 # milliseconds

class GameScreen(tk.Frame):
    def __init__(self, master, show_home_screen_callback, save_high_score_callback): # Added save_high_score_callback
        super().__init__(master, bg="black")
        self.master = master
        self.show_home_screen_callback = show_home_screen_callback
        self.save_high_score_callback = save_high_score_callback # Store the callback
        self.score = 0
        self.direction = "Right" # Initial direction
        self.snake_positions = [(100, 100), (80, 100), (60, 100)] # Initial snake
        self.food_position = self.create_food()
        self.game_over_flag = False

        # Score display at the top
        self.score_label = tk.Label(self, text=f"Score: {self.score}", fg="white", bg="black", font=("Arial", 16, "bold"))
        self.score_label.pack(pady=(10,0)) # Add some padding at the top

        self.canvas = tk.Canvas(self, bg="black", width=GAME_WIDTH, height=GAME_HEIGHT, highlightthickness=0)
        self.canvas.pack(pady=(5,0)) # Reduce padding between score and canvas

        # Back button at the bottom
        back_button = tk.Button(self, text="Back to Home", font=("Arial", 12), command=self.go_to_home, relief=tk.FLAT, bg="#333", fg="white")
        back_button.pack(pady=10, side=tk.BOTTOM)

        self.bind_keys() # Call to bind keys
        self.draw_elements()
        self.game_loop()

    def create_food(self):
        while True:
            x = random.randrange(0, GAME_WIDTH // SNAKE_ITEM_SIZE) * SNAKE_ITEM_SIZE
            y = random.randrange(0, GAME_HEIGHT // SNAKE_ITEM_SIZE) * SNAKE_ITEM_SIZE
            if (x, y) not in self.snake_positions:
                return (x, y)

    def draw_elements(self):
        self.canvas.delete(tk.ALL)
        # Draw snake
        for x, y in self.snake_positions:
            self.canvas.create_rectangle(x, y, x + SNAKE_ITEM_SIZE, y + SNAKE_ITEM_SIZE, fill="green", outline="darkgreen")
        # Draw food
        self.canvas.create_oval(self.food_position[0], self.food_position[1],
                                self.food_position[0] + SNAKE_ITEM_SIZE, self.food_position[1] + SNAKE_ITEM_SIZE,
                                fill="red", outline="darkred")

    def move_snake(self):
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
        else: # Should not happen
            return

        self.snake_positions.insert(0, new_head_position)

        # Check for collision with food
        if new_head_position == self.food_position:
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            self.food_position = self.create_food()
        else:
            self.snake_positions.pop() # Remove tail

        # Check for collision with self or walls
        if (self.check_collision_with_self() or
                self.check_collision_with_walls(new_head_position)):
            self.game_over()

    def check_collision_with_self(self):
        return self.snake_positions[0] in self.snake_positions[1:]

    def check_collision_with_walls(self, head_pos):
        x, y = head_pos
        return not (0 <= x < GAME_WIDTH and 0 <= y < GAME_HEIGHT)

    def game_over(self):
        self.game_over_flag = True
        self.canvas.delete(tk.ALL)

        # Call to save high score
        is_new_high_score = self.save_high_score_callback(self.score)

        game_over_text = "GAME OVER"
        if is_new_high_score:
            game_over_text += "\nNEW HIGH SCORE!"

        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 - 40, # Adjusted y for potential two lines
                                text=game_over_text,
                                fill="red", font=("Arial", 36, "bold"), justify="center", anchor="center", tags="game_over_text")
        self.canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2 + 30, # Adjusted y
                                text=f"Final Score: {self.score}",
                                fill="white", font=("Arial", 20), justify="center", anchor="center", tags="game_over_text")

        if hasattr(self.master, '_keys_bound') and self.master._keys_bound:
            self.master.unbind("<KeyPress-Left>")
            self.master.unbind("<KeyPress-Right>")
            self.master.unbind("<KeyPress-Up>")
            self.master.unbind("<KeyPress-Down>")
            self.master._keys_bound = False

        self.master.after(3000, self.go_to_home) # Redirect after 3 seconds

    def change_direction(self, new_direction):
        if self.game_over_flag:
            return
        # Prevent immediate reversal
        if new_direction == "Left" and self.direction != "Right":
            self.direction = new_direction
        elif new_direction == "Right" and self.direction != "Left":
            self.direction = new_direction
        elif new_direction == "Up" and self.direction != "Down":
            self.direction = new_direction
        elif new_direction == "Down" and self.direction != "Up":
            self.direction = new_direction

    def game_loop(self):
        if not self.game_over_flag:
            self.move_snake()
            if not self.game_over_flag: # Check again in case move_snake caused game over
                self.draw_elements()
            self.master.after(GAME_SPEED, self.game_loop)
        # If game_over_flag is true, the loop will naturally stop calling itself.
        # The game_over method handles displaying the message.

    def go_to_home(self):
        # Ensure game loop is stopped if active
        self.game_over_flag = True # This will stop the after call
        # Unbind game-specific keys before going home
        if hasattr(self.master, '_keys_bound') and self.master._keys_bound: # Check if keys were bound
            self.master.unbind("<KeyPress-Left>")
            self.master.unbind("<KeyPress-Right>")
            self.master.unbind("<KeyPress-Up>")
            self.master.unbind("<KeyPress-Down>")
            self.master._keys_bound = False
        self.show_home_screen_callback()

    def bind_keys(self):
        # Ensure keys are bound to the master window (GameApp instance)
        # and only if not already bound by another GameScreen instance (though unlikely with current structure)
        if not hasattr(self.master, '_keys_bound') or not self.master._keys_bound:
            self.master.bind("<KeyPress-Left>", lambda event: self.change_direction("Left"))
            self.master.bind("<KeyPress-Right>", lambda event: self.change_direction("Right"))
            self.master.bind("<KeyPress-Up>", lambda event: self.change_direction("Up"))
            self.master.bind("<KeyPress-Down>", lambda event: self.change_direction("Down"))
            self.master._keys_bound = True # Flag to track if keys are bound

if __name__ == '__main__':
    # This part is for testing game_screen.py independently
    root = tk.Tk()
    root.title("Test Game Screen")
    # Adjusted geometry to better fit score, canvas, and button
    # Canvas is 580x380. Score label and button add vertical space.
    # Approx height: 30 (score) + 10 (padding) + 380 (canvas) + 10 (padding) + 30 (button) + 10 (padding) = 470
    root.geometry(f"{GAME_WIDTH + 20}x{GAME_HEIGHT + 90}") # +20 for window borders
    
    def _show_home_test():
        print("Going back to home screen (test)")
        root.quit()
    
    def _save_hs_test(score):
        print(f"Test: Game over with score {score}. Is new high score? (Simulating True)")
        return True # Simulate new high score for testing text display

    game_frame = GameScreen(root, _show_home_test, _save_hs_test) # Pass dummy save callback
    game_frame.pack(fill="both", expand=True)
    root.mainloop()
