# Parse file content

engine = open("AdventOfCode/2023/examples/day3.in").read().split("\n")

# Part 1

parts = []
all_parts = []

def check(i, j1, j2):
    if j1 > 0:
        if i > 0:
            if engine[i-1][j1-1] != '.':
                return True
        if engine[i][j1-1] != '.':
            return True
        if i < len(engine) - 1:
            if engine[i+1][j1-1] != '.':
                return True
    if j2 < len(engine[0]) - 1:
        if i > 0:
            if engine[i-1][j2+1] != '.':
                return True
        if engine[i][j2+1] != '.':
            return True
        if i < len(engine) - 1:
            if engine[i+1][j2+1] != '.':
                return True
    if i > 0:
        for j in range(j2-j1+1):
            if engine[i-1][j1+j] != '.':
                return True
    if i < len(engine) - 1:
        for j in range(j2-j1+1):
            if engine[i+1][j1+j] != '.':
                return True


def save(num, i, j):
    global parts, all_parts
    if check(i, j, j+len(num)-1):
        parts.append(int(num))
        all_parts.append((int(num),i,j,j+len(num)-1))

num = ''

for i, line in enumerate(engine):
    if num:
        save(num, i-1, len(engine[i-1]) - len(num))
        num = ''
    for j in range(len(line)):
        if line[j].isdigit():
            num += line[j]
        else:
            if num:
                save(num, i, j - len(num))
                num = ''

print("Part 1: ", sum(parts))

# Part 2

gears = []

def find_part(i, j):
    for (part, i1, j1, j2) in all_parts:
        if i == i1 and j >= j1 and j <= j2:
            return part
        
def search(i, j):
    global gears
    found = set()
    if j > 0:
        if i > 0:
            if engine[i-1][j-1].isdigit():
                found.add(find_part(i-1, j-1))
        if engine[i][j-1].isdigit():
            found.add(find_part(i, j-1))
        if i < len(engine) - 1:
            if engine[i+1][j-1].isdigit():
                found.add(find_part(i+1, j-1))
    if j < len(engine[0]) - 1:
        if i > 0:
            if engine[i-1][j+1].isdigit():
                found.add(find_part(i-1, j+1))
        if engine[i][j+1].isdigit():
            found.add(find_part(i, j+1))
        if i < len(engine) - 1:
            if engine[i+1][j+1].isdigit():
                found.add(find_part(i+1, j+1))
    if i > 0:
        if engine[i-1][j].isdigit():
            found.add(find_part(i-1, j))
    if i < len(engine) - 1:
        if engine[i+1][j].isdigit():
            found.add(find_part(i+1, j))
    
    if len(found) == 2:
        x, y = found
        gears.append(x*y)


for i, line in enumerate(engine):
    for j, char in enumerate(line):
        if char == "*":
            search(i, j)

print("Part 2: ", sum(gears))