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
https://leetcode.cn/contest/weekly-contest-319
视频: https://www.bilibili.com/video/BV13841187gz/
总体难度较大. T2 最小公倍数, 注意遍历right时候的递推关系. T3计算「通过交换数对使得数组有序的最少交换次数」学到了新东西. T4回文, 也在超时边缘尝试了几次. 

@2022 """

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 6233. 温度转换 """
    
    """ 6234. 最小公倍数为 K 的子数组数目 #medium #题型 统计数组的所有子数组中, lcm为k的数量. 
思路1: 暴力枚举. 对于每个位置开始往后匹配right
    复杂度: 涉及到lcm/gcd的计算复杂度. 结论是 O(n (n+logk))
思路2: 利用lcm的性质. 见灵神题解. 
关联: 2447. 最大公因数等于 K 的子数组数目 基本是一样的
见 [灵神](https://leetcode.cn/problems/number-of-subarrays-with-lcm-equal-to-k/solution/by-endlesscheng-3qnt/)
另外, 灵神视频中还讲了 #hack 的方法, 构造反例
"""
    def subarrayLCM(self, nums: List[int], k: int) -> int:
        ans = 0
        n = len(nums)
        for i in range(n):
            c = 1       # 注意初始化, lcm
            for j in range(i,n):
                c = math.lcm(c, nums[j])
                # if c>k: break
                if k%c: break
                if c==k: ans+=1
        return ans
    
    """ 6235. 逐层排序二叉树所需的最少操作数目 #medium 二叉树上每个节点值都不同. 每次操作可以将同层的不同节点进行交换. 问使得每一层都递增的最少操作数. 
思路1: #置换环 + #离散化
    对于每一层, 需要计算「通过交换数对使得数组有序的最少交换次数」. 经典问题, 解决的方案是 #置换环
        也即, 对于一个长k的 #环, 需要交换的次数为 k-1
    如何找到环 (计数)? 经典的思路是顺着环的方向, 直到回到入环点. 可以通过一个vis数组来记录访问情况.
        #WA, 一开始计算的方法写错了, 见下代码
    参见 [灵神](https://leetcode.cn/problems/minimum-number-of-operations-to-sort-a-binary-tree-by-level/solution/by-endlesscheng-97i9/)
关联: 0765. 情侣牵手
"""
    def minimumOperations(self, root: Optional[TreeNode]) -> int:
        def count_v0(arr):
            # 计算通过交换数对使得数组有序的最少交换次数.
            # 错了! 例子: [4,3,1,2] 答案应该是3
            sorted_arr = sorted(arr)
            x2order = {x:i for i,x in enumerate(sorted_arr)}
            cnt = 0; s = set()
            for i,x in enumerate(arr):
                if i==x2order[x]: continue
                if x2order[x] in s: continue
                else: s.add(i); cnt+=1
            return cnt
        def count(arr):
            n = len(arr)
            # 离散化! 计算每个元素对应到sorted的位置
            a = sorted(range(n), key=lambda i: arr[i])
            vis = [False]*n
            cnt_ring = 0
            for v in a:
                if vis[v]: continue
                while not vis[v]:
                    vis[v] = True
                    v = a[v]
                cnt_ring += 1
            return n - cnt_ring
        # print(count([3,1,2]))
        # print(count([7,9,10,5]))
        # print(count([4,3,1,2]))
        # return 
        q = [root]
        ans = 0
        while q:
            arr = []
            nq = []
            for node in q:
                arr.append(node.val)
                if node.left: nq.append(node.left)
                if node.right: nq.append(node.right)
            ans += count(arr)
            q = nq
        return ans


    """ 2472. 不重叠回文子字符串的最大数目 #hard 要从字符串s中找不重叠的长度至少为k的不重叠子串, 问最大数量. 复杂度: n 2e3
思路1: DP 复杂度 O(n^2)
    记 `f[i]` 表示用前i个字符可以得到的最大回文子串数目.
    递推: `f[i] = max{ f[i-1], max{f[j...i]}+1 }` 这里要求 s[j...i] 是回文串
        如何判断 s[j...i] 是回文串? 可以预处理得到
    细节: 在预处理回文的时候, 采用默认的 cache设置会 #超时? 
思路2: 除了预处理来判断子串是否回文, 还可以采用 #中心扩展法 只需要 O(1) 空间
    贪心: 若找到了长度为 k的回文串, 则不需要找 k+2 的了! 直接break即可
[灵神](https://leetcode.cn/problems/maximum-number-of-non-overlapping-palindrome-substrings/solution/zhong-xin-kuo-zhan-dppythonjavacgo-by-en-1yt1/)
关联: 0647. 回文子串; 0132. 分割回文串 II
"""
    def maxPalindromes(self, s: str, k: int) -> int:
        n = len(s)
        # 预处理: s[i,j] 是否回文
        # 不知道为啥默认的 cache会超时? 找到一个 magic number 1000
        # @lru_cache(10000)
        # def isPalindromic(i,j):
        #     if s[i]!=s[j]: return False
        #     return True if j-i<=2 else isPalindromic(i+1,j-1)
        isP = [[False]*n for _ in range(n)]
        for i in range(n-1, -1,-1):
            isP[i][i] = True
            for j in range(i+1,n):
                if s[i]==s[j]: isP[i][j] = isP[i+1][j-1] if j-i>2 else True
        # DP
        f = [0]*(n)
        for i in range(n):
            f[i] = f[i-1] if i>0 else 0
            for j in range(i-k+1, -1, -1):
                # if s[j:i]==s[j:i][::-1]:
                # if isPalindromic(j,i):
                if isP[j][i]:
                    f[i] = max(f[i], f[j-1]+1 if j>0 else 1)
                    # 剪枝!!
                    break
        return f[-1]
    def maxPalindromes(self, s: str, k: int) -> int:
        n = len(s)
        f = [0] * (n + 1)
        for i in range(2 * n - 1):
            l, r = i // 2, i // 2 + i % 2  # 中心扩展法
            f[l + 1] = max(f[l + 1], f[l])
            # 中心拓展
            while l >= 0 and r < n and s[l] == s[r]:
                if r - l + 1 >= k:
                    f[r + 1] = max(f[r + 1], f[l] + 1)
                    # 贪心思路, 可以直接break!!
                    break
                l -= 1
                r += 1
        return f[n]


    """ 0765. 情侣牵手 #hard #题型 有n对情侣坐成一排, 每次交换两个人, 问最少交换次数, 使得所有情侣相邻. 限制: n 30
思路1: #建图 + 计算 #联通分量
    显然, 调整后, 位置 2i,2i+1 的一定是一对情侣. 
    结论: 把座位看成两两一组 (节点), 根据建情侣之间的匹配关系可以构建节点之间的连接关系. 注意到一个大小为k的 #环, 可以通过交换 k-1 步完成匹配.
    因此, 问题等价于找环的数量 (联通分枝数量), 答案就是 n-cnt
    如何计算联通分枝数量? 可以采用 #并查集 也可以用 #BFS 
见 [官答](https://leetcode.cn/problems/couples-holding-hands/solution/qing-lu-qian-shou-by-leetcode-solution-bvzr/)
关联: 6235. 逐层排序二叉树所需的最少操作数目
"""
    def minSwapsCouples(self, row: List[int]) -> int:
        # 模拟交换? from copilot
        n = len(row)
        # 记录每个人的位置
        pos = [0]*n
        for i in range(n):
            pos[row[i]] = i
        ans = 0
        for i in range(0,n,2):
            if row[i]//2 == row[i+1]//2: continue
            # 找到另一半
            j = pos[row[i]//2*2 + (row[i]+1)%2]
            # 交换
            row[i+1], row[j] = row[j], row[i+1]
            pos[row[i+1]] = i+1
            pos[row[j]] = j
            ans += 1
        return ans
    def minSwapsCouples(self, row: List[int]) -> int:
        n = len(row)//2
        g = [set() for _ in range(n)]
        x2idx = [0]*len(row)
        for i,x in enumerate(row): x2idx[x]=i
        for i in range(len(row)):
            for x in row[2*i:2*i+2]:
                y = x^1
                posy = x2idx[y]; posx = x2idx[x]
                g[posx//2].add(posy//2)
                g[posy//2].add(posx//2)
        # 找图中联通分枝数量
        vis = [False]*n
        cnt = 0
        for i in range(n):
            if vis[i]: continue
            vis[i] = True
            q = [i]
            while q:
                u = q.pop()
                for v in g[u]:
                    if vis[v]: continue
                    vis[v] = True
                    q.append(v)
            cnt += 1
        return n-cnt
    
sol = Solution()
result = [
    # sol.subarrayLCM(nums = [3,6,2,7,1], k = 6),
    # sol.minimumOperations(None),
    # sol.maxPalindromes(s = "abaccdbbd", k = 3),
    # sol.maxPalindromes(s = "adbcda", k = 2),
    sol.minSwapsCouples(row = [0,2,1,3]),
    sol.minSwapsCouples(row = [3,2,0,1]),
]
for r in result:
    print(r)
