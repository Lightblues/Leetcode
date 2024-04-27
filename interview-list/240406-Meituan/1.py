s = input().strip()
t = 'meituan'
ans = 0
for c1,c2 in zip(s,t):
    ans += c1 != c2
print(ans)