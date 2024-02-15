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
https://leetcode.cn/contest/weekly-contest-382
https://leetcode.cn/circle/discuss/gQg8iV/
T2 的边界情况比较恼人; T4 位运算比较难! 注意是两个数字合并为一个!

Easonsi @2023 """
class Solution:
    """ 3019. 按键变更的次数 """
    def countKeyChanges(self, s: str) -> int:
        s = s.lower()
        pre = s[0]
        cnt = 0
        for c in s[1:]:
            if pre==c:
                continue
            else:
                cnt += 1
                pre = c
        return cnt
    
    """ 3020. 子集中元素的最大数量 """
    def maximumLength(self, nums: List[int]) -> int:
        cnt = Counter(nums)
        ans = 1
        # 注意为1的边界情况!!!
        n1 = cnt[1]
        an1 = n1 if (n1%2) else n1-1
        ans = max(ans, an1)
        m = defaultdict(lambda: 1)
        for x in sorted(cnt.keys()):
            if x==1: continue
            # # isqrt 可以无误差地计算整数平方根的整数部分
            sqrted = int(sqrt(x))
            if sqrted**2 != x: continue
            if cnt[sqrted] >= 2:
                ans = max(ans, m[sqrted] + 2)
                m[x] = m[sqrted] + 2
        return ans

    """ 3021. Alice 和 Bob 玩鲜花游戏
问题等价于, 求两个非0数字之和为奇数的组合数量
    """
    def flowerGame(self, n: int, m: int) -> int:
        n1 = n//2 + (n%2)       # n1 是奇数的个数
        ans = n1 * (m//2)
        n2 = n//2                # n2 是偶数的个数
        ans += n2 * (m//2 + m%2)
        return ans
    

    """ 3022. 给定操作次数内使剩余元素的或值最小 #hard 对于一个序列, 每次可以选择位置 i,i+1, 将两个数字替换为一个数字 AND 的结果. 问经过最多k次操作后, 变换后数组 OR 的最小值. 
限制: n 1e5; nums[i] 2^30;  k<n
思路1: #试填法 from [ling](https://leetcode.cn/problems/minimize-or-of-remaining-elements-using-operations/solutions/2622658/shi-tian-fa-pythonjavacgo-by-endlesschen-ysom/)
    NOTE: 由于是两个数字合并为一个数字, 因为连续的数字合并, 其顺序不重要! —— 因此可以「从左到右」来考虑!
    1] 从高位到低位, 看是否可以变成0; 2] 注意到, 若该为无法变成0, 则不需要考虑这一位! 
    3] 重要的是, 如何在考虑低位的时候也保留高位需要删除的信息? 可以用一个mask来记录需要删除的位!
    PS: 题目保证了 k<n, 避免了特殊条件的判断
    """
    def minOrAfterOperations(self, nums: List[int], k: int) -> int:
        m = max(nums).bit_length()
        mask = 0        # mask 记录了当前, 还是高位的需要被删去的
        for b in range(m-1, -1, -1):
            mask |= 1 << b  # 此前高位 + 当前位 所需要删掉的地方
            cnt = 0         # 此前高位 + 当前位 要全部删去所需要步数, 一个限制条件!
            and_res = -1    # 全 1
            for x in nums:
                and_res &= (x&mask)
                if and_res:
                    cnt += 1    # 当前位需要被删掉
                else:
                    and_res = -1    # 此前span的mask位都被清空! 考虑下一span
            if cnt > k:
                mask ^= 1<<b    # 当前位无法被删去! 复原
        ans = reduce(operator.or_, nums)
        return (ans) & (~mask)

    
sol = Solution()
result = [
    # sol.maximumLength(nums = [5,4,1,2,2]),
    # sol.flowerGame(3,2),
    # sol.flowerGame(1,1),
    # sol.flowerGame(4, 3),
    sol.minOrAfterOperations(nums = [3,5,3,2,7], k = 2),
    sol.minOrAfterOperations(nums = [7,3,15,14,2,8], k = 4),
]
for r in result:
    print(r)
