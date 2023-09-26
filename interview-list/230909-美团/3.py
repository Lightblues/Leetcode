""" 
对于一个递增数组, 计算每个元素的差值, 这些差值的不同数量定义为「差异值」, 对于n个数字, 最大限制为m, 求最大的「差异值」
限制: n,m 1e5
"""
n,m = map(int, input().split())
def check(k):
    diff = (1+k)*k//2
    return m >= diff + n - k
l,r = 0,n-1
mx = 0
while l<=r:
    mid = (l+r)//2
    if check(mid):
        mx = mid
        l = mid+1
    else:
        r = mid-1
acc = 1
ans = [1]
for i in range(mx):
    acc += i+1
    ans.append(acc)
for i in range(n-mx-1):
    acc += 1
    ans.append(acc)
print(*ans)
