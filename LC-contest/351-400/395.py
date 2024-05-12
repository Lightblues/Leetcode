from easonsi.util.leetcode import *

def testClass(inputs):
    # 用于测试 LeetCode 的类输入
    s_res = [None] # 第一个初始化类, 一般没有返回
    methods, args = [eval(l) for l in inputs.split('\n')]
    class_name = eval(methods[0])(*args[0])
    for method_name, arg in list(zip(methods, args))[1:]:
        r = (getattr(class_name, method_name)(*arg))
        s_res.append(r)
    return s_res

""" 
https://leetcode.cn/contest/weekly-contest-395
https://leetcode.cn/circle/discuss/WH8n8y/

T3 的位运算有点意思
T4 的二分+滑窗有点难搞. 
Easonsi @2023 """
class Solution:
    """ 3131. 找出与数组相加的整数 I """
    def addedInteger(self, nums1: List[int], nums2: List[int]) -> int:
        return min(nums2) - min(nums1)
    
    """ 3132. 找出与数组相加的整数 II #medium len(nums1) == len(nums2)+2 问从前者丢掉两个数, 要求 nums1 的数字 +x 能够构成 nums2. 有多个可能的话返回最小的 """
    def minimumAddedInteger(self, nums1: List[int], nums2: List[int]) -> int:
        nums1.sort()
        nums2.sort()
        n = len(nums2); nn = len(nums1)
        def check(i):
            target = nums2[0] - nums1[i]
            acc = 0
            j = 0
            for i in range(i, nn):
                if nums2[j] - nums1[i] == target:
                    acc += 1
                    j += 1
                if j >= n: break
            return True if acc>=n else False
        for i in range(2,-1,-1):
            if check(i):
                return nums2[0] - nums1[i]
    
    """ 3133. 数组最后一个元素的最小值 #medium #题型 要求构造一个严格递增的长n的数组, 元素AND的结果为x. 求这些数组中, 最后一个元素的最小值
思路1: #贪心 #位运算
    注意到, 就是将 bin(n-1) 插入到 bin(x) 的空位中
[ling](https://leetcode.cn/problems/minimum-array-end/solutions/2759113/wei-yun-suan-jian-ji-xie-fa-pythonjavacg-nw8t/)
    """
    def minEnd(self, n: int, x: int) -> int:
        # num_zero = x.bit_length() - x.bit_count()
        target = bin(n-1)[2:]
        i = len(target) - 1
        ans = []
        for ch in bin(x)[2:][::-1]:
            if ch=='1': ans.append(ch)
            else:
                if i < 0: ans.append('0')
                else: 
                    ans.append(target[i])
                    i -= 1
        ans += target[:i+1][::-1]
        return int(''.join(ans[::-1]), 2)
    
    """ 3134. 找出唯一性数组的中位数 #hard #题型 对于所有子数组, 计算其中包含的不同数字个数 x. 对于这些 x 排序, 求其中位数 TT
限制: n 1e5
思路1: #二分
    所有的子数组数量为 n*(n+1)/2, 可以知道中位数的序号为o. 问题变为, 「找到xx, 是的子数组中不同数字 <=TT 的有xx个」—— 可以用二分来做
    如何检查a是否满足条件? #滑动窗口
原本的滑窗写得太难看了, 参见 [ling](https://leetcode.cn/problems/find-the-median-of-the-uniqueness-array/solutions/2759114/er-fen-da-an-hua-dong-chuang-kou-pythonj-ykg9/)
    """
    def medianOfUniquenessArray(self, nums: List[int]) -> int:
        n = len(nums)
        # target = ((n*(n+1))//2 - 1) // 2      # NOTE: 注意这样是 index, 下面进行比较的是从1开始的
        target = ((n*(n+1))//2 + 1) // 2
        def check(a):
            # 计算 #distinct 元素 <=a 的子数组数量
            # 答案是第一个满足 acc >=target 的 a
            acc = 0
            cnt = Counter()
            # NOTE: 这里遍历右边界方便多了!!!
            # j = 0
            # for i,x in enumerate(nums):
            #     cnt[x] += 1
            #     if i>0:
            #         cnt[nums[i-1]] -= 1
            #         if cnt[nums[i-1]] == 0: del cnt[nums[i-1]]
            #     j = max(j, i)       # 保证 j>=i? 但好像有 ERROR
            #     while j<n-1 and (len(cnt)<a or nums[j+1] in cnt):
            #         j += 1
            #         cnt[nums[j]] += 1
            #     acc += j-i+1
            r = 0
            for l,x in enumerate(nums):
                cnt[x] += 1
                while r<=l and len(cnt) > a:
                    cnt[nums[r]] -= 1
                    if cnt[nums[r]] == 0: del cnt[nums[r]]
                    r += 1
                acc += l-r+1
            return acc >= target
        l,r = 1, n
        ans = -1
        while l<=r:
            mid = (l+r)//2
            if check(mid):
                ans = mid
                r = mid - 1
            else:
                l = mid + 1
        return ans
        

sol = Solution()
result = [
    # sol.minimumAddedInteger(nums1 = [4,20,16,12,8], nums2 = [14,18,10]),
    # sol.minEnd(n = 3, x = 4),
    # sol.minEnd(2,7),
    sol.medianOfUniquenessArray(nums = [1,2,3]),
    sol.medianOfUniquenessArray(nums = [3,4,3,4,5]),
    sol.medianOfUniquenessArray([4,3,5,4]),
    sol.medianOfUniquenessArray([85,4,85,4]),
    sol.medianOfUniquenessArray([86,35,33,100,64]),
]
for r in result:
    print(r)
