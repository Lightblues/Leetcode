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
https://leetcode.cn/contest/biweekly-contest-132

T4 的DP有点难度! 比较有趣的一个题目场景! 
Easonsi @2025 """
class Solution:
    """3174. 清除数字  """
    def clearDigits(self, s: str) -> str:
        st = []
        for ch in s:
            if ch in string.digits:
                st.pop()
            else:
                st.append(ch)
        return ''.join(st)
    
    """ 3175. 找到连续赢 K 场比赛的第一位玩家 """
    def findWinningPlayer(self, skills: List[int], k: int) -> int:
        mxIdx=0; acc=0
        for i in range(1, len(skills)):
            if skills[i] > skills[mxIdx]:
                mxIdx = i
                acc = 1
            else:
                acc += 1
            if acc >= k: return mxIdx
        return mxIdx
    
    """ 3176. 求出最长好子序列 I #medium 从一个数组中找子序列, 要求满足相邻元素不相等的次数最多只有k个, 问最长长度. """
    """ 3177. 求出最长好子序列 II #hard 从一个数组中找子序列, 要求满足相邻元素不相等的次数最多只有k个, 问最长长度. 
限制: n 5e3; k 50
思路1: #DP
    记 f[i,j] 表示最后的数字是第i个数字, 不相等次数为j的最长子序列的长度
    递推:
        f[i,j] = max{ f[x][j-1]+1 if nums[x]!=nums[i] else f[x][j]+1 for x in range(i) }
    边界: f[i,0] = 1
    复杂度: O(n^2k) 不可接受
    优化: 考虑在遍历过程中, 只需要考虑两种:
        - nums[x]!=nums[i] 这时直接取 f[x][j-1] 最大的即可;
        - nums[x]==nums[i] 只需要考虑最近的那个数字同样为 nums[x] 的那个位置
        总结, 我们可以用一个辅助数组 zd[j] 来记录 "不相等次数为j的最长子序列的长度"!
    复杂度: O(nk)
official: https://leetcode.cn/problems/find-the-maximum-length-of-a-good-subsequence-ii/solutions/2905802/qiu-chu-zui-chang-hao-zi-xu-lie-ii-by-le-ydi5/
    """
    def maximumLength(self, nums: List[int], k: int) -> int:
        zd = [0] * (k+1)
        f = defaultdict(lambda: [0]*(k+1))
        for i, x in enumerate(nums):
            pre = f[x] # 上一个同样为 x 的位置的最大长度
            for j in range(k+1):
                pre[j] += 1 # 数字相同, 子序列可以免费 +1
                if j > 0:
                    pre[j] = max(pre[j], zd[j-1]+1) # 利用此前最长的子序列, 加上 x
            # 利用x结尾的的最大长度更新 zd
            for j in range(k+1):
                zd[j] = max(zd[j], pre[j])
        return zd[k]

    
sol = Solution()
result = [
    # sol.findWinningPlayer(skills = [4,2,6,3,9], k = 2),
    # sol.findWinningPlayer(skills = [2,5,4], k = 3),
    sol.maximumLength(nums = [1,2,1,1,3], k = 2),
]
for r in result:
    print(r)
