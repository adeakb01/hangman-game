# hangman.py
import random
import string

class HangmanGame:
    def __init__(self, word_list=None):
        if word_list is None:
            self.word_list = [
                "python", "javascript", "hangman", "challenge", "programming",
                "computer", "keyboard", "developer", "algorithm", "function"
            ]
        else:
            self.word_list = word_list
        
        self.reset_game()
    
    def reset_game(self):
        self.secret_word = random.choice(self.word_list).upper()
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.max_attempts = 6
        self.game_over = False
        self.won = False
    
    def guess_letter(self, letter):
        if self.game_over:
            return {"error": "Game is already over"}
        
        letter = letter.upper()
        
        # Validate input
        if len(letter) != 1 or letter not in string.ascii_uppercase:
            return {"error": "Please enter a single letter"}
        
        if letter in self.guessed_letters:
            return {"error": f"You've already guessed '{letter}'"}
        
        self.guessed_letters.add(letter)
        
        if letter in self.secret_word:
            # Check if player has won
            if all(char in self.guessed_letters for char in self.secret_word):
                self.game_over = True
                self.won = True
                return self.get_game_state()
        else:
            self.incorrect_guesses += 1
            if self.incorrect_guesses >= self.max_attempts:
                self.game_over = True
                return self.get_game_state()
        
        return self.get_game_state()
    
    def get_display_word(self):
        return " ".join([char if char in self.guessed_letters else "_" for char in self.secret_word])
    
    def get_game_state(self):
        return {
            "display_word": self.get_display_word(),
            "guessed_letters": sorted(list(self.guessed_letters)),
            "incorrect_guesses": self.incorrect_guesses,
            "max_attempts": self.max_attempts,
            "game_over": self.game_over,
            "won": self.won,
            "secret_word": self.secret_word if self.game_over else None
        }