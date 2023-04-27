
import sys 
s = sys.stdin.readline().strip()
n = len(s)
def f(s):
    for i in range(n-2):
        if s[i]<s[i+1]:
            return f"{s[:i]}{s[i+1]}{s[i]}{s[i+2:]}"
    for i in range(n-2):
        if s[i]==s[i+1]:
            return f"{s[:i]}{s[i+1]}{s[i]}{s[i+2:]}"
    return s[:-2]+s[-2:][::-1]
print(f(s))

