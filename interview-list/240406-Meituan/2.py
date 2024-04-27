""" 统计实数数量
4
-5 5-i 6+3i -4+0i
# 2

实数形式? 
    -4+0i
    0i
"""
def f0():
    x = x.lstrip('-')
    for c in '-+':
        if c in x:
            _,b = x.split(c)
            b = b.rstrip('i')
            # ans += b.strip()=='0'
            try:
                ans += (float(b)==0.0)
            except:
                continue
    if '-' not in x and '+' not in x:
        ans += 1

def f(x:str):
    x = x.lstrip('-')
    if '-' not in x and '+' not in x: 
        if 'i' in x: return x.strip('i') == '0'
        else: return 1
    else:
        ch = '-' if '-' in x else '+'
        _,b = x.split(ch)
        return b.rstrip('i') == '0'


n = int(input())
nums = input().strip().split()
ans = 0
for x in nums:
    ans += f(x)
print(ans)

