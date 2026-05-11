def factorial(num):
    # Return the factorial of n
      for i in range(1, num):
        num = num * i
 
      return num
  

# Read input and print result
num = int(input())
print(str(num) + "! = " + str(factorial(num)))