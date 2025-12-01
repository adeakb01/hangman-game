# app.py - FIXED VERSION
from flask import Flask, render_template, request, jsonify, session
import random
import string
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key

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
        self.guessed_letters = []
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
        
        self.guessed_letters.append(letter)
        
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
            "guessed_letters": sorted(self.guessed_letters),
            "incorrect_guesses": self.incorrect_guesses,
            "max_attempts": self.max_attempts,
            "game_over": self.game_over,
            "won": self.won,
            "secret_word": self.secret_word if self.game_over else None
        }
    
    def to_dict(self):
        """Convert game state to dictionary for session storage"""
        return {
            'secret_word': self.secret_word,
            'guessed_letters': self.guessed_letters,
            'incorrect_guesses': self.incorrect_guesses,
            'max_attempts': self.max_attempts,
            'game_over': self.game_over,
            'won': self.won
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create game instance from dictionary"""
        game = cls()
        game.secret_word = data['secret_word']
        game.guessed_letters = data['guessed_letters']
        game.incorrect_guesses = data['incorrect_guesses']
        game.max_attempts = data['max_attempts']
        game.game_over = data['game_over']
        game.won = data['won']
        return game

@app.route('/')
def index():
    # Initialize a new game if one doesn't exist
    if 'game_state' not in session:
        game = HangmanGame()
        session['game_state'] = game.to_dict()
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    game = HangmanGame()
    session['game_state'] = game.to_dict()
    return jsonify(game.get_game_state())

@app.route('/guess', methods=['POST'])
def guess():
    letter = request.json.get('letter', '')
    
    # Get game state from session
    game_data = session.get('game_state', {})
    if not game_data:
        game = HangmanGame()
    else:
        game = HangmanGame.from_dict(game_data)
    
    result = game.guess_letter(letter)
    
    # Save updated game state
    session['game_state'] = game.to_dict()
    
    return jsonify(result)

@app.route('/game_state', methods=['GET'])
def game_state():
    game_data = session.get('game_state', {})
    if game_data:
        game = HangmanGame.from_dict(game_data)
        return jsonify(game.get_game_state())
    else:
        return jsonify({"error": "No game in session"})

if __name__ == '__main__':
    app.run(debug=True)