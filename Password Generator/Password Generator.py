import random 
import string
def generate_password(length):
    if length < 8 or length > 128:
        raise ValueError("Password length must be between 8 and 128 characters.")
        

    characters = string.ascii_letters + string.digits + string.punctuation
    required_characters = [
    random.choice(string.ascii_lowercase),
    random.choice(string.ascii_uppercase),
    random.choice(string.digits),
    random.choice(string.punctuation),
]
    remaining = random.choices(characters, k=length - 4)
    password = required_characters + remaining
    random.shuffle(password)
    generated_password = ''.join(password)
    return generated_password

if __name__ == "__main__":
    try:
        password_length = int(input("Enter the desired password length (minimum 8 characters and maximum 128 characters): "))
        generated_password = generate_password(password_length)
        print("Generated Password:", generated_password)
    except ValueError as e:      # catches known errors cleanly
        print("Error:", e)
    except Exception as e:        # catches unknown/unexpected errors
        print("Unexpected:", e)