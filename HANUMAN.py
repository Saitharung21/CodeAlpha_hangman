import random

def hangman():
    # Predefined list of 5 words
    words = ['python', 'javascript', 'programming', 'developer', 'computer']
    
    # Select a random word
    selected_word = random.choice(words)
    word_length = len(selected_word)
    
    # Game variables
    max_attempts = 6
    attempts_left = max_attempts
    guessed_letters = []
    correct_guesses = ['_'] * word_length
    game_over = False
    
    print("🎯 Welcome to Hangman!")
    print(f"Guess the word! It has {word_length} letters.")
    print(" ".join(correct_guesses))
    print(f"You have {attempts_left} incorrect guesses allowed.\n")
    
    while not game_over and attempts_left > 0:
        # Get player input
        guess = input("Enter a letter: ").lower()
        
        # Validate input
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single letter (A-Z).")
            continue
        
        if guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try a different letter.")
            continue
        
        # Add to guessed letters
        guessed_letters.append(guess)
        
        # Check if guess is correct
        if guess in selected_word:
            print(f"Good guess! '{guess}' is in the word.")
            
            # Update correct guesses
            for i in range(word_length):
                if selected_word[i] == guess:
                    correct_guesses[i] = guess
        else:
            attempts_left -= 1
            print(f"Sorry, '{guess}' is not in the word.")
            print(f"Attempts left: {attempts_left}")
        
        # Display current progress
        print("\nWord: " + " ".join(correct_guesses))
        print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")
        
        # Draw hangman (simple ASCII art)
        draw_hangman(max_attempts - attempts_left)
        print()
        
        # Check if player won
        if '_' not in correct_guesses:
            game_over = True
            print(f"🎉 Congratulations! You guessed the word: {selected_word.upper()}")
            break
    
    # Check if player lost
    if attempts_left == 0:
        print(f"💀 Game over! The word was: {selected_word.upper()}")
        draw_hangman(max_attempts)  # Show full hangman

def draw_hangman(wrong_attempts):
    """Draw simple ASCII hangman based on wrong attempts"""
    stages = [
        """
           -----
           |   |
               |
               |
               |
               |
        -----------
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        -----------
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        -----------
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        -----------
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        -----------
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        -----------
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        -----------
        """
    ]
    
    if wrong_attempts < len(stages):
        print(stages[wrong_attempts])
    else:
        print(stages[-1])

def main():
    while True:
        hangman()
        
        # Ask if player wants to play again
        play_again = input("\nWould you like to play again? (y/n): ").lower()
        if play_again != 'y':
            print("Thanks for playing! Goodbye!")
            break
        print("\n" + "="*40 + "\n")

if __name__ == "__main__":
    main()