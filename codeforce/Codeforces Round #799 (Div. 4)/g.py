""" 
G. 2^Sort
给定一个长n的数组, 统计其中满足条件的长k的连续子数组的数量. 条件为这个长k的子数组, 以 2^0,2^1,2^2... 为权是严格递增的.
思路1: #双指针
    在遍历right的过程中, 维护left是最左边的满足条件的位置. 事实上每次仅需要判断 right, right-1 相邻位置是否满足条件即可 (`nums[right]*2<=nums[right-1]`), 若不满足则重置 `left=right`.
"""

def f():
    n, k = map(int, input().split())
    nums = list(map(int, input().split()))
    left = 0; ans = 0
    for right,b in enumerate(nums):
        # 原本这样筛是为了防止数字过大, 但下面改了之后似乎不会出现了?
        left = max(left, right-k)
        # 不应该看左侧而应该看最右边, 错例: 5 3 2 1
        # while left<right and b * 2**(right-left) <= nums[left]:
        #     left += 1
        if right>0 and b*2<=nums[right-1]:
            left = right
        if right-left==k: ans += 1
    print(ans)
    
for _ in range(int(input())): f()
