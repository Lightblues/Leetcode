""" 子区间计数
问多少长度为k的子数组经过重排列可以是一个「顺子」, 限制: n,k 3e5
思路1: #滑动窗口
    用一个Counter记录当前区间内的数字计数; 若 mx-mn=k-1 并且Counter中元素数量为k则说明满足条件
    如何记录当前区间的mx,mn? 用一个带时间戳的最大最小堆, 在移动窗口过程中进行更新
 """
from heapq import heappush, heappop
from collections import Counter
n,k = map(int, input().split())
nums = list(map(int, input().split()))
counter = Counter()
# 两个堆
maxH = []; minH = []
ans = 0
for i,x in enumerate(nums):
    counter[x] += 1
    if i>=k:
        counter[nums[i-k]] -= 1
        if counter[nums[i-k]]==0: del counter[nums[i-k]]
    heappush(maxH, (-x,i))
    heappush(minH, (x,i))
    # 删除过期的元素
    while maxH[0][1]<=i-k: heappop(maxH)
    while minH[0][1]<=i-k: heappop(minH)
    diff = -maxH[0][0]-minH[0][0]+1
    if diff==k and len(counter)==k:
        ans += 1
print(ans)


