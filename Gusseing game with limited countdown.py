import random

def play_game():
    number = random.randint(1, 100)
    attempts = 10
    print("Welcome to the Guessing Game!")
    print("You have 10 attempts to guess the number between 1 and 100.")
    while attempts > 0:
        while True:
            try:
                guess = int(input("Enter your guess: "))
                break
            except ValueError:
                print("Invalid input! Please enter an integer.")
        if guess < number:
            print("Too low! Try again.")
            attempts -= 1
            print(f"You have {attempts} attempts left.")
        elif guess > number:
            print("Too high! Try again.")
            attempts -= 1
            print(f"You have {attempts} attempts left.")
        else:
            print("Congratulations! You've guessed the number!")
            return

    print(f"Game over! The number was {number}.")

while True:
    play_game()
    again = input("Do you want to play again? (yes/no): ").strip().lower()
    if again != "yes":
        print("Thanks for playing!")
        break