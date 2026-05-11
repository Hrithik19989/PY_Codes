# Input from the user
num = int(input("Enter a number: "))

# Function to check if a number is prime
def is_prime(number):
    if number <= 1:  # Numbers less than or equal to 1 are not prime
        return False
    for i in range(2, int(number ** 0.5) + 1):  # Check divisibility from 2 to sqrt(number)
        if number % i == 0:  # If number is divisible by any number, it's not prime
            return False
    return True  # If no divisors were found, the number is prime



# Check if the number is prime and print the result
if is_prime(num):
    print(f"{num} is a prime number.")
else:
    print(f"{num} is not a prime number.")
    