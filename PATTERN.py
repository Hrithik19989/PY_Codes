
size = 3
n = size - 1  # Maximum distance from center (2)

for x in range(-n, n + 1):
    row_chars = []
    for y in range(-n, n + 1):
        distance = abs(x) + abs(y)
        if distance > n:
            row_chars.append("-")
        else:
            row_chars.append(chr(97 + distance))
    print("-".join(row_chars))
