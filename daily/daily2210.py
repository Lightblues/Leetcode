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


@2022 """
class Solution:


    """ 0754. 到达终点数字 #medium 但实际上很 #hard #数学 #题型 要从位置0走到target. 在每一步, 可以选择左/右一定i步. 问走到target最少需要多少步. 限制: target +/-1e9
只需要考虑正整数情况. 
利用到的结论: 假设 s = sum(1...k), 则对于在 [1,s] 范围内的任意整数 x, 都可以找到 1...k 中的一组数字 set, 使其和为 x. 
    证明: 归纳法. 
思路1: 
    显然, 先要能够到达target, 我们先取最小的 s=sum(1...k) >= target.
    记 `d = s-target`. 然后 #分类
        考虑翻转一个数字x的符号, 其对于和产生了 -2x 的影响, 一定是奇数!!!
        若 d为偶数. 则根据上面的节点, 我们可以找到一组数字, 使其和为 d/2. 
            (事实上在本题中, 我们可以找到一个大小为1的set.)
        若 d为奇数. 考虑 k+1 的符号,
            1) 如为奇数, 则s的变为偶数. 答案为 k+1
            2) 若为偶数, 注意到 k+1 + k+2 一定是一个奇数. 则此时 s必然为偶数. 答案为 k+2
参见 [官答](https://leetcode.cn/problems/reach-a-number/solution/dao-da-zhong-dian-shu-zi-by-leetcode-sol-ak90/)
图解见 [灵神](https://leetcode.cn/problems/reach-a-number/solution/fen-lei-tao-lun-xiang-xi-zheng-ming-jian-sqj2/)
"""
    def reachNumber(self, target: int) -> int:
        target = abs(target)
        k = 0; acc = 0
        while acc < target:
            k += 1
            acc += k
        d = acc - target
        if d%2 == 0: return k
        else: return k + (1 if k%2==0 else 2)
    
    """ 0891. 子序列宽度之和 #hard 对于数组的所有子序列, 定义其「宽度」为 mx-mn, 问最有子序列的宽度之和. 限制: n 1e5
思路1: 先 #排序, 算出每个元素在子序列中作为最大值/最小值的次数. 
[灵神](https://leetcode.cn/problems/sum-of-subsequence-widths/solution/by-endlesscheng-upd1/)
关联: 2104. 子数组范围和
"""
    def sumSubseqWidths(self, nums: List[int]) -> int:
        MOD = 10 ** 9 + 7
        nums.sort()
        n = len(nums)
        pow2 = [0] * n
        pow2[0] = 1
        for i in range(1, n):
            pow2[i] = pow2[i - 1] * 2 % MOD  # 预处理 2 的幂次
        return sum((pow2[i] - pow2[-1 - i]) * x
                   for i, x in enumerate(nums)) % MOD

""" 0895. 最大频率栈 #hard 实现一个类似堆栈的结构, push(int val), pop() 移除频率最大的元素, 若有多个, 则移除最接近栈顶的 (最近插入的). 限制: 操作次数 2e4
思路1: 用一个字典记录元素出现频率; 将元素分别存到出现 一次、两次、三次... 的栈列表中.
    具体见灵神的动画演示.
    复杂度: O(q)
[灵神](https://leetcode.cn/problems/maximum-frequency-stack/solution/mei-xiang-ming-bai-yi-ge-dong-hua-miao-d-oich/)
"""
class FreqStack:
    def __init__(self):
        self.cnt = Counter()
        self.stacks = []

    def push(self, val: int) -> None:
        # 将val插入到 一次、两次、三次... 所对应的栈中
        c = self.cnt[val]
        if c == len(self.stacks):
            self.stacks.append([val])
        else:
            self.stacks[c].append(val)
        self.cnt[val] += 1

    def pop(self) -> int:
        val = self.stacks[-1].pop()
        self.cnt[val] -= 1
        if not self.stacks[-1]:
            self.stacks.pop()
        return val
    
sol = Solution()
result = [

    # sol.reachNumber(3),
    # sol.reachNumber(2),
    testClass("""["FreqStack","push","push","push","push","push","push","pop","pop","pop","pop"]
[[],[5],[7],[5],[7],[4],[5],[],[],[],[]]"""),
]
for r in result:
    print(r)
