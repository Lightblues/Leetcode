""" 
a -> bc
b -> ca
c -> ab
操作k次, 最后的结果
"""
s = input()
k = int(input())
for _ in range(k):
    r = ""
    for c in s:
        if c == 'a':
            r += 'bc'
        elif c == 'b':
            r += 'ca'
        else:
            r += 'ab'
    s = r
print(s)
