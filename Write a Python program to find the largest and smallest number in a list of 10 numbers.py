my_list = [3, 5, 1, 9, 2, 8, 4, 7, 6, 0]
largest = my_list[0]
smallest = my_list[0]
for number in my_list:
    if number > largest:
        largest = number
    if number < smallest:
        smallest = number
print("Largest number:", largest)
print("Smallest number:", smallest)
