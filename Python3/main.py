import tkinter as tk
from tkinter import font
from random import choice

import config


# Other Setup
DIFFICULTIES = { # Difficulty Name, Value
                "Easy (250 Words)": "easy",
                "Normal (1000 Words)": "normal",
                "Hard (3000 Words)": "hard",
                "Custom": "custom"
                }


class Application(tk.Tk): # Application Class Object
    def __init__(self):
        super().__init__() # Superclass (tk.Tk)
        
        self.title(f"{config.PROGRAM_NAME} | {config.BUILD_VERSION} | By {config.AUTHOR}") # Window Title
        self.geometry("500x250") # Window Size (Template)
        self.resizable(0, 0) # not Resizable
        
        # Fonts
        self.hel15b = font.Font(family="Helvetica", size=15, weight="bold") # Font (Helvetica, 15, Bold)
        self.sys20bu = font.Font(family="system", size=20, weight="bold", underline=1) # Font (system, 20, Bold, Underline)
        self.bu = font.Font(weight="bold", underline=1) # Font (Bold, Underline) 
        self.bold = font.Font(weight="bold") # Font (Bold)


        # Other
        self.back_image = tk.PhotoImage(file="./Other/back.png") # back.png for Back Icon

    def __repr__(self):
        __name = self.__class__
        __type = type(self)
        __module = type.__module__
        __qualname = type.__qualname__

        return f"""\
        Class Name: {__name}
        Class Details: {config.PROGRAM_NAME}

        Build Version: {config.BUILD_VERSION}
        Author: {config.AUTHOR}
        
        Class Type: {__type}
        Class Module: {__module}
        Class Qualname: {__qualname}
        """

    def back(self): # Back Button
        self.destroy() # Destroy Window
        
        setup() # Run Main Menu Setup


class EndMessage(Application): # End Message/PopUp
    def __init__(self, state, word, newhighstreak=0):
        super().__init__() # Superclass (Application)s

        self.state = state # Win/Loss
        self.word = word.upper() # Previous Word
        self.newhighstreak = newhighstreak # (1) Yes / (0) No

        self.flash_colors = ("goldenrod", "orange4") # Flashing Colors
        self.flash_delay = 400 # Flash Delay (ms)

        self.geometry("400x200") # Window Size (OVERRIDE)

        # Window Contents

        if self.state == 1: # If Won
            tk.Label(self, text="You Won with the word...", font=self.bu).place(x=200, y=25, anchor="center") # Win Label
            tk.Label(self, text=self.word, font=self.hel15b, fg="lime green").place(x=200, y=65, anchor="center") # Word Label
            
            if self.newhighstreak == 1: # If new High Streak
                self.newhighstreak_tk = tk.Label(self, text="NEW HIGH STREAK!", font=self.bold, fg=self.flash_colors[0])
                self.newhighstreak_tk.place(x=200, y=100, anchor="center") # NEW HIGH STREAK!
        
        elif self.state == 0: # If Lose
            tk.Label(self, text="You Lost with the word...", font=self.bu).place(x=200, y=25, anchor="center")
            tk.Label(self, text=self.word, font=self.hel15b, fg="red2").place(x=200, y=65, anchor="center") # Word Label
        
        tk.Button(self, text="OK", width=5, command=self.back).place(x=200, y=150, anchor="center") # Go Back

        if self.newhighstreak == 1: # If new High Streak
            self.flashWin(self.newhighstreak_tk, 0) # Flash Label

    def flashWin(self, object, color_index): # Flash Green/Red
        object.config(foreground = self.flash_colors[color_index])

        self.after(self.flash_delay, self.flashWin, object, 1 - color_index)


