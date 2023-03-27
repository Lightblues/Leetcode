""" 子区间计数
问多少长度为k的子数组经过重排列可以是一个「顺子」, 限制: n,k 3e5
思路1: #滑动窗口
    用一个Counter记录当前区间内的数字计数; 若 mx-mn=k-1 并且Counter中元素数量为k则说明满足条件
    如何记录当前区间的mx,mn? 用一个带时间戳的最大最小堆, 在移动窗口过程中进行更新
 """
import heapq
import collections
n,k = map(int, input().split())
arr = list(map(int, input().split()))
cnt = collections.Counter()
# 两个堆
mx = []; mn = []
ans = 0
for i,x in enumerate(arr):
    cnt[x] += 1
    if i>=k:
        pp = arr[i-k]
        # 删除过期的元素
        cnt[pp] -= 1
        if cnt[pp]==0: del cnt[pp]
    heapq.heappush(mx, (-x,i))
    heapq.heappush(mn, (x,i))
    # 删除过期的元素
    while mx and mx[0][1]<=i-k: heapq.heappop(mx)
    while mn and mn[0][1]<=i-k: heapq.heappop(mn)
    if -mx[0][0]-mn[0][0]==k-1 and len(cnt)==k:
        ans += 1
print(ans)