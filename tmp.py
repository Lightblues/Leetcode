from easonsi import utils
from easonsi.util.leetcode import *


def threeSum(nums, target):
    nums.sort()
    # ans = []
    ans = 0
    n = len(nums)
    for i in range(n):
        if i>0 and nums[i]==nums[i-1]: continue # 避免重复
        a = nums[i]
        l,r = i+1,n-1
        while l<r:
            s = nums[l]+nums[r]
            if s == target-a:
                # ans.append([a,nums[l],nums[r]])
                ans += 1
                l+=1
                # 避免重复
                while l<r and nums[l]==nums[l-1]: l+=1
            elif s < target-a: l+=1
            else: r-=1
    return ans

print(
    threeSum([1,2,3,4,5], 6),
    threeSum([1,4,3,2,6,5], 9), # 3
)

# %%
import numpy as np
a = np.array([2,1,3,5,6])
np.log(a) / np.log(2)
# %%
from collections import Counter
c = Counter([1,2,2,3,3,5,4])
sorted(c.items())
# %%
