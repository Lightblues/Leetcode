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
https://leetcode.cn/contest/weekly-contest-161



@2022 """
class Solution:
    """ 1247. 交换字符使得字符串相同 #easy 两个字符串仅包含 xy 两种字符, 每次可以交换 s1[i], s2[j]. 问最少交换多少次可以变为相同. 
注意: 能否成立跟xy的数量差无关, 就看两者的数量是否都为偶数.
思路1: 统计不匹配的 xy 的数量. 根据示例可以得到答案.
    示例: xx yy 的操作次数为1; xy yx 的操作次数为 2. 
https://leetcode.cn/problems/minimum-swaps-to-make-strings-equal/
"""
    def minimumSwap(self, s1: str, s2: str) -> int:
        #  对应位不匹配的数量
        ux, uy = 0,0
        for a,b in zip(s1,s2):
            if a!=b:
                if a=='x': ux+=1
                else: uy += 1
        if (ux+uy) % 2: return -1
        return ux//2 + uy//2 + (ux%2)*2
    
    """ 1248. 统计「优美子数组」 #medium 在一个数组中, 找到所有子数组, 其包含的奇数的数量正好为 k个. """
    def numberOfSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        oddIdx = []
        for i,x in enumerate(nums):
            if x%2: oddIdx.append(i)
        oddIdx = [-1] + oddIdx + [n]
        ans = 0
        for l in range(k, len(oddIdx)-1):
            ans += (oddIdx[l-k+1]-oddIdx[l-k]) * (oddIdx[l+1]-oddIdx[l])
        return ans
    
    """ 1249. 移除无效的括号 #medium 去掉字符串中不合法的括号. 例如 "a)b(c)d" 中删掉第一个 ).
思路1: 统计所有的括号位置, 然后用 #栈 来找到待删除的那些位置. 
[官答](https://leetcode.cn/problems/minimum-remove-to-make-valid-parentheses/solution/yi-chu-wu-xiao-gua-hao-by-leetcode/)
"""
    def minRemoveToMakeValid(self, s: str) -> str:
        ps = []
        for i,x in enumerate(s):
            if x=='(': ps.append((i,1))
            elif x==')': ps.append((i,2))
        st = []
        removed = []
        for i,x in ps:
            if x==1: st.append((i,x))
            else:
                if st: st.pop()
                else: removed.append(i)
        removed += [i for i,x in st]
        removed.sort()
        return ''.join([x for i,x in enumerate(s) if i not in removed])
    
    """ 1250. 检查「好数组」 #hard 给定一个正整数数组, 要求从中选一个子集, 将这个元素乘以任意整数, 要求之和为1. 问是否存在这样的子集. 限制: n 1e5; a[i] 1e9.
思路1: #裴蜀定理
    简化: 考虑两个数的情况
        观察: 两个互质的数字 x,y, 一定可以找到因子 ax+by=1
        说明: #裴蜀定理(重要推论) : a,b互质的充分必要条件是存在整数x,y使ax+by=1.
    推测: 对于多个数字的情况, 累计 gcd==1 即可.
see [here](https://leetcode.cn/problems/check-if-it-is-a-good-array/solution/shu-xue-he-365-shui-hu-wen-ti-lei-si-python-by-fe-/)
"""
    def isGoodArray(self, nums: List[int]) -> bool:
        g = nums[0]
        if g==1: return True
        for x in nums[1:]:
            g = math.gcd(g,x)
            if g==1: return True
        return False
    
    
sol = Solution()
result = [
    # sol.minimumSwap(s1 = "xxyyxyxyxx", s2 = "xyyxyxxxyx"),
    # sol.minimumSwap('xy', 'xx'),
    # sol.numberOfSubarrays(nums = [1,1,2,1,1], k = 3),
    # sol.minRemoveToMakeValid(s = "lee(t(c)o)de)"),
    sol.isGoodArray(nums = [12,5,7,23]),
]
for r in result:
    print(r)
