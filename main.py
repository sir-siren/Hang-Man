"""Main entry point for the Hangman game.

This module contains the game logic encapsulated in the HangmanGame class,
demonstrating modern Python practices including type hinting, docstrings,
and decorators.
"""

import random
from typing import Callable, List
from hangman_words import words_and_hints
from hangman_art import LOGO, STAGES


def validate_guess(func: Callable) -> Callable:
    """Decorator to validate user input for the guess method.

    Ensures that the input is a single alphabetical character.
    If invalid, prints a message and returns None without executing the
    wrapped method's logic (or handles it gracefully within the loop scope).
    """

    def wrapper(self, *args, **kwargs):
        guess = args[0] if args else kwargs.get("guess")
        if not guess or len(guess) != 1 or not guess.isalpha():
            print(f"Invalid input: '{guess}'. Please enter a single letter.")
            return
        return func(self, *args, **kwargs)

    return wrapper


class HangmanGame:
    """Class representing the Hangman game state and logic."""

    def __init__(self) -> None:
        """Initialize the game with a random word and default state."""
        self.word_entry = random.choice(words_and_hints)
        self.word: str = self.word_entry["word"]
        self.hint: str = self.word_entry["hint"]
        self.word_length: int = len(self.word)
        self.end_of_game: bool = False
        self.lives: int = 6
        self.display: List[str] = ["_"] * self.word_length
        self.guessed_letters: List[str] = []

    def start(self) -> None:
        """Start the main game loop."""
        print(LOGO)
        print(f"Hint: {self.hint}\n")

        while not self.end_of_game:
            user_input = input("Guess a letter: ").lower()
            self.process_guess(user_input)

    @validate_guess
    def process_guess(self, guess: str) -> None:
        """Process a single letter guess.

        Args:
            guess: The letter guessed by the user.
        """
        if guess in self.guessed_letters:
            print(f"You've already guessed {guess}")
            return

        self.guessed_letters.append(guess)
        if guess in self.word:
            for position in range(self.word_length):
                letter = self.word[position]
                if letter == guess:
                    self.display[position] = letter
            print(f"Good guess: {guess}")
        else:
            print(f"You guessed {guess}, that's not in the word. You lose a life.")
            self.lives -= 1
            if self.lives == 0:
                self.end_of_game = True
                print(f"You lose, The Answer is {self.word}.")

        print(f"{' '.join(self.display)}")
        if "_" not in self.display:
            self.end_of_game = True
            print("You win.")

        print(STAGES[self.lives])


if __name__ == "__main__":
    game = HangmanGame()
    game.start()
