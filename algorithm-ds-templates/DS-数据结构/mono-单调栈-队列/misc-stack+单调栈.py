from easonsi import utils
from easonsi.util.leetcode import *
""" 单调栈题型
=== 得到指定条件的子序列
0316. 去除重复字母 #medium #题型 #单调栈 #stack
    要求得到一个字符串的子串, 1) 由原本字符串中的所有元素组成; 2) 所有字符不重复; 3) 字典序最小.
2030. 含特定字母的最小子序列 #单调栈 #hard #题型
    给定一个字符串s要求找到一个长度为k的子序列 (不要求连续), 使得: 1) 其中包含至少 repetition 个特定字符 letter; 2) 子序列字典序最小.




1793. 好子数组的最大分数 #hard
    定义子数组的score为, 数组中的最小值*数组长度. 现给定一个数组和一个下标k, 要求找到包含下标k的子数组的最大score.
    见232.py 也是求两个边界.

6080. 使数组按非递减顺序排列 #medium #题型
    给定一个数组经过若干次删除操作将其变为非递减数组. 每次操作定义为: 删除满足 `nums[i - 1] > nums[i]` 的位置的元素 i. 问经过多少次操作后得到最终结果 (非递减).
    利用单调栈维护「该元素被删除的时刻」


== 比较特殊的pop条件
1776. 车队 II #hard #题型 #单调栈 #hardhard
有一组车 (position, speed) 相同方向行驶. 当两辆车相遇时, 它们按照较低速度组成「车队」. 问所有车与下一辆车相遇的时间 (不相遇则为 -1).
    提示: 一定是速度快的车从后面追上前一辆车. 这题的难点在于, 虽然idx可以追上idx+1车, 但idx+1的速度可能会被更前面的车所「拖慢」, 因此实际上相遇时间是需要计算得失idx和idx+x的相遇所需时间.
    思路1: 用 #单调栈 递增栈, 来记录可能会被追到的车. 然后需要根据追到栈顶元素的时候, 以及栈顶元素追到下一个车的时间的大小关系进行讨论.
    比较繁琐细致.

@2022 """
class Solution:
    """ 0316. 去除重复字母 #medium #题型 #单调栈 #stack
要求得到一个字符串的子串, 1) 由原本字符串中的所有元素组成; 2) 所有字符不重复; 3) 字典序最小.
思路: 单调栈
    去除限制条件, 我们如何得到一个尽可能小的字符串? 基本思路是 **维护一个单调栈**, 当遇到一个新的字符时, 如果栈顶元素小于当前字符, 则递归弹出栈顶元素, 然后再把这个字符入栈; 否则直接把当前字符压入栈 (注意当前字符总会入栈).
    这里要求 1) 保留原字符串中的所有元素, 因此用一个 counter 记录剩余的数量, 当剩余数量为0时, 我们不能将该元素弹出栈; 3) 字符不重复, 因此在入栈的时候判断该字符是否已经在栈内.
[here](https://leetcode.cn/problems/remove-duplicate-letters/solution/qu-chu-zhong-fu-zi-mu-by-leetcode-soluti-vuso/)
"""
    def removeDuplicateLetters(self, s: str) -> str:
        stack = []
        # counter 记录字母剩余的数量
        counter = collections.Counter(s)
        for ch in s:
            counter[ch] -= 1
            # 字符已经用过了, 去重
            if ch in stack: continue
            while stack and ch < stack[-1]:
                # 注意这里是 while, 例如 "bcabc" 需要将栈中的 bc 都弹出.
                # 剩余字符还有, 可以弹出
                if counter[stack[-1]] > 0: stack.pop()
                else: break
            # ch 在 ch < stack[-1] 与否两种情况下都会入栈
            stack.append(ch)
        return "".join(stack)


    """ 2030. 含特定字母的最小子序列 #单调栈 #hard #题型
给定一个字符串s要求找到一个长度为k的子序列 (不要求连续), 使得: 1) 其中包含至少 repetition 个特定字符 letter; 2) 子序列字典序最小.
关联: 0316. 去除重复字母; 另有基本题型「求长为 k 的字典序最小子序列」
本题的限制包括 1) 子序列长度为 k; 2) 子序列中包含至少 repetition 个特定字符 letter.
思路: 单调栈, 注意判断这些限制条件!
单调栈相关问题思路: 
- 注意空栈 pop 的错误;
- 限制子序列长度为 k: 1) 在push的时候判断时候超过限制; 2) pop时判断剩余的是否够, 即使 break;
- 限制栈内元素数量 (比如要求ch的数量至少为repetition): 1) pop的时候检查剩余是否够; 2) 另外需要检查, 若栈内元素不足以放剩余的ch (repetition-countInStack), 则需要push.
"""
    def smallestSubsequence(self, s: str, k: int, letter: str, repetition: int) -> str:
        countLetter = collections.Counter(s)[letter]
        stack = []
        n = len(s)
        # 允许从栈中弹出的 letter 数量
        # possPop = counter[letter] - repetition
        # 
        cInStack = 0 # 当前栈中的字符 letter 数量
        cPop = 0     # 弹出的 letter数量
        for i, ch in enumerate(s):
            """ 单调栈的 pop 条件: 递归弹出比当前判断元素大的栈顶元素 """
            # 注意防止 stack 空
            while stack and ch < stack[-1]:
                # 条件1: 长度k的约束不允许弹出
                if len(stack) + (n-i) <= k:
                    break
                if stack[-1]==letter:
                    # 条件2: 不允许弹出 letter 了
                    if countLetter - cPop - 1 < repetition:
                        break
                    cPop += 1
                    cInStack -= 1
                    stack.pop()
                else:
                    stack.pop()
            # 条件2: 剩余空间不足以放剩下的 letter
            # while k - len(stack) < repetition-cInStack: 
            #     c = stack.pop()
            #     # cInStack -= c==letter
            # 每次压入栈一个元素的时候检查即可, 不需要用到while
            if k-len(stack) < repetition-cInStack:
                stack.pop()
            # 条件1: 长度k约束. 当前栈已经超过 k 了, 不在压入栈
            if len(stack) >= k:
                cPop += ch==letter
                continue
            stack.append(ch)
            if ch==letter:
                cInStack += 1
        return "".join(stack)










    """ 6080. 使数组按非递减顺序排列 #medium #题型
给定一个数组经过若干次删除操作将其变为非递减数组. 每次操作定义为: 删除满足 `nums[i - 1] > nums[i]` 的位置的元素 i. 问经过多少次操作后得到最终结果 (非递减).
尝试0: 一开始想到, 通过一次遍历可以得到最终保留的子序列. 这样只需要计算这些idx所分割的每一个连续序列中, 需要进行的操作次数即可. 
    然而, 对于如何计算按照的删除方式「删除序列中的每一个元素」, 还是没想出来. 一开始想记录每一个递增序列的长度, 但是还需要考虑到 [1,2,3,1,2,3] 中, 第二个3 这样的情况.
思路1: 单调栈
    [here](https://leetcode.cn/problems/steps-to-make-array-non-decreasing/solution/by-endlesscheng-s2yc/)
    对于每一个元素 i, (若会被删除), 其删除时间由什么决定? 由 `nums[i - 1] > nums[i]` 这一公式决定. 也即其左侧的第一个比它大的元素, 记为 j.
    如何记录 j 的删除时间? 可以通过一个(严格)单调递减栈来解决.
    具体而言, 栈内记录 `(num, delete_time)`, 后者为它被移除的时刻. 对于每一个元素, 移除所有满足 `stack[-1][0] <= num` 的栈顶元素 (注意是小于等于).
        相等的时候, 1) 若num被保留, 下面的 `if stack` 语句确保了其移除时间的记录为 0; 2) num被移除, 则其被移除的时刻同样取决于上一个值为 num的元素. 例如 [3,1,2,1,2] 中两个2的移除时刻分别为 2,3.
    若经过pop操作后栈空, 说明该元素会被保留到最后, 其 `delete_time` 为 0. 否则, 为出栈元素中  `delete_time` 最大值 +1. 也即, `if stack: maxt += 1`
    """
    def totalSteps(self, nums: List[int]) -> int:
        """ [here](https://leetcode.cn/problems/steps-to-make-array-non-decreasing/solution/by-endlesscheng-s2yc/)
        """
        # 栈内元素为 (num, maxt) 其中第二个数字是它被移除的时刻
        stack = []
        ans = 0
        for num in nums:
            maxt = 0    # 记录num左侧的元素的小于等于num的元素的最大移除时间
            # 注意这里是 <=. 相等的时候, 1) 若num被保留, 下面的 `if stack` 语句确保了其移除时间的记录为 0; 2) num被移除, 则其被移除的时刻同样取决于上一个值为 num的元素. 例如 [3,1,2,1,2] 中两个2的移除时刻分别为 2,3.
            while stack and stack[-1][0] <= num:
                maxt = max(maxt, stack.pop()[1])
            # 若栈为空, 说明是新的最大元素, 其被移除的时刻为 0; 否则, 该元素会被移除, 其被移除的时刻为 maxt+1.
            if stack: maxt += 1
            ans = max(ans, maxt)
            stack.append((num, maxt))
        return ans



    """ 1776. 车队 II #hard #题型 #单调栈
有一组车 (position, speed) 相同方向行驶. 当两辆车相遇时, 它们按照较低速度组成「车队」. 问所有车与下一辆车相遇的时间 (不相遇则为 -1).
限制: 数组长度 1e5;  位置,速度 1e6
提示: 一定是速度快的车从后面追上前一辆车.
    这题的难点在于, 虽然idx可以追上idx+1车, 但idx+1的速度可能会被更前面的车所「拖慢」, 因此实际上相遇时间是需要计算得失idx和idx+x的相遇所需时间.
思路1: 用 #单调栈 递增栈, 来记录可能会被追到的车
    从右往左遍历. 用一个「单调递增栈」进行记录.
    #分类: 1) 若栈顶速度更快, 追不上, 而idx后面的车一定会被idx拖慢, 所以栈顶元素没用了, pop; 2) 否则, 说明idx可以追上栈顶元素, 但时间怎么算? 我们 计算idx追上栈顶所需的时间, 若该时间小于栈顶元素追上下一车的时间, 则直接利用两者计算; 否则, 我们递归栈内下一个元素, 直到找到满足条件的车. 注意到, 对于不满足要求的, **栈顶元素会在下一辆车追到之前撞上栈内下一个元素, 因此没有用了**, 可以pop. (从而将复杂度从 `O(n^2)` 降为 `O(n)`)
    参见 [here](https://leetcode.cn/problems/car-fleet-ii/solution/dan-diao-zhan-xiang-xi-jie-fa-by-2018272-5ff7/)
"""
    def getCollisionTimes(self, cars: List[List[int]]) -> List[float]:
        # 思路1
        n = len(cars)
        ans = [-1] * n
        stack = []
        for i in range(n-1, -1, -1):
            p,v = cars[i]
            while stack:    # (p,v,i)
                # 栈顶元素更快, 则左侧的车都不会与它发生碰撞, 没用了.
                if stack[-1][1]>=v:
                    stack.pop()
                else:
                    # 栈顶尚未发生碰撞 (它是从左往右目前最快的), 则一定会撞到它
                    if ans[stack[-1][-1]] == -1:
                        ans[i] = (stack[-1][0]-p)/(v-stack[-1][1])
                        break
                    # 否则, 需要判断在栈顶元素发生碰撞 (速度被拖慢) 之前, 能否追到它. 
                    # 若可以追到, 则结束; 否则, 继续考察栈内下一个元素.
                    # 下面注释部分没有pop不需要的元素, 复杂度 O(n^2)
                    # idx = len(stack)-1
                    # while ans[stack[idx][-1]]>0 and (stack[idx][0]-p)/(v-stack[idx][1]) > ans[stack[idx][-1]]:
                    #     idx -= 1
                    # ans[i] = (stack[idx][0]-p)/(v-stack[idx][1]) 
                    # break
                    # 思路1
                    t = (stack[-1][0]-p) / (v-stack[-1][1])
                    if t < ans[stack[-1][-1]]:
                        ans[i] = t
                        break
                    else:
                        stack.pop()

            stack.append((p,v,i))
        return ans
    


sol = Solution()
result = [
    
]
for r in result:
    print(r)
