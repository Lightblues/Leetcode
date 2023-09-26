""" 
贪心得到 1,2,3... 序列需要删除多少元素
"""
n = int(input())
arr = list(map(int, input().split()))
acc = 1
ans = 0
for x in arr:
    if x==acc:
        acc += 1
    else:
        ans += 1
if acc==1:
    print(-1)
else: print(ans)
