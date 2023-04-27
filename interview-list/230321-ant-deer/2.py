
""" 
对于一个序列, 计算 (i,j,k) 组, 满足 2j = i+k
限制: n 2e3
思路1: 两两匹配枚举
 """

from collections import Counter
n = int(input())
arr = list(map(int, input().split()))
cnt = Counter(arr)
ans = 0
# 枚举中间的那个均值
for i,c1 in cnt.items():
    # 枚举剩余的两个数字, 计数
    # i =  j=k
    if c1>=3: ans += c1*(c1-1)*(c1-2)
    # 不相等的情况
    for j,c2 in cnt.items():
        if i==j: continue
        ans += c1*c2*cnt[2*j-i]
print(ans)



