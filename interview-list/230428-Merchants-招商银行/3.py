""" 
对于一个数字, 统计满足条件的数组: h!=t, 同时 (h..t) 之间的元素都不等于h/t
限制: N 2e5; 数组的元素范围 N

7
1 2 3 4 3 2 5
# 13
# 注意区间 (1,7) 也满足!
4
1 2 1 2
# 3

思路0: 不会做, 下面写了个 O(n^2) 的实现. 

"""
n = int(input())
arr = list(map(int, input().split()))
ans = 0
for i,x in enumerate(arr):
    s = set()
    for j in range(i+1,n):
        y = arr[j]
        if y==x: break
        if y in s: continue
        s.add(y)
        ans += 1
print(ans)

