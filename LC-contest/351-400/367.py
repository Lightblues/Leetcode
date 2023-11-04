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
https://leetcode.cn/contest/weekly-contest-367

关于逆元, 见 [逆元 —— 广义化的倒数](https://zhuanlan.zhihu.com/p/449221995)
Python中的实现, 见 [stackoverflow](https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python)
    但是, 这里
Easonsi @2023 """
class Solution:
    """ 2903. 找出满足差值条件的下标 I """
    def findIndices(self, nums: List[int], indexDifference: int, valueDifference: int) -> List[int]:
        n = len(nums)
        for i in range(n):
            for j in range(i+indexDifference, n):
                if abs(nums[i]-nums[j]) >= valueDifference:
                    return [i,j]
        return (-1,-1)
    
    """ 2904. 最短且字典序最小的美丽子字符串 """
    def shortestBeautifulSubstring(self, s: str, k: int) -> str:
        n = len(s)
        if s.count('1') < k: return ""
        ans = "1" * n; mn = n
        l = cnt = 0
        for r,x in enumerate(s):
            if x == '1': cnt += 1
            # NOTE: 这里的第二个判断, 去除前缀0
            while cnt > k or s[l] != '1':
                if s[l] == '1': cnt -= 1
                l += 1
            if cnt == k:
                if r-l+1 < mn:
                    mn = r-l+1
                    ans = s[l:r+1]
                elif r-l+1 == mn:
                    ans = min(ans, s[l:r+1])
        return ans
    
    """ 2905. 找出满足差值条件的下标 II #medium 找到下标 i,j, 满足 abs(i-j)>=indexDifference, abs(nums[i]-nums[j])>=valueDifference
限制: n 1e5
思路1: 「滑动窗口」, 遍历过程中, 记录当前满足 idx条件的数字 (mn,mx)
"""
    def findIndices(self, nums: List[int], indexDifference: int, valueDifference: int) -> List[int]:
        n = len(nums)
        mn = mx = nums[0]
        imn = imx = 0
        for i in range(indexDifference, n):
            # NOTE: 注意 indexDifference==0
            if i>indexDifference:
                val = nums[i-indexDifference]
                if val < mn: mn, imn = val, i-indexDifference
                if val > mx: mx, imx = val, i-indexDifference
            x = nums[i]
            if abs(x-mn) >= valueDifference:
                return [imn, i]
            if abs(x-mx) >= valueDifference:
                return [imx, i]
        return (-1,-1)
    
    """ 对于除法逆元的探究
方法1: 扩展欧几里德定理, 适用于所有的n的情况
方法2: 费马小定理, 注意只适用于素数p的情况
see https://zhuanlan.zhihu.com/p/449221995
    """
    def mod_inv(self):
        def egcd(a, b):
            """ 给定正整数 a,b，求满足等式 ax+by = 1 的 x 的最小正整数解。
            返回: (g,x,y) 当g==1说明问题有解
            """
            if a == 0:
                return (b, 0, 1)
            else:
                g, y, x = egcd(b % a, a)
                return (g, x - (b // a) * y, y)
        def modinv(a, m):
            """ 返回 a关于数字p的乘法逆元; 注意可能不存在 
            也即求 ax = 1 (mod p) 的最小正整数解, 也即 ax = bm + 1, k为整数
                转换一下, 就是求 ax + bm = 1 的最小正整数解
            """
            g, x, y = egcd(a, m)
            if g != 1:
                raise Exception('modular inverse does not exist')
            else:
                return x % m
            
        def modinv2(x, p):
            # Python中的接口
            return pow(x, -1, p)
        def modinv3(x, p):
            # 费马小定理. 注意, 这里的 p 需要是素数
            return pow(x, p-2, p)
        
        print(modinv(2,7))
        print(modinv2(2,7))
        print(modinv3(2,7))

    """ 2906. 构造乘积矩阵 #medium #题型 #hard 对于一个矩阵的元素 g[i,j], 将其转为 prod(g) / g[i,j] % p
限制: n*m 1e5
思路0: 转为 log, 但是精度不够
思路1: #前后缀 分解
    [灵神](https://leetcode.cn/problems/construct-product-matrix/solutions/2483137/zhou-sai-chang-kao-qian-hou-zhui-fen-jie-21hr/)
    还总结了「前后缀分解」的题单
思路2: 乘法逆元 #hard
注意, 本题等于 0238. 除自身以外数组的乘积 
    """
    def constructProductMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        p = 12345
        m,n = len(grid), len(grid[0])
        ll = n*m
        llist = list(itertools.chain.from_iterable(grid))
        suf = [1] * ll
        pre = [1] * ll
        t1 = t2 = 1
        for i in range(ll):
            pre[i] = t1
            t1 = t1 * llist[i] % p
            suf[ll-1-i] = t2
            t2 = t2 * llist[ll-1-i] % p
        for idx in range(ll):
            i,j = divmod(idx, n)
            grid[i][j] = pre[idx] * suf[idx] % p
        return grid
        
    def constructProductMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        # WA: 尝试转为 log, 但是精度不够
        import numpy as np
        p = 12345
        m,n = len(grid), len(grid[0])
        log_grid = np.log(grid)
        ss = np.sum(log_grid)
        for i,j in product(range(m), range(n)):
            grid[i][j] = round(np.exp(ss - log_grid[i][j]) % p)
        return grid

sol = Solution()
result = [
    # sol.shortestBeautifulSubstring(s = "100011001", k = 3),
    # sol.shortestBeautifulSubstring(s = "1011", k = 2),
    # sol.findIndices(nums = [5,1,4,1], indexDifference = 2, valueDifference = 4),
    # sol.findIndices([1],0,1),
    # sol.findIndices([6,5,5,10,4,3],1,5),
    # sol.constructProductMatrix(grid = [[1,2],[3,4]]),
    # sol.constructProductMatrix(grid = [[12345],[2],[1]]),
    
    sol.mod_inv(),
]
for r in result:
    print(r)
