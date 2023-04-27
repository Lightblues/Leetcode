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
https://leetcode.cn/contest/weekly-contest-154
T2 的扩括号翻转题目好有意思! 进阶做法有些巧妙. T3 的分类讨论也需要一定的思维量. 
T4 考察了 Tarjan 有些超纲. 

@2022 """
class Solution:
    """ 1189. “气球” 的最大数量 """
    def maxNumberOfBalloons(self, text: str) -> int:
        cnt = Counter(text)
        return min(cnt['b'], cnt['a'], cnt['l']//2, cnt['o']//2, cnt['n'])
    
    """ 1190. 反转每对括号间的子串 #medium #parenthese #括号 #review #题型 给定一个字符串, 从内层到外层, 对于其中的所有括号内的元素进行反转 (结果中去除括号) 限制: n 2e3
思路1: #模拟 翻转, 可以采用 #栈 结构存储. 复杂度 O(n^2)
思路0: 记录每一个括号的 (s,e). 对于每个括号内部的元素, 若是奇数层则进行反转, 否则原样. 
    想要用一个 `def f(i,j, layer)` 来处理 s[i:j+1] 片段的第layer层翻转, 但因为预处理没做好无法解决类似 ((eqk((h)))) 的重叠括号问题. 放弃...
思路2: 实际上并不需要上面的预处理, 我们直接在原字符串中记录每一对括号的位置, 直接 #递归 解决即可. 这样, 只需要顺序输出. 
    图参见 [官答](https://leetcode.cn/problems/reverse-substrings-between-each-pair-of-parentheses/solution/fan-zhuan-mei-dui-gua-hao-jian-de-zi-chu-gwpv/)
    
"""
    def reverseParentheses(self, s: str) -> str:
        stack = []
        for c in s:
            if c == ')':
                tmp = []
                while stack[-1] != '(':
                    tmp.append(stack.pop())
                stack.pop()
                stack += tmp
            else:
                stack.append(c)
        return ''.join(stack)
    def reverseParentheses(self, s: str) -> str:
        # 得到原数组中的所有括号位置
        stack = []
        parentheses = {}
        for i,c in enumerate(s):
            if c=='(': stack.append(i)
            elif c==')': parentheses[stack.pop()] = i
            else: continue
        rparentheses = {v:k for k,v in parentheses.items()}
        # 递归处理
        ans = []
        def f(i,j,layer=0):
            # 处理 s[i:j+1] 的第 layer 层括号
            if layer==0:
                idx = i
                while idx<=j:
                    if s[idx] == '(':
                        f(idx+1, parentheses[idx]-1, 1)
                        idx = parentheses[idx]+1
                    else:
                        ans.append(s[idx])
                        idx += 1
            else:
                idx = j
                while idx>=i:
                    if s[idx] == ')':
                        f(rparentheses[idx]+1, idx-1, 0)
                        idx = rparentheses[idx]-1
                    else:
                        ans.append(s[idx])
                        idx -= 1
        f(0, len(s)-1)
        return ''.join(ans)
    # def reverseParentheses(self, s: str) -> str:
    #     # 预处理字符串
    #     n = sum(1 for c in s if c not in "()")
    #     chs = [None] * n
    #     parentheses = []        # 所有括号对
    #     st = []
    #     idx = 0
    #     # idx2layer = 
    #     idx2layerAcc = [0] * (n+1)  # 每个字符的层数
    #     for i,c in enumerate(s):
    #         if c=='(': st.append(idx)
    #         elif c==')': 
    #             l,r = (st.pop(), idx-1)
    #             parentheses.append((l,r))
    #             idx2layerAcc[l]+=1
    #             idx2layerAcc[r+1]-=1
    #         else: chs[idx] = c; idx += 1
    #     idx2layer = list(accumulate(idx2layerAcc))[:-1]
    #     parentheses.sort()
    #     lmap = {i: j for i, j in parentheses}
    #     # rmap = {j: i for i, j in parentheses}
    #     lidx2layer = {}
    #     layer = 0
    #     for lidx in sorted(i for i,j in parentheses):
    #         layer += 1
    #         lidx2layer[lidx] = layer
    #     # 
    #     ans = [''] * n
    #     def f(i,j, sidx=0):
    #         layer = lidx2layer.get(i, 0)
    #         # 根据所在层级, 将 s[i:j+1] 中的元素反转或原样输出, sidx 是在结果数组中的位置. 
    #         if layer % 2 == 0:
    #             idx = i
    #             while idx<=j:
    #                 if idx==i or idx not in lmap:
    #                     ans[sidx] = chs[idx]
    #                     sidx += 1; idx += 1
    #                 else:
    #                     f(idx, lmap[idx], sidx)
    #                     sidx += lmap[sidx] - idx + 1
    #                     idx = lmap[idx] + 1
    #         else:
    #             sidx = sidx + j - i
    #             idx = i
    #             while idx <= j:
    #                 if idx==i or idx not in lmap:
    #                     ans[sidx] = chs[idx]
    #                     sidx-=1; idx+=1
    #                 else:
    #                     f(idx, lmap[idx], sidx-(lmap[idx]-idx))
    #                     sidx -= lmap[idx] - idx + 1
    #                     idx = lmap[idx] + 1
    #     f(0,n-1,0)
    #     return ''.join(ans)
    
    """ 1191. K 次串联后最大子数组之和 #medium #题型 #review 对于 [arr]*k, 计算其中子数组的最大和 限制: n 1e5; k 1e5 对结果取模
思路1: 根据数组和 #分类 讨论
    若 sum(arr)<=0, 等价于求 [arr]*2 的「最大正子序列和」.
        如何求这个值? 就是累积前缀和
    若 sum(arr)>0, 则取中间的 k-1 个完整数组, 以及「最大前缀」和最大后缀. 
        如何求最大前缀和? 相较于上一种情况, 不能「重制」acc
    注意 #边界: k=1
说明: 求「最大子数组和」的算法叫做 #Kadane, 参见 [here](https://leetcode.cn/problems/k-concatenation-maximum-sum/solution/java-kadanesuan-fa-yu-jie-ti-si-lu-by-zdxiq125/)
"""
    def kConcatenationMaxSum(self, arr: List[int], k: int) -> int:
        mod = 10**9 + 7
        def maxSubarray(arr, prefix=False):
            ans = 0
            acc = 0
            for x in arr:
                acc += x
                if acc < 0 and not prefix: acc = 0
                ans = max(ans, acc)
            return ans
        s = sum(arr)
        if k==1: return maxSubarray(arr) % mod
        if s>0:
            return (s*(k-2) + maxSubarray(arr, prefix=True) + maxSubarray(arr[::-1], prefix=True)) % mod
        else:
            return (maxSubarray(arr*2)) % mod
    
    """ 1192. 查找集群内的关键连接 见 [Trajan] 这里自己写了一个简化版本 """
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        pass
    
sol = Solution()
result = [
    # sol.reverseParentheses("(abcd)"),
    # sol.reverseParentheses("(u(love)i)"),
    # sol.reverseParentheses(s = "(ed(et(oc))el)"),
    # sol.reverseParentheses("((eqk((h))))"), 
    # sol.kConcatenationMaxSum(arr = [1,-3,1], k = 5),
    # sol.kConcatenationMaxSum(arr = [1,2], k = 3),
    # sol.kConcatenationMaxSum([-5,-2,0,0,3,9,-2,-5,4], 5),
    # sol.kConcatenationMaxSum([4,-10,-2,-3,4], 1),
    # sol.criticalConnections(n = 4, connections = [[0,1],[1,2],[2,0],[1,3]]),
]
for r in result:
    print(r)
