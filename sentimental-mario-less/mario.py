from cs50 import get_int

# Prompt for height until a valid value (1–8)
while True:
    height = get_int("Height: ")
    if 1 <= height <= 8:
        break

for i in range(1, height + 1):
    print(" " * (height - i) + "#" * i)
