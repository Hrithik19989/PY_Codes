my_class = {
    "Alice": 63,
    "Bob": 90,
    "Charlie": 81,
    "Diana": 72,
    "Eve": 81,
}
for student, marks in my_class.items():
    if marks > 75:
        print(student)