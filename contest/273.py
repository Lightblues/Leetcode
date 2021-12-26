from typing import List
import collections

class Solution273:
    def isSameAfterReversals(self, num: int) -> bool:
        if str(int(str(num)[::-1]))[::-1] == str(num):
            return True
        return False


    def executeInstructions(self, n: int, startPos: List[int], s: str) -> List[int]:
        order2dir = {
            'L': (0, -1),
            "R": (0, 1),
            'U': (-1, 0),
            'D': (1, 0),
        }
        def isValid(x,y):
            return x>=0 and x<n and y>=0 and y<n
        result = []
        for i in range(len(s)):
            orders = s[i:]
            count = 0
            x,y = startPos
            for order in orders:
                dx,dy = order2dir[order]
                x,y = x+dx, y+dy
                if isValid(x,y):
                    count += 1
                else:
                    break
            result.append(count)
        return result

    """ 5965. 相同元素的间隔之和
n == arr.length
1 <= n <= 10**5
1 <= arr[i] <= 10**5

输入：arr = [2,1,3,1,2,3,3]
输出：[4,2,7,2,4,4,5]
解释：
- 下标 0 ：另一个 2 在下标 4 ，|0 - 4| = 4
- 下标 1 ：另一个 1 在下标 3 ，|1 - 3| = 2
- 下标 2 ：另两个 3 在下标 5 和 6 ，|2 - 5| + |2 - 6| = 7
- 下标 3 ：另一个 1 在下标 1 ，|3 - 1| = 2
- 下标 4 ：另一个 2 在下标 0 ，|4 - 0| = 4
- 下标 5 ：另两个 3 在下标 2 和 6 ，|5 - 2| + |5 - 6| = 4
- 下标 6 ：另两个 3 在下标 2 和 5 ，|6 - 2| + |6 - 5| = 5

用一个 defaultdict(list) 记录各个元素出现的位置.
问题转化为对于一个数字出现的位置, 计算各个位置的 dist 和.
- 注意数据量, 直接暴力遍历复杂度为 O(n^2) 会超时
- 思路1: 观察相邻两个元素相差的(子距离数量), 可得递推公式 dp[i+1] = dp[i] -(n-2i-2) * (arr[i-1]-arr[i]) 
- 思路2: 计算 cumsum, 则 i 处的距离和为 (cumsum[-1]-cumsum[i] - arr[i]*(n-1-i)) + (cumsum[i]-cumsum[0] - arr[0]*i)
"""
    def getDistances(self, arr: List[int]) -> List[int]:
        indexRecord = collections.defaultdict(list)
        for i,num in enumerate(arr):
            indexRecord[num].append(i)
        # result = []
        # for i,num in enumerate(arr):
        #     l = indexRecord[num]
        #     ls = [abs(ii-i) for ii in l]
        #     result.append(sum(ls))
        # return result
        def getDist(arr):
            n = len(arr)
            res = []
            res.append(sum([num-arr[0] for num in arr]))
            for i in range(len(arr)-1):
                res.append(res[-1] - (n-2*i-2)*(arr[i+1]-arr[i]))
            return res
        result = [0] * len(arr)
        for indexs in indexRecord.values():
            dists = getDist(indexs)
            for i,d in zip(indexs,dists):
                result[i] = d
        return result
    
    """ 5966. 还原原数组
就是对于一个数组 arr, 用一个正整数 k, 分别生成两个数组, lower[i] = arr[i] - k, higher[i] = arr[i] + k
要求给定这两个数组的混合, 还原 arr

2 * n == nums.length
1 <= n <= 1000
1 <= nums[i] <= 109
生成的测试用例保证存在 至少一个 有效数组 arr

输入：nums = [2,10,6,4,8,12]
输出：[3,7,11]
解释：
如果 arr = [3,7,11] 且 k = 1 ，那么 lower = [2,6,10] 且 higher = [4,8,12] 。
组合 lower 和 higher 得到 [2,6,10,4,8,12] ，这是 nums 的一个排列。
另一个有效的数组是 arr = [5,7,9] 且 k = 3 。在这种情况下，lower = [2,4,6] 且 higher = [8,10,12] 。 

关键看约束条件, 数组大小最多为 1000 所以暴力搜索即可, 题目只是比较繁琐
- sort, 得到可能的 k
- 用 indexRecord 记录每个数字对应的位置
- 关键在判断一个 k 是否满足条件. 这里用了一个 used 记录每个所对应的元素所在位置, 遍历 nums 后, 若 sum(used) == n 则说明 k 满足条件
"""
    def recoverArray(self, nums: List[int]) -> List[int]:
        n = len(nums)/2
        nums = sorted(nums)
        possibleK2 = [num-nums[0] for num in nums[1:]]
        possibleK2 = [i for i in possibleK2 if i%2==0]      # 注意一定是偶数
        indexRecord = collections.defaultdict(list)
        for i,num in enumerate(nums):
            indexRecord[num].append(i)
        for k2 in possibleK2:
            used = [False] * len(nums)
            for i in range(len(nums)):
                if used[i]:
                    continue
                indexs = indexRecord[nums[i]+k2]
                put = False
                for i in indexs:
                    if not used[i]:
                        put = True
                        used[i] = True
                        break
                if not put:
                    break
            if sum(used) == n:
                return [num-k2//2 for i,num in enumerate(nums) if used[i]]
        
class Test273:
    def test3(self):
        def getDist(arr):
            n = len(arr)
            res = []
            res.append(sum([num-arr[0] for num in arr]))
            for i in range(len(arr)-1):
                res.append(res[-1] - (n-2*i-2)*(arr[i+1]-arr[i]))
            return res
        def getDist2(arr):
            cumsum = []
            s = 0
            for num in arr:
                s += num
                cumsum.append(s)
            result = []
            n = len(arr)
            for i in range(len(arr)):
                result.append(
                    cumsum[-1]-cumsum[i] - arr[i]*(n-1-i) + cumsum[i]-cumsum[0] - arr[0]*i
                )
            return result
        l = [1,3,4,6]
        result = []
        for num in l:
            ll = [abs(ii-num) for ii in l]
            result.append(sum(ll))
        print(result)
        print(getDist(l))
        print(getDist2(l))
# test = Test273()
# test.test3()

sol = Solution273()

print(
    # sol.executeInstructions(n = 3, startPos = [0,1], s = "RRDDLU"),
    # sol.getDistances(arr = [2,1,3,1,2,3,3]),
    sol.recoverArray([11,6,3,4,8,7,8,7,9,8,9,10,10,2,1,9]),
    sol.recoverArray(nums = [2,10,6,4,8,12]),
    sol.recoverArray(nums = [1,1,3,3]),
    sol.recoverArray(nums = [5,435])
)