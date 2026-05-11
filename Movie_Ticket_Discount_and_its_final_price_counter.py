
while True:
    movie_name = input("Enter the name of the movie: ")
    try:
        ticket_price = float(input("Enter the price of the ticket: "))
    except ValueError:
        print("Invalid ticket price. Please enter a valid number.")
        continue

    if movie_name == "Avengers: Endgame":
        discount = 0.20
    elif movie_name == "The Lion King":
        discount = 0.15
    else:
        print("Movie is not available. Please enter a valid movie name.")
        continue

    if discount > 0:
        print(f"You get a {discount*100}% discount on the ticket.")
        finalprice = ticket_price * (1 - discount)
        print(f"The final price of the ticket for {movie_name} is: {finalprice:.2f}")
        break