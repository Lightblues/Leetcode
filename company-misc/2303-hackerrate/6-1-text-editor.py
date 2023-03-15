""" Simple Text Editor

append(W) - Append string W to the end of S.
delete(k) - Delete the last k characters of S.
print(k) - Print the k character of S.
undo() - Undo the last (not previously undone) operation of type 1 or 2, reverting S to the state it was in prior to that operation.
"""

# Enter your code here. Read input from STDIN. Print output to STDOUT
n = int(input())
hist = []
s = ""
for i in range(n):
    line = input().strip()
    if ' ' in line:
        cmd, arg = line.split()
    else:
        cmd = line
    cmd = int(cmd)
    if cmd==1:
        s += arg
        hist.append(len(arg))
    elif cmd==2:
        arg = int(arg)
        hist.append(s[-arg:])
        s = s[:-arg]
    elif cmd==3:
        print(s[int(arg)-1])
    elif cmd==4:
        lst = hist.pop()
        if type(lst)==int:
            s = s[:-lst]
        else:
            s += lst
    