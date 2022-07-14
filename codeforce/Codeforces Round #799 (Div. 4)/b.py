""" B. All Distinct """
def f():
    n = int(input())
    arr = map(int, input().split())
    s = set(); cnt = 0
    for a in arr:
        if a not in s: s.add(a)
        else: cnt += 1
    c = cnt if cnt%2==0 else cnt+1
    print(n-c)

n = int(input())
for _ in range(n):
    f()
    
