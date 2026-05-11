import random

# Rock Paper Scissors Game against Computer
#Input from the user
def get_user_choice():
    user_input = input("Enter your choice (rock, paper, scissors): ").lower()# Convert to lowercase to handle case sensitivity
    while user_input not in ['rock', 'paper', 'scissors']:
        print("Invalid choice. Please try again.")# Prompt the user again if the input is invalid
        user_input = input("Enter your choice (rock, paper, scissors): ").lower()
    return user_input

# Computer's choice using random module
def get_computer_choice():
    return random.choice(['rock', 'paper', 'scissors'])

# Determine the winner based on the rules of the game
def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        return "You win!"
    else:
        return "Computer wins!"
    
# Main function to play the game
def play_game():
    user_choice = get_user_choice()
    computer_choice = get_computer_choice()
    print(f"You chose: {user_choice}")
    print(f"Computer chose: {computer_choice}")
    result = determine_winner(user_choice, computer_choice)
    print(result)               
 
# Run the game   
if __name__ == "__main__":
    play_game()   
    
#Quit or play again
    while True:
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again == 'yes':
            play_game()
        elif play_again == 'no':
            print("Thanks for playing! Goodbye!")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")  
    
    
    
    