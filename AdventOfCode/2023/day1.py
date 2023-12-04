import re

# Part 1

digits = [re.sub(r'[\D]+', '', l) for l in open("AdventOfCode/2023/examples/day1-1.in")]
calibration = [int(d[0] + d[-1]) for d in digits]

print('Part 1:', sum(calibration))


# Part 2

all_digits = [['one', 1], ['two', 2], ['three', 3], ['four', 4], ['five', 5], ['six', 6], ['seven', 7], ['eight', 8], ['nine', 9]]

calibration = []

with open("AdventOfCode/2023/examples/day1-2.in") as file:
    for l in file:
        str_digits = []

        i = 0
        while i < len(l):
            if l[i].isdigit():
                str_digits.append(int(l[i]))
            else:
                for spelled_digit, digit in all_digits:
                    if l[i:].startswith(spelled_digit):
                        str_digits.append(digit)
                        # We actually should search for the last occurrence of a digit, not replace as we go
                        # So, "threeight" is not interpreted as "3ight" but as "38"!
                        # Commenting next line will do the trick, for lack of more time to solve the puzzle :)
                        # i += len(spelled_digit) - 1
            i += 1

        calibration.append(int(str(str_digits[0]) + str(str_digits[-1])))

print('Part 2:', sum(calibration))
