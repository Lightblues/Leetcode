""" 
统计数字中「圆圈」的数量
"""

ones = '069'
twos = '8'

s = input().strip()
ans = 0
for c in s:
    if c in ones:
        ans += 1
    elif c in twos: ans += 2
print(ans)
