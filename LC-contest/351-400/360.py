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
https://leetcode.cn/contest/weekly-contest-360
https://leetcode.cn/circle/discuss/VghzJ4/



Easonsi @2023 """
class Solution:
    """ 2833. 距离原点最远的点 """
    def furthestDistanceFromOrigin(self, moves: str) -> int:
        cnt = Counter(moves)
        diff = abs(cnt['L'] - cnt['R'])
        return diff + cnt['_']
    
    """ 2834. 找出美丽数组的最小和 """
    def minimumPossibleSum(self, n: int, target: int) -> int:
        if n==1: return 1
        ava = min(target//2, n)
        ans = ava * (ava+1) // 2
        if n > ava:
            ans += (2*target+n-ava-1) * (n-ava) // 2
        return ans
    
    """ 2835. 使子序列的和等于目标的最少操作次数 #hard 所有数组元素都是 2^j, 每次操作可以选择一个数变成两个 2^(j-1), 问最少操作次数使得和为target.
限制: n 1e3; MAX 2^31
"""
    def minOperations(self, nums: List[int], target: int) -> int:
        targ = []
        LEN = 32
        for i in range(LEN):
            if target & (1<<i):
                targ.append(i)
        cnt = [0] * LEN
        for x in nums:
            cnt[int(log2(x))] += 1
        _n = len(targ)
        _idx = 0
        ans = 0
        remains = 0
        for i,c in enumerate(cnt):
            c += remains
            if c==0: continue
            if targ[_idx] <= i:
                c -= 1
                # 至少需要从 i 拆分到 targ[_idx]
                if targ[_idx] < i:
                    ans += i - targ[_idx]
                _idx += 1
                while _idx < _n and targ[_idx] < i:
                    _idx += 1
                # 还同时有一个 i
                if c>0 and _idx<_n and targ[_idx]==i:
                    c -= 1
                    _idx += 1
                # 提前结束
                if _idx==_n: break
            remains = c // 2
        if _idx<_n: return -1
        else: return ans
                
    """ 2836. 在传球游戏中最大化函数值 #hard 一队列人, 每个人传给下一个人的idx都是固定的 (#基环树), 一个路径的分数是所有序号之和, 问k次的最大路径. 
限制: N 1e5
思路1: #倍增 
    关联: 如何快速得到树上节点的K阶祖先? 可以对于每个节点构建 1/2/4... 级祖先. 也即「1483. 树节点的第 K 个祖先」
    记 f[x, i] = (j, pathValue) 表示节点x, 的第 2^i 级祖先是 j, 且路径值为 pathValue.
        则有 f[x,i] = f[f[x,i-1], i-1]
见 [灵神](https://leetcode.cn/problems/maximize-value-of-function-in-a-ball-passing-game/solutions/2413298/shu-shang-bei-zeng-by-endlesscheng-xvsv/)
思路2: 考虑 #内向基环树 可以实现 O(n) 复杂度
"""
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int: 
        # MLE
        @lru_cache(None)
        def f(x, i):
              if i==0: return receiver[x], x
              j, pathValue = f(x, i-1)
              jj, pathValue2 = f(j, i-1)
              return jj, pathValue + pathValue2
        ans = 0
        n = len(receiver)
        for i in range(n):
            tmp = 0
            cur = i
            for j in range((k+1).bit_length()):
                if ((k+1) >> j) & 1:
                    cur, pValue = f(cur, j)
                    tmp += pValue
            ans = max(ans, tmp)
        return ans
    def getMaxFunctionValue(self, receiver: List[int], k: int) -> int: 
        n = len(receiver)
        k += 1  # 转移k次, 计算 k+1 个人的序号
        BLEN = k.bit_length()
        f = [[(fa,x) for x, fa in enumerate(receiver)]]
        for j in range(1, BLEN):
            nf = [(-1,-1)] * n
            for i in range(n):
                fa,value1 = f[j-1][i]
                ffa,value2 = f[j-1][fa]
                nf[i] = (ffa, value1+value2)
            f.append(nf)
        ans = 0
        for i in range(n):
            tmp = 0
            cur = i
            for j in range(BLEN):
                if (k >> j) & 1:
                    cur, pValue = f[j][cur]
                    tmp += pValue
            ans = max(ans, tmp)
        return ans
                
                
            
sol = Solution()
result = [
    # sol.minimumPossibleSum(n = 2, target = 3),
    # sol.minimumPossibleSum(n = 3, target = 3),
    # sol.minOperations(nums = [1,2,8], target = 7),
    # sol.minOperations(nums = [1,32,1,2], target = 12),
    # sol.minOperations(nums = [1,32,1], target = 35),
    # sol.minOperations([16,16,4], 3), 
    # sol.minOperations([128,1024,1073741824,4194304,268435456,1024,16,1073741824,131072,4,16777216,67108864,16777216,268435456,1073741824,256,16,67108864,1048576,16,4,4194304,1024,16,262144,1048576,1024,128,1073741824,67108864,65536,128,32768,128,32768,8192,256,1024], 38), 
    sol.getMaxFunctionValue(receiver = [2,0,1], k = 4),
    sol.getMaxFunctionValue(receiver = [1,1,1,2,3], k = 3),
]
for r in result:
    print(r)
