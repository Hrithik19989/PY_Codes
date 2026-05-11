import random

def get_computer_choice():
    """Generate random choice for computer"""
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def get_user_choice():
    """Get and validate user input"""
    while True:
        user_input = input("Enter your choice (rock/paper/scissors) or 'quit' to exit: ").lower().strip()
        
        # Check if user wants to quit
        if user_input == 'quit':
            return 'quit'
        
        # Validate input
        if user_input in ['rock', 'paper', 'scissors']:
            return user_input
        else:
            print("Invalid choice! Please enter 'rock', 'paper', or 'scissors'.")

def determine_winner(user_choice, computer_choice):
    """Determine the winner using conditional logic"""
    if user_choice == computer_choice:
        return "tie"
    
    # User wins conditions
    if (user_choice == 'rock' and computer_choice == 'scissors') or \
       (user_choice == 'paper' and computer_choice == 'rock') or \
       (user_choice == 'scissors' and computer_choice == 'paper'):
        return "user"
    else:
        return "computer"

def display_result(user_choice, computer_choice, winner):
    """Display the round result"""
    print(f"\nYou chose: {user_choice}")
    print(f"Computer chose: {computer_choice}")
    
    if winner == "tie":
        print("It's a tie!")
    elif winner == "user":
        print("You win this round!")
    else:
        print("Computer wins this round!")

def play_game():
    """Main game loop with flow control"""
    print("=== Welcome to Rock Paper Scissors! ===")
    print("Instructions: Rock beats Scissors, Scissors beats Paper, Paper beats Rock")
    print("Type 'quit' anytime to exit the game.\n")
    
    # Score tracking
    user_score = 0
    computer_score = 0
    rounds_played = 0
    
    # Main game loop
    while True:
        print(f"\n--- Round {rounds_played + 1} ---")
        print(f"Score - You: {user_score}, Computer: {computer_score}")
        
        # Get user choice
        user_choice = get_user_choice()
        
        # Check if user wants to quit
        if user_choice == 'quit':
            break
        
        # Get computer choice
        computer_choice = get_computer_choice()
        
        # Determine winner
        winner = determine_winner(user_choice, computer_choice)
        
        # Display result
        display_result(user_choice, computer_choice, winner)
        
        # Update scores using conditional statements
        if winner == "user":
            user_score += 1
        elif winner == "computer":
            computer_score += 1
        # No score change for tie
        
        rounds_played += 1
        
        # Ask if user wants to continue (optional)
        while True:
            continue_game = input("\nDo you want to play another round? (y/n): ").lower().strip()
            if continue_game in ['y', 'yes']:
                break
            elif continue_game in ['n', 'no']:
                user_choice = 'quit'  # Set to quit to exit main loop
                break
            else:
                print("Please enter 'y' for yes or 'n' for no.")
        
        # Break if user chose not to continue
        if user_choice == 'quit':
            break
    
    # Final results
    print("\n=== Game Over ===")
    print(f"Final Score - You: {user_score}, Computer: {computer_score}")
    print(f"Total rounds played: {rounds_played}")
    
    # Determine overall winner using nested conditionals
    if user_score > computer_score:
        print("🎉 Congratulations! You won overall!")
    elif computer_score > user_score:
        print("😔 Computer wins overall! Better luck next time!")
    else:
        if rounds_played > 0:
            print("🤝 It's an overall tie! Great game!")
        else:
            print("No rounds played. Thanks for trying!")
    
    print("Thanks for playing Rock Paper Scissors!")

# Run the game
if __name__ == "__main__":
    play_game()