class Game(Application): # Main Game
    def __init__(self, difficulty):
        super().__init__() # Superclass (Application)

        self.geometry("750x500") # Window Size (OVERRIDE)
        
        self.difficulty = difficulty # Difficulty

        # Game Setup
        with open(f"./Other/{self.difficulty}.txt", "r") as wordFile: # Read File of Words
            if not wordFile.read(1): # If Empty
                raise FileNotFoundError("File is Empty")
            
            else:
                wordFile.seek(0) # Return to Start
                word_list = [] # List of Words (init)

                try:
                    for word in wordFile: # For word in File of Words
                        word_list.append((word.lower()).strip("\n")) # Append word to List of Words (removing the "\n")
                except Exception as e:
                    print(f"FILE ERROR: {e}")

        self.selected_word = choice(word_list) # Random Word
        self.letters_of_word = [None] * len(self.selected_word) # Unknown Letters in word
        self.number_of_incorrect_guesses = 0 # Incorrect Guesses

        self.word_label_tk = tk.StringVar() # Word Label Tk
        self.guesses_left_tk = tk.IntVar() # Guesses Left Label Tk

        self.update_word_label() # Update Word Label
        self.guesses_left_tk.set(config.TOTAL_GUESSES_ALLOWED - self.number_of_incorrect_guesses) # Calculate Guesses left (start)

        # Window Contents
        tk.Label(self, textvariable=self.word_label_tk, font=self.hel15b, wraplengt=450).place(x=375, y=100, anchor="center") # Word Label

        self.letter_a = tk.Button(self, text="a", command=lambda: self.take_guess("a"), width=2, height=2)
        self.letter_a.place(x=175, y=350, anchor="center") # Letter "a" (Button)
        self.letter_b = tk.Button(self, text="b", command=lambda: self.take_guess("b"), width=2, height=2)
        self.letter_b.place(x=400, y=400, anchor="center") # Letter "b" (Button)
        self.letter_c = tk.Button(self, text="c", command=lambda: self.take_guess("c"), width=2, height=2)
        self.letter_c.place(x=300, y=400, anchor="center") # Letter "c" (Button)
        self.letter_d = tk.Button(self, text="d", command=lambda: self.take_guess("d"), width=2, height=2)
        self.letter_d.place(x=275, y=350, anchor="center") # Letter "d" (Button)
        self.letter_e = tk.Button(self, text="e", command=lambda: self.take_guess("e"), width=2, height=2)
        self.letter_e.place(x=250, y=300, anchor="center") # Letter "e" (Button)
        self.letter_f = tk.Button(self, text="f", command=lambda: self.take_guess("f"), width=2, height=2)
        self.letter_f.place(x=325, y=350, anchor="center") # Letter "f" (Button)
        self.letter_g = tk.Button(self, text="g", command=lambda: self.take_guess("g"), width=2, height=2)
        self.letter_g.place(x=375, y=350, anchor="center") # Letter "g" (Button)
        self.letter_h = tk.Button(self, text="h", command=lambda: self.take_guess("h"), width=2, height=2)
        self.letter_h.place(x=425, y=350, anchor="center") # Letter "h" (Button)
        self.letter_i = tk.Button(self, text="i", command=lambda: self.take_guess("i"), width=2, height=2)
        self.letter_i.place(x=500, y=300, anchor="center") # Letter "i" (Button)
        self.letter_j = tk.Button(self, text="j", command=lambda: self.take_guess("j"), width=2, height=2)
        self.letter_j.place(x=475, y=350, anchor="center") # Letter "j" (Button)
        self.letter_k = tk.Button(self, text="k", command=lambda: self.take_guess("k"), width=2, height=2)
        self.letter_k.place(x=525, y=350, anchor="center") # Letter "k" (Button)
        self.letter_l = tk.Button(self, text="l", command=lambda: self.take_guess("l"), width=2, height=2)
        self.letter_l.place(x=575, y=350, anchor="center") # Letter "l" (Button)
        self.letter_m = tk.Button(self, text="m", command=lambda: self.take_guess("m"), width=2, height=2)
        self.letter_m.place(x=500, y=400, anchor="center") # Letter "m" (Button)
        self.letter_n = tk.Button(self, text="n", command=lambda: self.take_guess("n"), width=2, height=2)
        self.letter_n.place(x=450, y=400, anchor="center") # Letter "n" (Button)
        self.letter_o = tk.Button(self, text="o", command=lambda: self.take_guess("o"), width=2, height=2)
        self.letter_o.place(x=550, y=300, anchor="center") # Letter "o" (Button)
        self.letter_p = tk.Button(self, text="p", command=lambda: self.take_guess("p"), width=2, height=2)
        self.letter_p.place(x=600, y=300, anchor="center") # Letter "p" (Button)
        self.letter_q = tk.Button(self, text="q", command=lambda: self.take_guess("q"), width=2, height=2)
        self.letter_q.place(x=150, y=300, anchor="center") # Letter "q" (Button)
        self.letter_r = tk.Button(self, text="r", command=lambda: self.take_guess("r"), width=2, height=2)
        self.letter_r.place(x=300, y=300, anchor="center") # Letter "r" (Button)
        self.letter_s = tk.Button(self, text="s", command=lambda: self.take_guess("s"), width=2, height=2)
        self.letter_s.place(x=225, y=350, anchor="center") # Letter "s" (Button)
        self.letter_t = tk.Button(self, text="t", command=lambda: self.take_guess("t"), width=2, height=2)
        self.letter_t.place(x=350, y=300, anchor="center") # Letter "t" (Button)
        self.letter_u = tk.Button(self, text="u", command=lambda: self.take_guess("u"), width=2, height=2)
        self.letter_u.place(x=450, y=300, anchor="center") # Letter "u" (Button)
        self.letter_v = tk.Button(self, text="v", command=lambda: self.take_guess("v"), width=2, height=2)
        self.letter_v.place(x=350, y=400, anchor="center") # Letter "v" (Button)
        self.letter_w = tk.Button(self, text="w", command=lambda: self.take_guess("w"), width=2, height=2)
        self.letter_w.place(x=200, y=300, anchor="center") # Letter "w" (Button)
        self.letter_x = tk.Button(self, text="x", command=lambda: self.take_guess("x"), width=2, height=2)
        self.letter_x.place(x=250, y=400, anchor="center") # Letter "x" (Button)
        self.letter_y = tk.Button(self, text="y", command=lambda: self.take_guess("y"), width=2, height=2)
        self.letter_y.place(x=400, y=300, anchor="center") # Letter "y" (Button)
        self.letter_z = tk.Button(self, text="z", command=lambda: self.take_guess("z"), width=2, height=2)
        self.letter_z.place(x=200, y=400, anchor="center") # Letter "z" (Button)

        self.letter_buttons = { # Letter Buttons and their Variables
                               "a": self.letter_a,
                               "b": self.letter_b,
                               "c": self.letter_c,
                               "d": self.letter_d,
                               "e": self.letter_e,
                               "f": self.letter_f,
                               "g": self.letter_g,
                               "h": self.letter_h,
                               "i": self.letter_i,
                               "j": self.letter_j,
                               "k": self.letter_k,
                               "l": self.letter_l,
                               "m": self.letter_m,
                               "n": self.letter_n,
                               "o": self.letter_o,
                               "p": self.letter_p,
                               "q": self.letter_q,
                               "r": self.letter_r,
                               "s": self.letter_s,
                               "t": self.letter_t,
                               "u": self.letter_u,
                               "v": self.letter_v,
                               "w": self.letter_w,
                               "x": self.letter_x,
                               "y": self.letter_y,
                               "z": self.letter_z,
                            }

        tk.Label(self, text="Guesses Left:", font=self.bold).place(x=325, y=475, anchor="center") # Guesses Left Text (Label)
        tk.Label(self, textvariable=self.guesses_left_tk, font=self.bu).place(x=425, y=475, anchor="center") # Guesses Left Number (Label)

        self.back_button = tk.Button(self, command=self.back, image=self.back_image)
        self.back_button.place(x=550, y=400, anchor="center") # Back (Button)

    def take_guess(self, letter):
        button = getattr(self, f"letter_{letter}")

        if letter in self.selected_word:
            button.configure(state="disabled", bg="lime green") # Disable and Color Green Button
            for index, char in enumerate(self.selected_word): # If correct
                if char == letter:
                    self.letters_of_word[index] = char

        elif letter not in self.selected_word:
            button.configure(state="disabled", bg="red2", fg="black") # Disable and Color Red Button
            self.number_of_incorrect_guesses += 1 # Add Incorrect Guess (if incorrect)
            self.guesses_left_tk.set(config.TOTAL_GUESSES_ALLOWED - self.number_of_incorrect_guesses) # Update Guesses Left Value
        
        self.update_word_label() # Update Word Label

        if self.check_win(): # If lost
            self.disable_all_buttons() # Disable Letters
            tk.Label(self, text="You Lost! Please wait...", font=self.sys20bu, bg="red2", width=100).pack()
            self.finish(0) # Wrap Up (Loss)

        if self.check_lost(): # If won
            self.disable_all_buttons() # Disable Letters
            tk.Label(self, text="You Won! Please wait...", font=self.sys20bu, bg="lime green", width=100).pack()
            self.finish(1) # Wrap Up (Win)

    def finish(self, state): # Win/Loss Result/Outcome
        gamesPlayed_file = open("./Other/Data/gamesplayed.txt", "r+")
        currentStreak_file = open("./Other/Data/currentstreak.txt", "r+")
        highestStreak_file = open("./Other/Data/higheststreak.txt", "r+")

        previous_gamesplayed = int(gamesPlayed_file.read()) # Previous GamesPlayed
        previous_currentstreak = int(currentStreak_file.read()) # Previous CurrentStreak
        previous_higheststreak = int(highestStreak_file.read()) # Previous HighestStreak

        gamesPlayed_file.seek(0)
        currentStreak_file.seek(0)
        highestStreak_file.seek(0)

        self.new_gamesplayed = previous_gamesplayed + 1 # New GamesPlayed Value

        if state == 1: # If win
            self.new_currentstreak = previous_currentstreak + 1 # New CurrentStreak Value

            if previous_higheststreak < self.new_currentstreak: # If new highest streak...
                self.new_higheststreak = self.new_currentstreak # New HighestStreak Value
                self.newhighstreak = 1 # New High Streak (Yes)
            else:
                self.new_higheststreak = previous_higheststreak # New HighestStreak Value
                self.newhighstreak = 0 # New High Streak (No)

        elif state == 0: # If lost
            self.new_currentstreak = 0 # New CurrentStreak Value
            self.new_higheststreak = previous_higheststreak # New HighestStreak Value
            self.newhighstreak = 0 # New High Streak (No)

        gamesPlayed_file.write(str(self.new_gamesplayed)) # Set new GamesPlayed
        currentStreak_file.write(str(self.new_currentstreak)) # Set new CurrentStreak
        highestStreak_file.write(str(self.new_higheststreak)) # Set new HighestStreak

        gamesPlayed_file.close() # Close File
        currentStreak_file.close() # Close File
        highestStreak_file.close() # Close File

        self.after(3000, self.to_endmessage, state) # Wait 3 seconds...

    def to_endmessage(self, state):
        self.destroy() # Destroy Window
        endmessage = EndMessage(state=state,
                                word=self.selected_word, 
                                newhighstreak=self.newhighstreak) # End Message Window
        endmessage.mainloop() # End Message Loop

    def disable_all_buttons(self):
        for button in self.letter_buttons.values(): # For each button
            button.config(state="disabled") # Disable Button
        self.back_button.configure(state="disabled") # Disable Back Button

    def check_lost(self): # Check If Lost
        return not None in self.letters_of_word

    def check_win(self): # Check If Won
        return self.number_of_incorrect_guesses >= config.TOTAL_GUESSES_ALLOWED

    def update_word_label(self): # Update Word Label (tk)
        self.word_label_tk.set("     ".join(letter if letter is not None else config.BLANK
                                            for letter in self.letters_of_word))

