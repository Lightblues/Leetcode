import sys

try:
    while True:
        line = sys.stdin.readline().strip()
        if line == '':
            break
        lines = line.split()
        print(int(lines[0]) + int(lines[1]))
except:
    pass

