
import random

def toss_coin():
    result = random.choice(['Head', 'Tail'])
    return result

toss_result = toss_coin()
print(f"The result of the coin toss is: {toss_result}")
