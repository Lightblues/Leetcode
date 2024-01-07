""" 
对于arr, 判断是否存在下标 i,j, 满足 abs(i-j) <= k, abs(a[i]-a[j]) <= t
思路1: 对于k范围内的数字, 维护最大最小值 (使用堆)
"""
import heapq

# nums, k, t = input().strip().rsplit(',', 2)
# nums = eval(nums.split('=')[1].strip())
# k = int(k.split('=')[1])
# t = int(t.split('=')[1])

def parse_input():
    _, nums, k, t = input().strip().split('=')
    idx = nums.find(']')
    nums = eval(nums[:idx+1])
    k = int(k.split(',')[0])
    t = int(t.split(',')[0])
    return nums, k, t
nums, k, t = parse_input()
# if len(nums) <= 1:
#     print('false')
#     exit

def check_1(nums, k, t):
    mxq = [(-nums[0],0)]
    mnq = [(nums[0],0)]
    for j in range(1, len(nums)):
        x = nums[j]
        while mxq and mxq[0][1] < j-k:
            heapq.heappop(mxq)
        mx,i = mxq[0]
        if abs(-mx-x) <= t:
            return 'true'
        while mnq and mnq[0][1] < j-k:
            heapq.heappop(mnq)
        mn,i = mnq[0]
        if abs(mn-x) <= t:
            return 'true'
        heapq.heappush(mxq, (-x,j))
        heapq.heappush(mnq, (x,j))
    return 'false'
print(check_1(nums, k, t))

