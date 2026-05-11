# 1. Start with an empty list
students = []

# 2. Decide how many students to add
num_students = int(input("Enter number of students: "))

for i in range(num_students):
    # 3. Get name and marks from the user
    name = input(f"Enter name of student {i+1}: ")
    marks = int(input(f"Enter marks for {name}: "))
    
    # 4. Create a small sub-list and add it to the main list
    students.append([name, marks])

# 5. See the final result
print(students)
