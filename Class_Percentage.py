student_name = input("Enter the student's name: ")

class1_student_names = ["Math", "Science", "English" , "History", "Geography"]
class1_marks = [85, 90, 78, 92, 88]

if student_name in class1_student_names:
    index = class1_student_names.index(student_name)
    print(f"{student_name}'s marks are:{class1_marks[index]}")