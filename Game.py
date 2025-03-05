import tkinter as tk
from tkinter import ttk, messagebox
import random
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class WordLadderGame:
    def __init__(self, dictionary_file='dictionary.txt', words_file='words.txt'):
        self.load_dictionary(dictionary_file)
        self.current_path = []
        self.optimal_path = []
        self.current_algorithm = "A*"
        self.game_mode = "Beginner"
        self.score = 0
        self.tries = []  # List to store user's attempts
        self.max_tries = {
            "Beginner": 5,
            "Advanced": 8,
            "Challenge": 10
        }
        self.word_lengths = {
            "Beginner": 3,  # 3-letter words for beginner
            "Advanced": 5,  # 5-letter words for advanced
            "Challenge": 5  # 5-letter words with constraints for challenge
        }
        self.banned_words = set()
        self.restricted_letters = set()
    
    
    def load_dictionary(self, dictionary_file):
        """Load dictionary from file, keeping only words of the same length."""
        try:
            with open(dictionary_file, 'r') as f:
                self.dictionary = set(word.strip().lower() for word in f.readlines())
            print(f"Loaded {len(self.dictionary)} words from dictionary")
        except FileNotFoundError:
            # Fallback to a minimal dictionary for testing
            self.dictionary = {'cat', 'hat', 'bat', 'bet', 'let', 'set', 'sit', 'hit', 'hot', 'dot', 'dog'}
            print("Using default dictionary as file was not found")
    
    def load_words(self, words_file):
        """Load start and end words from a file."""
        try:
            with open(words_file, 'r') as f:
                words = [word.strip().lower() for word in f.readlines()]
                if len(words) >= 2:
                    return words[0], words[1]
                else:
                    raise ValueError("The words file must contain at least two words.")
        except FileNotFoundError:
            print("Words file not found. Using default words.")
            return "cat", "dog"  # Fallback to default words
    
    def is_one_letter_different(self, word1, word2):
        """Check if two words differ by exactly one letter."""
        if len(word1) != len(word2):
            return False
        differences = sum(1 for a, b in zip(word1, word2) if a != b)
        return differences == 1
    
    def find_neighbors(self, word):
        """Find all words in the dictionary that differ by one letter."""
        neighbors = []
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                if c != word[i]:
                    new_word = word[:i] + c + word[i+1:]
                    if new_word in self.dictionary and len(new_word) == len(word):
                        neighbors.append(new_word)
        return neighbors
    
    def hamming_distance(self, word1, word2):
        """Calculate the Hamming distance between two words."""
        return sum(1 for a, b in zip(word1, word2) if a != b)
    
    def bfs(self, start_word, end_word):
        """Breadth-First Search to find the shortest path."""
        if start_word not in self.dictionary or end_word not in self.dictionary:
            return None
        
        queue = [(start_word, [start_word])]
        visited = {start_word}
        
        while queue:
            current_word, path = queue.pop(0)
            
            if current_word == end_word:
                return path
            
            for neighbor in self.find_neighbors(current_word):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def ucs(self, start_word, end_word):
        """Uniform Cost Search to find the shortest path."""
        if start_word not in self.dictionary or end_word not in self.dictionary:
            return None
        
        priority_queue = [(0, start_word, [start_word])]  # (cost, word, path)
        visited = set()
        
        while priority_queue:
            cost, current_word, path = heapq.heappop(priority_queue)
            
            if current_word in visited:
                continue
                
            visited.add(current_word)
            
            if current_word == end_word:
                return path
            
            for neighbor in self.find_neighbors(current_word):
                if neighbor not in visited:
                    new_cost = cost + 1  # Each step has uniform cost of 1
                    heapq.heappush(priority_queue, (new_cost, neighbor, path + [neighbor]))
        
        return None
    
    def a_star(self, start_word, end_word):
        """A* Search to find the shortest path."""
        if start_word not in self.dictionary or end_word not in self.dictionary:
            return None
        
        # Priority queue: (f(n), g(n), word, path)
        priority_queue = [(self.hamming_distance(start_word, end_word), 0, start_word, [start_word])]
        visited = set()
        
        while priority_queue:
            _, g_cost, current_word, path = heapq.heappop(priority_queue)
            
            if current_word in visited:
                continue
                
            visited.add(current_word)
            
            if current_word == end_word:
                return path
            
            for neighbor in self.find_neighbors(current_word):
                if neighbor not in visited:
                    g_new = g_cost + 1  # Uniform step cost
                    h_new = self.hamming_distance(neighbor, end_word)  # Heuristic
                    f_new = g_new + h_new  # f(n) = g(n) + h(n)
                    heapq.heappush(priority_queue, (f_new, g_new, neighbor, path + [neighbor]))
        
        return None
    
    def find_path(self, start_word, end_word, algorithm="A*"):
        """Find path between words using the specified algorithm."""
        if algorithm == "BFS":
            return self.bfs(start_word, end_word)
        elif algorithm == "UCS":
            return self.ucs(start_word, end_word)
        elif algorithm == "A*":
            return self.a_star(start_word, end_word)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
    
    def validate_move(self, word, prev_word):
        """Check if a word is a valid move from the previous word."""
        if not word in self.dictionary:
            return False, "Word not in dictionary"
        
        if not self.is_one_letter_different(prev_word, word):
            return False, "Must change exactly one letter"
        
        return True, "Valid move"
    
    def setup_ui(self):
        """Set up the game user interface with improved styling."""
        self.root = tk.Tk()
        self.root.title("Word Ladder Adventure Game")
        self.root.geometry("1280x720")
        
        # Make the window fullscreen by default
        self.root.attributes('-fullscreen', True)
        
        # Add key binding to exit fullscreen with Escape key
        self.root.bind("<Escape>", lambda event: self.root.attributes("-fullscreen", False))
        
        # Modern color palette
        self.colors = {
            'bg_dark': '#1F2544',       # Dark navy
            'bg_medium': '#474F7A',     # Navy blue
            'accent': '#81689D',        # Purple
            'highlight': '#FFD0EC',     # Light pink
            'text_light': '#FFFFFF',    # Pure white for maximum contrast
            'text_medium': '#FFD0EC',   # Light pink for better visibility
            'success': '#81689D',       # Using purple
            'warning': '#474F7A',       # Using navy blue
            
            # Updated node colors with green start and red end
            'node_start': '#2E8B57',    # Sea Green for start node
            'node_end': '#CD5C5C',      # Indian Red for end node
            'node_current': '#FFD0EC',  # Light pink for intermediate nodes
            'node_path': '#FFD0EC',     # Light pink for intermediate nodes
            'node_text_dark': '#1F2544',# Dark text for pink nodes
            'node_text_light': '#FFFFFF'# White text for colored nodes
        }
        
        # Configure ttk styles with the new color palette
        style = ttk.Style()
        
        # Configure the theme
        style.theme_use('clam')  # Use clam as base theme for better customization
        
        # Configure styles with new colors and rounded elements
        style.configure('Title.TLabel', 
                       font=('Poppins', 28, 'bold'), 
                       foreground='#FFFFFF',  # Pure white for titles
                       background=self.colors['bg_dark'])
        
        style.configure('Game.TLabel', 
                       font=('Poppins', 12), 
                       foreground='#FFFFFF',  # Pure white for regular labels
                       background=self.colors['bg_dark'])
        
        style.configure('Game.TFrame', 
                       background=self.colors['bg_dark'])
        
        # Custom button style with rounded corners
        style.configure('Game.TButton', 
                       font=('Poppins', 11),
                       background=self.colors['accent'],
                       foreground=self.colors['text_light'],
                       borderwidth=0,
                       focusthickness=0,
                       padding=(10, 5))
        
        # Hover effect for buttons
        style.map('Game.TButton',
                 background=[('active', self.colors['highlight'])],
                 foreground=[('active', self.colors['text_light'])])
        
        # Main frame
        main_frame = ttk.Frame(self.root, style='Game.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title with animation effect
        title_frame = ttk.Frame(main_frame, style='Game.TFrame')
        title_frame.pack(fill=tk.X, pady=(20, 25))
        
        title_label = ttk.Label(title_frame, text="Word Ladder Adventure",
                               style='Title.TLabel', padding="10")
        title_label.pack()
        
        # Animate title appearance
        def animate_title(count=0, direction=1):
            # Pulse animation for title
            size = 28 + int(count/10)  # Convert to integer
            title_label.configure(font=('Poppins', size, 'bold'))
            
            if count >= 5:
                direction = -1
            elif count <= 0:
                direction = 1
            
            count += direction
            title_frame.after(100, lambda: animate_title(count, direction))
        
        title_frame.after(100, animate_title)
        
        # Game controls frame with gradient background
        controls_frame = ttk.Frame(main_frame, style='Game.TFrame')
        controls_frame.pack(fill=tk.X, padx=30, pady=10)
        
        # Left side - Game Mode
        mode_frame = ttk.Frame(controls_frame, style='Game.TFrame')
        mode_frame.pack(side=tk.LEFT, padx=(0, 30))
        ttk.Label(mode_frame, text="Game Mode:", style='Game.TLabel').pack(side=tk.LEFT, padx=5)
        self.mode_var = tk.StringVar(value="Beginner")
        
        # Custom combobox style
        style.configure('Game.TCombobox', 
                       fieldbackground=self.colors['bg_medium'],
                       background=self.colors['accent'],
                       foreground=self.colors['text_light'],
                       arrowcolor=self.colors['text_light'],
                       font=('Poppins', 11))
        
        mode_combo = ttk.Combobox(mode_frame, textvariable=self.mode_var,
                                 values=["Beginner", "Advanced", "Challenge"],
                                 width=10, state='readonly', font=('Poppins', 11),
                                 style='Game.TCombobox')
        mode_combo.pack(side=tk.LEFT, padx=5)
        
        # Right side - Algorithm
        algo_frame = ttk.Frame(controls_frame, style='Game.TFrame')
        algo_frame.pack(side=tk.RIGHT, padx=(30, 0))
        ttk.Label(algo_frame, text="Algorithm:", style='Game.TLabel').pack(side=tk.LEFT, padx=5)
        self.algorithm_var = tk.StringVar(value="A*")
        algorithm_combo = ttk.Combobox(algo_frame, textvariable=self.algorithm_var,
                                     values=["BFS", "UCS", "A*"],
                                     width=6, state='readonly', font=('Poppins', 11),
                                     style='Game.TCombobox')
        algorithm_combo.pack(side=tk.LEFT, padx=5)
        
        # Start Game button with hover effect
        start_button = ttk.Button(main_frame, text="Start New Game",
                                 command=self.start_game,
                                 style='Game.TButton',
                                 padding="12 8")
        start_button.pack(pady=15)
        
        # Word display frame (graph)
        self.word_frame = ttk.Frame(main_frame, style='Game.TFrame')
        self.word_frame.pack(fill=tk.BOTH, expand=True, pady=15)
        
        # Word entry section - Create but don't pack initially
        self.entry_frame = ttk.Frame(main_frame, style='Game.TFrame')
        
        ttk.Label(self.entry_frame, text="Enter word:", style='Game.TLabel').pack(side=tk.LEFT, padx=5)
        
        # Custom entry style
        entry_style = {'background': self.colors['bg_medium'], 
                      'foreground': self.colors['text_light'],
                      'insertbackground': self.colors['highlight'],
                      'relief': 'flat',
                      'borderwidth': 0,
                      'highlightthickness': 1,
                      'highlightcolor': self.colors['highlight'],
                      'highlightbackground': self.colors['accent']}
        
        self.word_entry = tk.Entry(self.entry_frame, width=15, font=('Poppins', 12), **entry_style)
        self.word_entry.pack(side=tk.LEFT, padx=10)
        
        submit_btn = ttk.Button(self.entry_frame, text="Submit",
                               command=self.submit_word,
                               style='Game.TButton',
                               padding="8 6")
        submit_btn.pack(side=tk.LEFT, padx=5)
        
        # Game info frame
        self.info_frame = ttk.Frame(main_frame, style='Game.TFrame')
        self.info_frame.pack(fill=tk.X, padx=30, pady=10)
        
        # Add message text widget with improved styling
        message_frame = ttk.Frame(main_frame, style='Game.TFrame')
        message_frame.pack(fill=tk.X, padx=30, pady=10)
        
        self.message_text = tk.Text(message_frame, 
                                   height=3,
                                   wrap=tk.WORD,
                                   font=('Poppins', 11),
                                   bg=self.colors['bg_medium'],
                                   fg='#FFFFFF',
                                   relief=tk.FLAT,
                                   padx=15,
                                   pady=10,
                                   state='disabled',
                                   borderwidth=0,
                                   highlightthickness=1,
                                   highlightcolor=self.colors['highlight'],
                                   highlightbackground=self.colors['accent'])
        self.message_text.pack(fill=tk.X, expand=True)
        
        # Bottom buttons frame
        bottom_frame = ttk.Frame(main_frame, style='Game.TFrame')
        bottom_frame.pack(fill=tk.X, padx=30, pady=15)
        
        # Left side buttons
        self.hint_button = ttk.Button(bottom_frame, text="Get Hint",
                                command=self.get_hint,
                                style='Game.TButton',
                                padding="8 6",
                                state='disabled')  # Disabled initially
        self.hint_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = ttk.Button(bottom_frame, text="Reset Game",
                                 command=self.reset_game,
                                 style='Game.TButton',
                                 padding="8 6",
                                 state='disabled')  # Disabled initially
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Auto-solve button
        self.auto_solve_button = ttk.Button(bottom_frame, text="Auto Solve",
                                      command=self.auto_solve,
                                      style='Game.TButton',
                                      padding="8 6",
                                      state='disabled')  # Disabled initially
        self.auto_solve_button.pack(side=tk.LEFT, padx=5)
        
        # Compare algorithms button
        self.compare_button = ttk.Button(bottom_frame, text="Compare Algorithms",
                                   command=self.compare_algorithms,
                                   style='Game.TButton',
                                   padding="8 6",
                                   state='disabled')  # Disabled initially
        self.compare_button.pack(side=tk.LEFT, padx=5)
        
        # Exit button on right
        exit_button = ttk.Button(bottom_frame, text="Exit",
                                command=self.root.quit,
                                style='Game.TButton',
                                padding="8 6")
        exit_button.pack(side=tk.RIGHT, padx=5)
    
    def set_message(self, message):
        """Update the message text widget."""
        self.message_text.config(state='normal')  # Temporarily enable for editing
        self.message_text.delete(1.0, tk.END)
        self.message_text.insert(tk.END, message)
        self.message_text.see(tk.END)  # Scroll to show the latest message
        self.message_text.config(state='disabled')  # Disable editing again
    
    def submit_word(self):
        """Handle word submission."""
        word = self.word_entry.get().strip().lower()
        
        if not word:
            self.set_message("Please enter a word.")
            return
        
        if len(self.tries) >= self.max_tries[self.game_mode]:
            self.set_message(f"You've reached the maximum number of tries ({self.max_tries[self.game_mode]}).")
            return
        
        # Get previous word
        prev_word = self.start_word if not self.tries else self.tries[-1]
        
        # Validate move
        if self.game_mode == "Challenge":
            if any(letter in self.restricted_letters for letter in word):
                self.set_message(f"Word contains restricted letters: {', '.join(self.restricted_letters)}")
                return
            if word in self.banned_words:
                self.set_message(f"This word is banned in challenge mode")
                return
        
        valid, message = self.validate_move(word, prev_word)
        if valid:
            self.tries.append(word)
            self.update_word_display()
            
            if word == self.end_word:
                score = self.calculate_score()
                win_message = (
                    f"🎉 Congratulations! You've completed the word ladder! 🎉\n"
                    f"Path: {' → '.join([self.start_word] + self.tries)}\n"
                    f"Steps taken: {len(self.tries)} (Minimum possible: {self.min_tries})\n"
                    f"Score: {score}/10"
                )
                self.set_message(win_message)
                self.show_graph()
            else:
                self.set_message(f"Valid move from '{prev_word}' to '{word}'")
        else:
            self.set_message(message)
        
        self.word_entry.delete(0, tk.END)
    
    def update_word_display(self):
        """Update the display of the word ladder with dynamic graph visualization."""
        # Clear existing display
        for widget in self.word_frame.winfo_children():
            widget.destroy()
        
        # Create canvas for drawing
        canvas_width = min(1200, max(600, (len(self.tries) + 2) * 100))
        canvas_height = 200
        canvas = tk.Canvas(self.word_frame, 
                          width=canvas_width,
                          height=canvas_height,
                          bg=self.colors['bg_dark'],
                          highlightthickness=0)
        canvas.pack(pady=10)
        
        # Get all words in the current path plus end word
        words = [self.start_word] + self.tries
        if words[-1] != self.end_word:  # Add end word if not reached
            words.append(self.end_word)
        
        num_words = len(words)
        
        # Fixed node properties
        node_radius = 30
        node_spacing = 100
        
        # Calculate starting x position to center the graph
        start_x = (canvas_width - (num_words - 1) * node_spacing) / 2
        center_y = canvas_height / 2
        
        # Draw edges (lines) first
        for i in range(num_words - 1):
            x1 = start_x + i * node_spacing
            x2 = start_x + (i + 1) * node_spacing
            # Use dashed line for connection to end word if not reached
            if i == len(self.tries) and words[-2] != self.end_word:
                canvas.create_line(x1, center_y, x2, center_y, 
                                 fill=self.colors['text_medium'], 
                                 width=2,
                                 dash=(5, 5))  # Dashed line
            else:
                canvas.create_line(x1, center_y, x2, center_y, 
                                 fill=self.colors['text_light'], 
                                 width=2)
        
        # Draw nodes with animation
        for i, word in enumerate(words):
            x = start_x + i * node_spacing
            is_start = (i == 0)
            is_end = (word == self.end_word)
            is_current = (i == len(self.tries))
            
            # Draw the node with a remove button if it's not the start or end word
            # and it's part of the current path (not the target word)
            can_remove = not is_start and not is_end and i <= len(self.tries)
            
            # Animate node appearance with a delay based on position
            canvas.after(i * 100, lambda c=canvas, x=x, y=center_y, w=word, s=is_start, 
                        curr=is_current, e=is_end, cr=can_remove, idx=i-1: 
                        self.draw_node(c, x, y, w, s, curr, e, cr, idx))
        
        # Show tries remaining
        tries_left = self.max_tries[self.game_mode] - len(self.tries)
        
        # Clear previous tries label
        for widget in self.info_frame.winfo_children():
            widget.destroy()
        
        tries_label = ttk.Label(self.info_frame,
                               text=f"Tries remaining: {tries_left}",
                               style='Game.TLabel')
        tries_label.pack(pady=5)
    
    def draw_node(self, canvas, x, y, word, is_start=False, is_current=False, is_end=False, can_remove=False, word_index=None):
        """Draw a node with word label and optional remove button with animation."""
        node_radius = 30
        
        # Select node color based on node type
        if is_start:
            node_color = self.colors['node_start']  # Green for start
            text_color = self.colors['node_text_light']  # White text
        elif is_end:
            node_color = self.colors['node_end']    # Red for end
            text_color = self.colors['node_text_light']  # White text
        else:
            node_color = self.colors['node_current']  # Pink for intermediate
            text_color = self.colors['node_text_dark']   # Dark text
        
        # Draw the node
        for r in range(1, node_radius + 1, 3):
            canvas.after(r * 3, lambda r=r: canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=node_color, outline=self.colors['text_light'], width=2))
        
        # Draw word label with appropriate text color
        canvas.after(node_radius * 3 + 10, lambda: canvas.create_text(
            x, y, text=word.upper(), fill=text_color,
            font=('Poppins', 11, 'bold')))
        
        # Add remove button (X) if this word can be removed
        if can_remove:
            # Create a small circle for the X button
            button_radius = 8
            button_x = x + node_radius - 5
            button_y = y - node_radius + 5
            
            # Draw button background with delay
            canvas.after(node_radius * 3 + 20, lambda: self._draw_remove_button(
                canvas, button_x, button_y, button_radius, word_index))
    
    def _draw_remove_button(self, canvas, x, y, radius, word_index):
        """Helper method to draw the remove button with animation."""
        # Draw button background
        button_id = canvas.create_oval(
            x - radius, y - radius,
            x + radius, y + radius,
            fill=self.colors['highlight'], outline=self.colors['text_light'])
        
        # Draw X
        x_id = canvas.create_text(
            x, y,
            text="×",
            fill=self.colors['text_light'],
            font=('Poppins', 11, 'bold'))
        
        # Bind click events to remove the word
        def remove_word(event, idx=word_index):
            self.remove_word_at_index(idx)
        
        canvas.tag_bind(button_id, '<Button-1>', remove_word)
        canvas.tag_bind(x_id, '<Button-1>', remove_word)
    
    def remove_word_at_index(self, index):
        """Remove a word from the tries list at the specified index."""
        if 0 <= index < len(self.tries):
            # Store the word being removed for the message
            removed_word = self.tries[index]
            
            # Remove the word and all words that come after it
            self.tries = self.tries[:index]
            self.update_word_display()
            
            # Update message
            if self.tries:
                last_word = self.tries[-1]
                self.set_message(f"Removed '{removed_word}' and subsequent words. Current position: '{last_word}'")
            else:
                self.set_message(f"Removed '{removed_word}' and subsequent words. Current position: '{self.start_word}'")
            
            # Clear the entry field to allow for new input
            self.word_entry.delete(0, tk.END)
    
    def start_game(self):
        """Start a new game with the given parameters."""
        # Setup game mode
        mode = self.mode_var.get()
        self.setup_game_mode(mode)
        
        # Select random words for the current mode
        self.start_word, self.end_word = self.select_random_words()
        
        # Calculate max tries based on minimum path
        self.max_tries[mode], self.min_tries = self.calculate_max_tries()
        
        # Reset game state
        self.tries = []
        self.current_path = [self.start_word]
        
        # Calculate optimal path
        algorithm = self.algorithm_var.get()
        self.optimal_path = self.find_path(self.start_word, self.end_word, algorithm)
        
        if not self.optimal_path:
            self.set_message(f"No path found between '{self.start_word}' and '{self.end_word}'. Trying new words...")
            self.start_game()  # Retry with new words
            return
        
        # Show the entry frame now that the game has started
        # Move the entry frame to appear above the info frame
        self.entry_frame.pack(fill=tk.X, padx=20, pady=5, before=self.info_frame)
        
        # Enable game control buttons
        self.hint_button.config(state='normal')
        self.reset_button.config(state='normal')
        self.auto_solve_button.config(state='normal')
        self.compare_button.config(state='normal')
        
        # Update UI
        self.update_word_display()
        message = (
            f"Transform '{self.start_word}' to '{self.end_word}'\n\n"
            f"Minimum possible moves: {self.min_tries}\n"
            f"Maximum allowed moves: {self.max_tries[mode]}\n"
            f"Mode: {mode} ({self.word_lengths[mode]}-letter words)"
        )
        
        if mode == "Challenge":
            message += (
                f"\n\nBanned words: {', '.join(self.banned_words)}\n"
                f"Restricted letters: {', '.join(self.restricted_letters)}"
            )
            
            # Display challenge mode rules in the message text box
            challenge_rules = (
                f"Challenge Mode Rules:\n"
                f"1. You cannot use words containing: {', '.join(self.restricted_letters)}\n"
                f"2. You cannot use these banned words: {', '.join(self.banned_words)}\n"
                f"3. You still need to change exactly one letter at a time"
            )
            self.set_message(challenge_rules)
        else:
            # Set a standard message for non-challenge modes
            self.set_message(f"Game started! Transform '{self.start_word}' to '{self.end_word}' by changing one letter at a time.")
        
        # Add auto-solve option to initial popup
        message += "\n\nYou can either:\n- Play manually\n- Click 'Auto Solve' to watch AI solve it"
        
        self.show_game_info(message)
    
    def get_hint(self):
        """Provide a hint by suggesting the next optimal word."""
        if not hasattr(self, 'optimal_path') or not self.optimal_path:
            self.show_game_info("Start a game first to get hints.")
            return
        
        # Get the current word (either start word or last tried word)
        current_word = self.start_word if not self.tries else self.tries[-1]
        
        # Find where we are in the optimal path
        try:
            current_index = self.optimal_path.index(current_word)
            if current_index < len(self.optimal_path) - 1:
                next_word = self.optimal_path[current_index + 1]
                self.show_game_info(f"Hint: Try using '{next_word}'")
                # Auto-fill the entry box with the hint
                self.word_entry.delete(0, tk.END)
                self.word_entry.insert(0, next_word)
            else:
                self.show_game_info("You're at the end! Try to reach the target word.")
        except ValueError:
            # If current word is not in optimal path, suggest the next word from start
            self.show_game_info(f"Hint: Try using '{self.optimal_path[1]}'")
            self.word_entry.delete(0, tk.END)
            self.word_entry.insert(0, self.optimal_path[1])
    
    def reset_game(self):
        """Reset the current game."""
        # Reset tries
        self.tries = []
        self.update_word_display()
        
        # Clear entry field
        self.word_entry.delete(0, tk.END)
        
        # Update message
        self.set_message("Game reset. Try to transform the start word to the end word.")
    
    def setup_game_mode(self, mode):
        """Configure game settings based on mode."""
        self.game_mode = mode
        word_length = self.word_lengths[mode]
        
        # Filter dictionary by word length for the current mode
        self.active_dictionary = {word for word in self.dictionary if len(word) == word_length}
        
        if mode == "Challenge":
            # Select random banned words and restricted letters
            self.banned_words = set(random.sample(list(self.active_dictionary), 5))
            self.restricted_letters = set(random.sample('abcdefghijklmnopqrstuvwxyz', 3))
            # Remove banned words from active dictionary
            self.active_dictionary -= self.banned_words
        else:
            self.banned_words = set()
            self.restricted_letters = set()
    
    def select_random_words(self):
        """Select random start and end words based on current game mode."""
        # Filter words based on current game mode's word length
        word_length = self.word_lengths[self.game_mode]
        valid_words = {word for word in self.dictionary if len(word) == word_length}
        
        if len(valid_words) < 2:
            self.set_message("Not enough words in dictionary for this mode. Using default words.")
            return "cat", "dog"  # Fallback
        
        # Keep trying until we find a pair with a valid path of appropriate length
        min_path_length = {
            "Beginner": 3,  # At least 2 moves (3 words including start and end)
            "Advanced": 4,  # At least 3 moves (4 words including start and end)
            "Challenge": 4  # At least 3 moves (4 words including start and end)
        }
        
        required_length = min_path_length[self.game_mode]
        
        for _ in range(100):  # Limit attempts to avoid infinite loop
            start_word = random.choice(list(valid_words))
            end_word = random.choice(list(valid_words))
            
            if start_word != end_word:
                # Verify that a path exists between the words
                test_path = self.find_path(start_word, end_word, self.algorithm_var.get())
                if test_path and len(test_path) >= required_length:
                    return start_word, end_word
        
        # If no valid pair found after 100 attempts, use appropriate defaults
        if self.game_mode == "Beginner":
            return "cat", "dog"  # Requires: cat -> hat -> hot -> dot -> dog
        elif self.game_mode == "Advanced":
            return "stone", "money"  # Requires multiple steps
        else:  # Challenge mode
            return "stone", "break"  # Requires multiple steps
    
    def calculate_max_tries(self):
        """Calculate maximum tries based on minimum path length."""
        # Find minimum path length using A* (most efficient)
        optimal_path = self.find_path(self.start_word, self.end_word, "A*")
        if not optimal_path:
            return 8, 5  # Default fallback if no path found (max_tries, min_tries)
        
        min_tries = len(optimal_path) - 1  # Subtract 1 as path includes start word
        max_tries = min_tries + 3  # Add 3 extra moves for flexibility
        
        return max_tries, min_tries
    
    def calculate_score(self):
        """Calculate score out of 10 based on moves taken vs minimum possible."""
        if not hasattr(self, 'min_tries'):
            return 0
        
        moves_taken = len(self.tries)
        max_allowed = self.max_tries[self.game_mode]
        
        # Score formula:
        # 10 points if completed in minimum tries
        # Linear reduction down to 5 points if used maximum tries
        # Below 5 if went over optimal path but still within max tries
        
        if moves_taken <= self.min_tries:
            score = 10.0  # Perfect score
        else:
            # Calculate score reduction for each extra move
            extra_moves = moves_taken - self.min_tries
            max_extra_moves = max_allowed - self.min_tries
            
            # Score reduces from 10 to 5 over the allowed extra moves
            score = 10.0 - (5.0 * extra_moves / max_extra_moves)
        
        # Ensure score is between 0 and 10
        score = max(0.0, min(10.0, score))
        
        return round(score, 1)
    
    def show_graph(self):
        """Display a simple word ladder graph showing the path taken."""
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title("Word Ladder Path")
        popup.geometry("800x600")
        
        # Create graph
        G = nx.Graph()
        
        # Add nodes and edges for the path taken
        path = [self.start_word] + self.tries
        for i in range(len(path) - 1):
            G.add_edge(path[i], path[i + 1])
        
        # Create figure
        fig = plt.figure(figsize=(8, 6), facecolor='white')
        plt.clf()
        
        # Set layout
        pos = nx.spring_layout(G)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, edge_color='gray')
        
        # Draw nodes
        node_colors = ['lightgreen' if node == self.start_word 
                       else 'lightcoral' if node == self.end_word 
                       else 'lightblue' for node in G.nodes()]
        
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2000)
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        
        plt.title("Word Ladder Path", pad=20)
        plt.axis('off')
        
        # Add to window
        canvas = FigureCanvasTkAgg(fig, master=popup)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add close button
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
    
    def show_game_info(self, message):
        """Show game information in a popup window with improved styling."""
        popup = tk.Toplevel(self.root)
        popup.title("Game Information")
        popup.geometry("400x300")
        popup.configure(bg=self.colors['bg_dark'])
        
        # Add a frame with a border effect
        frame = ttk.Frame(popup, style='Game.TFrame')
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        text = tk.Text(frame, 
                      wrap=tk.WORD,
                      font=('Poppins', 11),  
                      bg=self.colors['bg_medium'],
                      fg='#FFFFFF',
                      relief=tk.FLAT,
                      padx=20,
                      pady=20,
                      borderwidth=0,
                      highlightthickness=1,
                      highlightcolor=self.colors['highlight'],
                      highlightbackground=self.colors['accent'])
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text.insert(tk.END, message)
        text.configure(state='disabled')
        
        # Create a custom OK button
        ok_button = ttk.Button(popup, 
                              text="OK", 
                              command=popup.destroy,
                              style='Game.TButton',
                              padding="10 5")
        ok_button.pack(pady=15)
        
        # Center the popup on the screen
        popup.update_idletasks()
        width = popup.winfo_width()
        height = popup.winfo_height()
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        # Make popup appear with a fade-in effect
        popup.attributes('-alpha', 0.0)
        
        def fade_in(alpha=0.0):
            alpha += 0.1
            popup.attributes('-alpha', alpha)
            if alpha < 1.0:
                popup.after(20, lambda: fade_in(alpha))
        
        popup.after(0, fade_in)
    
    def auto_solve(self):
        """Automatically solve the word ladder with animation."""
        if not hasattr(self, 'optimal_path') or not self.optimal_path:
            self.show_game_info("Start a game first to see the solution.")
            return
        
        # Disable buttons during animation
        self.disable_buttons()
        
        # Reset game state
        self.tries = []
        self.update_word_display()
        
        # Create popup for solution animation
        popup = tk.Toplevel(self.root)
        popup.title("Auto-Solving Word Ladder")
        popup.geometry("600x400")
        popup.configure(bg='#2C3E50')
        
        # Get the current algorithm
        algorithm = self.algorithm_var.get()
        
        # Add info label
        info_label = ttk.Label(popup, 
                              text=f"Watch as AI solves the word ladder using {algorithm} algorithm...",
                              style='Game.TLabel',
                              padding="20")
        info_label.pack(pady=20)
        
        # Add statistics label
        stats_label = ttk.Label(popup,
                               text="",
                               style='Game.TLabel',
                               padding="20")
        stats_label.pack(pady=10)
        
        # Function to update solution step by step
        def animate_solution():
            if len(self.tries) < len(self.optimal_path) - 1:
                next_word = self.optimal_path[len(self.tries) + 1]
                self.tries.append(next_word)
                self.update_word_display()
                
                # Update info label
                step_num = len(self.tries)
                total_steps = len(self.optimal_path) - 1
                info_label.config(text=f"Step {step_num} of {total_steps}: {next_word}")
                
                # Update statistics
                stats_text = (
                    f"Current path: {' → '.join([self.start_word] + self.tries)}\n"
                    f"Steps taken: {step_num} of {self.min_tries} (minimum)\n"
                    f"Tries remaining: {self.max_tries[self.game_mode] - step_num}\n"
                    f"Algorithm: {algorithm}"
                )
                stats_label.config(text=stats_text)
                
                # Schedule next step
                if len(self.tries) < len(self.optimal_path) - 1:
                    popup.after(1000, animate_solution)
                else:
                    # Calculate final score
                    score = self.calculate_score()
                    
                    # Show completion message with statistics
                    completion_text = (
                        "Solution Complete! 🎉\n\n"
                        f"Path: {' → '.join([self.start_word] + self.tries)}\n"
                        f"Steps taken: {len(self.tries)} (Minimum possible: {self.min_tries})\n"
                        f"Score: {score}/10\n"
                        f"Algorithm: {algorithm}\n\n"
                        "This was the optimal solution found by the AI!"
                    )
                    info_label.config(text=completion_text)
                    stats_label.config(text="")  # Clear the stats label
                    
                    self.enable_buttons()
                    # Add close button
                    ttk.Button(popup, 
                              text="Close",
                              command=popup.destroy,
                              style='Game.TButton',
                              padding="8 4").pack(pady=20)
        
        # Start animation
        popup.after(1000, animate_solution)

    def disable_buttons(self):
        """Disable all game buttons during auto-solve."""
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.configure(state='disabled')

    def enable_buttons(self):
        """Re-enable all game buttons after auto-solve."""
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.configure(state='normal')
    
    def compare_algorithms(self):
        """Compare the performance of different algorithms on the current word ladder."""
        if not hasattr(self, 'start_word') or not hasattr(self, 'end_word'):
            self.show_game_info("Start a game first to compare algorithms.")
            return
        
        # Disable buttons during comparison
        self.disable_buttons()
        
        # Create popup for algorithm comparison
        popup = tk.Toplevel(self.root)
        popup.title("Algorithm Comparison")
        popup.geometry("800x600")
        popup.configure(bg='#2C3E50')
        
        # Add title label
        title_label = ttk.Label(popup, 
                               text=f"Comparing Algorithms: {self.start_word} → {self.end_word}",
                               style='Game.TLabel',
                               font=('Helvetica', 14, 'bold'),
                               padding="10")
        title_label.pack(pady=5)
        
        # Create a frame for the visualization
        viz_frame = ttk.Frame(popup, style='Game.TFrame')
        viz_frame.pack(fill=tk.X, expand=False, padx=20, pady=5)
        
        # Create canvas for path visualization
        canvas_width = 700
        canvas_height = 150
        canvas = tk.Canvas(viz_frame, 
                          width=canvas_width,
                          height=canvas_height,
                          bg='#2C3E50',
                          highlightthickness=0)
        canvas.pack(pady=5)
        
        # Create a frame for the results
        results_frame = ttk.Frame(popup, style='Game.TFrame')
        results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Create a text widget to display results
        results_text = tk.Text(results_frame, 
                              height=15,
                              wrap=tk.WORD,
                              font=('Helvetica', 11),
                              bg='#34495E',
                              fg='#ECF0F1',
                              relief=tk.FLAT,
                              padx=15,
                              pady=15)
        results_text.pack(fill=tk.BOTH, expand=True)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=results_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        results_text.configure(yscrollcommand=scrollbar.set)
        
        # Add initial message
        results_text.insert(tk.END, "Running comparison of BFS, UCS, and A* algorithms...\n\n")
        results_text.see(tk.END)
        
        # Add current algorithm label
        current_algo_label = ttk.Label(popup, 
                                      text="",
                                      style='Game.TLabel',
                                      font=('Helvetica', 12, 'bold'),
                                      padding="5")
        current_algo_label.pack(pady=5)
        
        # Dictionary to store results
        results = {}
        
        # Function to visualize a path on the canvas
        def visualize_path(path, algorithm_name):
            # Clear canvas
            canvas.delete("all")
            
            if not path:
                canvas.create_text(canvas_width/2, canvas_height/2, 
                                  text="No path found", 
                                  fill='#ECF0F1',
                                  font=('Helvetica', 14))
                return
            
            # Node properties
            node_radius = 25
            node_spacing = min(80, (canvas_width - 100) / (len(path) - 1))
            
            # Calculate starting position to center the path
            start_x = (canvas_width - (len(path) - 1) * node_spacing) / 2
            center_y = canvas_height / 2
            
            # Draw algorithm name
            canvas.create_text(canvas_width/2, 20, 
                              text=f"Algorithm: {algorithm_name}", 
                              fill='#ECF0F1',
                              font=('Helvetica', 12, 'bold'))
            
            # Draw edges first
            for i in range(len(path) - 1):
                x1 = start_x + i * node_spacing
                x2 = start_x + (i + 1) * node_spacing
                canvas.create_line(x1, center_y, x2, center_y, 
                                 fill='#ECF0F1', 
                                 width=2)
            
            # Draw nodes
            for i, word in enumerate(path):
                x = start_x + i * node_spacing
                
                # Select node color
                if i == 0:
                    color = '#2ECC71'  # Green for start
                elif i == len(path) - 1:
                    color = '#E74C3C'  # Red for end
                else:
                    color = '#3498DB'  # Blue for intermediate
                
                # Draw node
                canvas.create_oval(x - node_radius, center_y - node_radius,
                                 x + node_radius, center_y + node_radius,
                                 fill=color, outline='#ECF0F1', width=2)
                
                # Draw word label
                canvas.create_text(x, center_y,
                                 text=word.upper(),
                                 fill='#ECF0F1',
                                 font=('Helvetica', 10, 'bold'))
        
        # Function to run each algorithm and update results
        def run_comparison():
            algorithms = ["BFS", "UCS", "A*"]
            algorithm_colors = {
                "BFS": "#3498DB",  # Blue
                "UCS": "#9B59B6",  # Purple
                "A*": "#2ECC71"    # Green
            }
            
            # Run each algorithm multiple times to get more accurate timing
            num_runs = 5  # Run each algorithm 5 times for more accurate timing
            
            for algorithm in algorithms:
                # Update status and current algorithm label
                current_algo_label.config(text=f"Running: {algorithm}")
                current_algo_label.config(foreground=algorithm_colors[algorithm])
                
                results_text.insert(tk.END, f"Running {algorithm}...\n")
                results_text.see(tk.END)
                popup.update()  # Force UI update
                
                # Measure time with multiple runs for more accuracy
                total_time = 0
                path = None
                
                for run in range(num_runs):
                    start_time = time.perf_counter()  # Use perf_counter for higher precision
                    path = self.find_path(self.start_word, self.end_word, algorithm)
                    end_time = time.perf_counter()
                    total_time += (end_time - start_time)
                
                # Calculate average time
                avg_time = total_time / num_runs
                
                # Calculate metrics
                path_length = len(path) - 1 if path else "No path found"
                
                # Store results
                results[algorithm] = {
                    "time": avg_time,
                    "path_length": path_length,
                    "path": path
                }
                
                # Visualize the path
                visualize_path(path, algorithm)
                
                # Update results display
                results_text.insert(tk.END, f"  - Time: {avg_time:.8f} seconds (avg of {num_runs} runs)\n")
                results_text.insert(tk.END, f"  - Path length: {path_length}\n")
                if path:
                    results_text.insert(tk.END, f"  - Path: {' → '.join(path)}\n")
                results_text.insert(tk.END, "\n")
                results_text.see(tk.END)
                
                # Pause to show the visualization
                popup.update()
                time.sleep(1)  # Show each algorithm's result for 1 second
            
            # Compare and display summary
            results_text.insert(tk.END, "=== COMPARISON SUMMARY ===\n\n")
            
            # Find fastest algorithm
            fastest = min(algorithms, key=lambda x: results[x]["time"])
            
            # Find algorithm with shortest path (they should all be the same length)
            path_lengths = {alg: results[alg]["path_length"] for alg in algorithms if isinstance(results[alg]["path_length"], int)}
            
            # Display summary
            fastest_time = results[fastest]["time"]
            if fastest_time > 0.000001:  # Ensure we have a meaningful time measurement
                results_text.insert(tk.END, f"Fastest algorithm: {fastest} ({results[fastest]['time']:.8f} seconds)\n")
                
                if path_lengths:
                    shortest = min(path_lengths, key=path_lengths.get)
                    results_text.insert(tk.END, f"Shortest path: {shortest} (length: {path_lengths[shortest]})\n\n")
                
                # Performance comparison as percentage
                results_text.insert(tk.END, "Performance comparison (time):\n")
                for alg in algorithms:
                    time_ratio = results[alg]["time"] / fastest_time
                    percentage = (time_ratio - 1) * 100
                    if alg == fastest:
                        results_text.insert(tk.END, f"  - {alg}: Baseline (fastest)\n")
                    else:
                        results_text.insert(tk.END, f"  - {alg}: {percentage:.2f}% slower than {fastest}\n")
            else:
                results_text.insert(tk.END, "All algorithms completed too quickly for accurate timing comparison.\n")
                results_text.insert(tk.END, "Try with longer words or a more complex word ladder.\n")
                
                # Just show the raw times
                results_text.insert(tk.END, "\nRaw timing results:\n")
                for alg in algorithms:
                    results_text.insert(tk.END, f"  - {alg}: {results[alg]['time']:.8f} seconds\n")
            
            # Update current algorithm label
            current_algo_label.config(text=f"Fastest Algorithm: {fastest}")
            current_algo_label.config(foreground=algorithm_colors[fastest])
            
            # Show the fastest algorithm's path
            if results[fastest]["path"]:
                visualize_path(results[fastest]["path"], f"{fastest} (Fastest)")
            
            # Re-enable buttons
            self.enable_buttons()
            
            # Add close button
            ttk.Button(popup, 
                      text="Close",
                      command=popup.destroy,
                      style='Game.TButton',
                      padding="8 4").pack(pady=10)
        
        # Run comparison after a short delay to allow UI to update
        popup.after(100, run_comparison)
    
    def run(self):
        """Run the game."""
        self.setup_ui()
        self.root.mainloop()

# Example usage
if __name__ == "__main__":
    game = WordLadderGame()
    game.run()


