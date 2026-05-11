length = float(input("Enter the length of the rectangle: "))
width = float(input("Enter the width of the rectangle: "))


def calculate_area(length, width):
    return length * width

print(f"Area of {length} x {width} rectangle: {calculate_area(length, width)}")