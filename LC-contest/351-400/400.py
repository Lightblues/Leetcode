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
https://leetcode.cn/contest/weekly-contest-400
https://leetcode.cn/circle/discuss/wIuw7p/
T4 位运算! 灵神的分析太精妙啦!

Easonsi @2023 """
class Solution:
    """ 3168. 候诊室中的最少椅子数 """
    def minimumChairs(self, s: str) -> int:
        cnt = 0; mx = 0
        for c in s:
            if c == "E":
                cnt += 1
                mx = max(mx, cnt)
            elif c == 'L':
                cnt -= 1
        return mx

    """ 3169. 无需开会的工作日 """
    def countDays(self, days: int, meetings: List[List[int]]) -> int:
        meetings.sort()
        cnt = 0
        n = len(meetings)
        st, en = meetings[0]
        for s,e in meetings[1:]:
            if s > en:
                cnt += en - st + 1
                st, en = s, e
            else:
                en = max(en, e)
        cnt += en - st + 1
        return days - cnt

    """ 3170. 删除星号以后字典序最小的字符串 #medium 从左到右删除*符号, 对于每个*符号, 都可以删去起左侧最小的一个字符 (有相同的话任意), 问删除所有*后的最小字符串
限制: n 1e5
思路: #贪心 注意到若出现多个最小字符, 则每次删除最右边的! 
    这里用的 #堆 来实现, 灵神中直接用 26 个栈来模拟
[ling](https://leetcode.cn/problems/lexicographically-minimum-string-after-removing-stars/solutions/2798240/yong-26-ge-zhan-mo-ni-pythonjavacgo-by-e-mhtn/)
    """
    def clearStars(self, s: str) -> str:
        st = []
        for i,c in enumerate(s):
            if c != '*':
                heapq.heappush(st, (c, -i))
            else:
                heapq.heappop(st)
        idxs = [-idx for _,idx in st]
        idxs.sort()
        return ''.join([s[i] for i in idxs])

    """ 3171. 找到按位或最接近 K 的子数组 #hard 给定一个数组, 找到一个子数组, 使其OR 和 给定的k的 (绝对)差 最小
限制: n 1e5; x 1e9
思路1: 从暴力出发进行优化
    显然, 有暴力 O(n^2) 的做法: 外层从左到右, 对于每个i位置从右往左考虑j
    [ling](https://leetcode.cn/problems/find-subarray-with-bitwise-or-closest-to-k/solutions/2798206/li-yong-and-de-xing-zhi-pythonjavacgo-by-gg4d/?utm_source=LCUS&utm_medium=ip_redirect&utm_campaign=transfer2china)
        考虑到OR的性质, 值是递增的! 
    考虑一个操作来利用该性质 —— 对于 `nums[j] | x != nums[j]` 的情况, 说明有新的位非零, 更新 nums[j] = nums[j] | x
        也是从右往左考虑j, 直到上面的条件不成立即可break! 
        为什么? 因为之前的更新 nums[j] 的操作, 实际上已经保证了每个位置都 >= 右侧的值
    -> 也可以从集合论的角度来看二进制, 见 ling
    """
    def minimumDifference(self, nums: List[int], k: int) -> int:
        ans = inf
        for i,x in enumerate(nums):
            ans = min(ans, abs(x-k))
            j = i - 1
            while j>=0 and nums[j] | x != nums[j]:
                nums[j] |= x        # 将x的非零位加入到nums[j]中
                ans = min(ans, abs(nums[j]-k))
                j -= 1
        return ans


sol = Solution()
result = [
    # sol.minimumChairs(s = "ELEELEELLL"),
    # sol.countDays(days = 10, meetings = [[5,7],[1,3],[9,10]]),
    # sol.clearStars(s = "aaba*"),
    sol.minimumDifference(nums = [1,3,1,3], k = 2),
]
for r in result:
    print(r)