class MainMenu(Application): # Main Menu
    def __init__(self):
        super().__init__() # Superclass (Application)

        # Data Setup
        gamesPlayed_file = open("./Other/Data/gamesplayed.txt", "r")
        currentStreak_file = open("./Other/Data/currentstreak.txt", "r")
        highestStreak_file = open("./Other/Data/higheststreak.txt", "r")

        self.gamesplayed = gamesPlayed_file.read() # GamesPlayed Value
        self.currentstreak = currentStreak_file.read() # CurrentStreak Value
        self.higheststreak = highestStreak_file.read() # HighestStreak Value

        gamesPlayed_file.close()
        currentStreak_file.close()
        highestStreak_file.close()

        # Difficulty Setup
        self.selected_difficulty_tk = tk.StringVar() # Difficulty Variable (Tk)
        self.selected_difficulty_tk.set("Normal (1000 Words)") # Default Option (Normal)

        # Window Contents
        tk.Button(self, text="Play", command=self.play, bg="gray50", width=25, font=self.hel15b).place(x=250, y=50, anchor="center") # Play (Button)

        tk.Label(self, text="Difficulty:", font=self.bold).place(x=100, y=100, anchor="w")
        tk.OptionMenu(self, self.selected_difficulty_tk, *DIFFICULTIES.keys()).place(x=400, y=100, anchor="e") # Difficulty Option Menu

        tk.Label(self, text="Games Played:", font=self.bold).place(x=200, y=150, anchor="center") # Games Played (Label)
        tk.Label(self, text=self.gamesplayed, font=self.bu).place(x=325, y=150, anchor="center") # Games Played Number (Label)

        tk.Label(self, text="Current Streak:", font=self.bold).place(x=200, y=175, anchor="center") # Current Streak (Label)
        tk.Label(self, text=self.currentstreak, font=self.bu).place(x=325, y=175, anchor="center") # Current Streak Number (Label)

        tk.Label(self, text="Highest Streak:", font=self.bold).place(x=200, y=200, anchor="center") # Highest Streak (Label)
        tk.Label(self, text=self.higheststreak, font=self.bu).place(x=325, y=200, anchor="center") # Highest Streak Number (Label)

    def play(self):
        self.destroy() # Destroy Window

        difficulty_choice = DIFFICULTIES[self.selected_difficulty_tk.get()]

        game = Game(difficulty=difficulty_choice) # Game Window (init)
        game.mainloop() # Window Loop

    
def setup(): # Main Menu Setup
    main = MainMenu() # Main Menu Window (init)
    main.mainloop() # Window Loop


if __name__ == "__main__": # If Program is run directly...
    setup() # App Setup

"""
MIT License

Copyright (c) 2020 Kevin Apetrei

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
