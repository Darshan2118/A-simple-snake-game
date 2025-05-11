import tkinter as tk
from tkinter import messagebox
import json
import os

from home_screen import HomeScreen
from game_screen import GameScreen

HIGHSCORE_FILE = "highscores.json" # File to store top scores

class GameApp(tk.Tk):
    """Main application class for the Snake game."""
    def __init__(self):
        super().__init__()
        self.title("Snake Game")
        self.geometry("600x480") # Main window size
        self.current_frame = None # Holds the currently displayed screen (Home or Game)
        self.current_username = "Player" # Stores the name entered by the player
        self.top_scores = self.load_top_scores() # List of top 5 scores
        self.show_home_screen()

    def load_top_scores(self):
        """Loads top 5 scores from HIGHSCORE_FILE."""
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, 'r') as f:
                    scores = json.load(f)
                    # Validate data structure (list of dicts with 'name' and 'score')
                    if isinstance(scores, list) and all(
                        isinstance(item, dict) and "name" in item and "score" in item for item in scores
                    ):
                        scores.sort(key=lambda x: x["score"], reverse=True) # Sort descending by score
                        return scores[:5] # Return top 5
            except (json.JSONDecodeError, IOError):
                pass # Error reading file, will return default empty list
        return [] # Default if file not found or invalid

    def get_high_score_values(self):
        """Returns the name and score of the #1 player for display."""
        if self.top_scores:
            return self.top_scores[0]["name"], self.top_scores[0]["score"]
        return "None", 0 # Default if no scores are recorded

    def save_score(self, current_score_value):
        """
        Adds the current score to the list of top scores if it qualifies,
        keeps the list sorted and capped at 5, and saves to file.
        Returns True if the score made it into the top 5, False otherwise.
        """
        min_score_in_top_5 = 0
        if len(self.top_scores) == 5:
            min_score_in_top_5 = self.top_scores[-1]["score"] # Score of the 5th player

        made_it_to_top_5 = False
        if current_score_value > min_score_in_top_5 or len(self.top_scores) < 5:
            self.top_scores.append({"name": self.current_username, "score": current_score_value})
            self.top_scores.sort(key=lambda x: x["score"], reverse=True)
            self.top_scores = self.top_scores[:5] # Keep only top 5
            made_it_to_top_5 = True
            
            try:
                with open(HIGHSCORE_FILE, 'w') as f:
                    json.dump(self.top_scores, f) # Save updated list
            except IOError:
                messagebox.showerror("Error", "Could not save high scores.")
        
        return made_it_to_top_5

    def show_home_screen(self):
        """Destroys current frame and displays the HomeScreen."""
        if self.current_frame:
            self.current_frame.destroy()
        # HomeScreen needs callbacks to show game screen and get top score
        self.current_frame = HomeScreen(self, self.show_game_screen, self.get_high_score_values)
        self.current_frame.pack(fill="both", expand=True)
        # Refresh high score display on HomeScreen if it's being re-shown
        if hasattr(self.current_frame, 'update_high_score_display'):
             self.current_frame.update_high_score_display()

    def show_game_screen(self, username):
        """Destroys current frame and displays the GameScreen."""
        self.current_username = username # Store for use when saving score
        if self.current_frame:
            self.current_frame.destroy()
        # GameScreen needs callbacks to return to home and save score
        self.current_frame = GameScreen(self, self.show_home_screen, self.save_score)
        self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
