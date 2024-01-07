""" 10转为r进制数值 """
import string
i,r = map(int, input().split())
dmap = list(range(10)) + list(string.ascii_uppercase)
ans = []
while i:
    ans.append(dmap[i%r])
    i //= r
print(''.join(map(str, ans[::-1])))