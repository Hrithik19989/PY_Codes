
import pandas as pd

df = pd.read_csv("countries.csv")
c = df['Country']

print("Welcome to the Country Guessing Game!")

print("RULES:\n1.Try to guess the name of a country. You will earn points for each correct guess.\n2.Type 'exit' to quit the game at any time.\n3.First letter of the country name should be capital and the rest should be in small letters.")
print("Let's start the game! Good luck!")
isguess_first = True

print(f"Your current score is: 0")

def play_game():
        global isguess_first
        score = 0
        guess = []
        while True:
                guess_value = input('Enter the name of a country or type exit to exit from the game: ')
                if guess_value in c.values:
                        if isguess_first:
                                print("You gained a point.")
                                current_score = score + 1
                                guess.append(guess_value)
                                print(guess)
                                score = current_score
                                print(f"Your current score is {score} .")
                                isguess_first = False
                        elif guess_value not in guess:
                                print("You gained a point.")
                                current_score = score + 1
                                guess.append(guess_value)
                                print(guess)
                                score = current_score
                                print(f"Your current score is {score} .")
                        else:
                                print("You have already guessed this country. Try a different one.")
                                current_score = score 
                                score = current_score
                                print(f"Your current score is {score} .")
                                
                elif guess_value.lower() == 'exit':
                        exit(score)
                        
                else:
                        try_again()
                        
                
def try_again():
        print('Do you want to try again? (y/n)')
        choice = input().lower()
        global score
        if choice == 'y':
                play_game()
        elif choice == 'n':
                print("Thanks for playing! See you next time.")
                print(f"Your final score is: {score} points.")
                quit()
        else:
                print("Invalid input. Please enter (y for yes/n for no)")
                try_again()
                

def exit(score):
        print('Are you sure you want to exit? (y for yes/n for no)')
        choice = input().lower()
        if choice == 'y':
                print("Thanks for playing! See you next time.")
                print(f"Your final score is: {score} points.")
                quit()
        elif choice == 'n':
                print("Great! Let's continue playing.")
                print(f"Your current score is: {score} points.")
                play_game()
        else:
                print("Invalid input. Please enter (y for yes/n for no)")
                

   
                
play_game()
                
