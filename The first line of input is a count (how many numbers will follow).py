
n = int(input())
numbers = []
for i in range(n):
    number = int(input())
    numbers.append(number)
    
#The next lines each have one number 
print("The numbers you entered are:")
for number in numbers:  
    print(number)
    
#Add all the numbers together and print the sum:
total = sum(numbers)
print("The sum of the numbers you entered is:", total)

