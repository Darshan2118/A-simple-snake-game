import tkinter as tk

class HomeScreen(tk.Frame):
    """HomeScreen for the Snake game, allowing player to enter name and start game."""
    def __init__(self, master, show_game_screen_callback, get_high_score_callback):
        super().__init__(master)
        self.show_game_screen_callback = show_game_screen_callback
        self.get_high_score_callback = get_high_score_callback

        title_label = tk.Label(self, text="Welcome to Snake!", font=("Arial", 28, "bold"))
        title_label.pack(pady=(30, 20))

        # High score display section
        high_score_frame = tk.Frame(self)
        high_score_frame.pack(pady=(0,20))
        tk.Label(high_score_frame, text="High Score: ", font=("Arial", 14)).pack(side=tk.LEFT)
        self.high_score_label = tk.Label(high_score_frame, text="0 (None)", font=("Arial", 14, "bold"))
        self.high_score_label.pack(side=tk.LEFT)
        self.update_high_score_display() # Initial display of high score

        # Username input section
        tk.Label(self, text="Enter your name:", font=("Arial", 14)).pack(pady=(10,5))
        self.name_entry = tk.Entry(self, font=("Arial", 14), width=20, justify="center")
        self.name_entry.pack(pady=(0,20))
        self.name_entry.insert(0, "Player") # Default player name

        # Action buttons
        start_button = tk.Button(self, text="Start Game", font=("Arial", 18, "bold"), command=self.start_game, bg="#4CAF50", fg="white", relief=tk.FLAT, padx=10, pady=5)
        start_button.pack(pady=10)

        exit_button = tk.Button(self, text="Exit", font=("Arial", 18), command=self.master.quit, bg="#f44336", fg="white", relief=tk.FLAT, padx=10, pady=5)
        exit_button.pack(pady=10)

    def update_high_score_display(self):
        """Fetches and updates the high score label on the screen."""
        name, score = self.get_high_score_callback()
        self.high_score_label.config(text=f"{score} ({name})")

    def start_game(self):
        """Gets username and calls the callback to show the game screen."""
        username = self.name_entry.get().strip()
        if not username:
            username = "Player" # Default username if input is empty
        self.show_game_screen_callback(username)
