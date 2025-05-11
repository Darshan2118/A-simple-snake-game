import tkinter as tk
from tkinter import messagebox
import json
import os

from home_screen import HomeScreen
from game_screen import GameScreen

HIGHSCORE_FILE = "highscores.json"

class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Snake Game")
        self.geometry("600x480") # Adjusted height
        self.current_frame = None
        self.current_username = "Player"
        self.top_scores = self.load_top_scores() # Now a list
        self.show_home_screen()

    def load_top_scores(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, 'r') as f:
                    scores = json.load(f)
                    # Validate that it's a list of dicts with 'name' and 'score'
                    if isinstance(scores, list) and all(
                        isinstance(item, dict) and "name" in item and "score" in item for item in scores
                    ):
                        # Ensure it's sorted and capped at 5, just in case file was manually edited
                        scores.sort(key=lambda x: x["score"], reverse=True)
                        return scores[:5]
            except (json.JSONDecodeError, IOError):
                pass # File corrupted or unreadable, will create a new one
        return [] # Default if file doesn't exist or is invalid (empty list)

    def get_high_score_values(self):
        # Returns name and score of the #1 high score for HomeScreen display
        if self.top_scores:
            return self.top_scores[0]["name"], self.top_scores[0]["score"]
        return "None", 0 # Default if no scores yet

    def save_score(self, current_score_value):
        # Called from GameScreen when a game ends
        # Determine if this score qualifies for the top 5
        
        # Get the score of the 5th player, or 0 if less than 5 scores
        min_score_in_top_5 = 0
        if len(self.top_scores) == 5:
            min_score_in_top_5 = self.top_scores[-1]["score"]
        
        made_it_to_top_5 = False
        if current_score_value > min_score_in_top_5 or len(self.top_scores) < 5:
            # Add new score
            self.top_scores.append({"name": self.current_username, "score": current_score_value})
            # Sort by score descending
            self.top_scores.sort(key=lambda x: x["score"], reverse=True)
            # Keep only top 5
            self.top_scores = self.top_scores[:5]
            made_it_to_top_5 = True
            
            try:
                with open(HIGHSCORE_FILE, 'w') as f:
                    json.dump(self.top_scores, f)
            except IOError:
                messagebox.showerror("Error", "Could not save high scores.")
        
        return made_it_to_top_5 # Return true if the score made it into the top 5

    def show_home_screen(self):
        if self.current_frame:
            self.current_frame.destroy()
        # Pass the get_high_score_values callback to HomeScreen
        self.current_frame = HomeScreen(self, self.show_game_screen, self.get_high_score_values)
        self.current_frame.pack(fill="both", expand=True)
        # If home screen is being re-shown (e.g. after a game), ensure its high score display is up-to-date
        if hasattr(self.current_frame, 'update_high_score_display'):
             self.current_frame.update_high_score_display()


    def show_game_screen(self, username): # Now accepts username
        self.current_username = username # Store username for when game ends
        if self.current_frame:
            self.current_frame.destroy()
        # Pass show_home_screen (for back button) and save_score (for game over)
        self.current_frame = GameScreen(self, self.show_home_screen, self.save_score)
        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
