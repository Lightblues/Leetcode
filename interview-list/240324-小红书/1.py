""" 

"""
n = int(input())
s = set()
for _ in range(n):
    ii = input().strip()
    if ii not in s:
        print(ii)
        s.add(ii)

