from easonsi.util.leetcode import *

# 求出所有数字的最小的真因子
LIMIT = 1_000_001
lm = [0] * LIMIT
for i in range(2, LIMIT):
    if lm[i] == 0:
        for j in range(i+i, LIMIT, i):
            if lm[j] == 0: lm[j] = i
""" 
https://leetcode.cn/contest/weekly-contest-420

T3 质因数再次被卡, 需要理解清楚题意!!
T4 听一遍 Manacher 讲解非常过瘾~

Easonsi @2023 """
class Solution:
    """ 3324. 出现在屏幕上的字符串序列 """
    def stringSequence(self, target: str) -> List[str]:
        ans = []
        ss = string.ascii_lowercase
        for i,x in enumerate(target):
            r = ord(x) - ord('a')
            for idx in range(r+1):
                ans.append(target[:i] + ss[idx])
        return ans
    
    """ 3325. 字符至少出现 K 次的子字符串 I #medium  计算相同字符至少出现 k 次的子字符串个数"""
    def numberOfSubstrings(self, s: str, k: int) -> int:
        cnt = Counter()
        r = 0; ans = 0
        for i,x in enumerate(s):
            cnt[x] += 1
            while max(cnt.values()) >= k:
                cnt[s[r]] -= 1
                r += 1
            ans += r
        return ans

    """ 3326. 使数组非递减的最少除法操作次数 #medium 给定一个数组, 要求经过最少操作变为非递减. 允许的操作: 将某一位置的元素除以其最大真因子 (不能是它本身!) 
限制: n 1e5; x 1e6
思路: 预处理 #质因数分解 + 逆序
    允许的操作, 等价于, 将一个数字变为其最小真因子! 因此可以做预处理
    对于本题, 显然逆序遍历!
[ling](https://leetcode.cn/problems/minimum-division-operations-to-make-array-non-decreasing/solutions/2957768/yu-chu-li-lpf-cong-you-dao-zuo-tan-xin-p-k3gt/)
    """
    def minOperations(self, nums: List[int]) -> int:
        ans = 0; pre = nums[-1]
        for i in range(len(nums)-2, -1, -1):
            x = nums[i]
            if x > pre:
                # cannot fulfill!
                if lm[x]==0 or lm[x]>pre: return -1
                pre = lm[x]
                ans += 1
            else:
                pre = x
        return ans
    
    """ 3327. 判断 DFS 字符串是否是回文串 #hard 给定一个字符树, 判断每一个节点的子树是否是回文串 #题型
限制: n 1e5
思路: 时间戳DFS #马拉车
    分解问题: 每个子树对应的字符串是整棵树的对应字符串的一个子串! 因此, 我们希望 O(1) 的判断一个字符串的子串是否是回文串! -- Manacher's algorithm
--- 下面讲马拉车. 对于查询 (l,r) 是否是回文的, 我们可以等价地判断其是否包含在 mid 包含的最大回文串范围内!  
    [bilibili](https://www.bilibili.com/video/BV1UcyYY4EnQ/) 讲解非常清晰!
    核心思想: 维护一个最靠右边的 box (boxM, boxR), 在暴力从每个位置i搜索其最长回文的时候, 复用之前的信息!
    (很容易困惑的) 为什么复杂度可以从 O(n^2) -> O(n)? 和滑动窗口的分析类似, 因为中其中box更新 (while循环) 最多只会发生 O(n) 次! 
[ling](https://leetcode.cn/problems/check-if-dfs-strings-are-palindromes/solutions/2957704/mo-ban-dfs-shi-jian-chuo-manacher-suan-f-ttu6/)
    """
    def findAnswer(self, parent: List[int], s: str) -> List[bool]:
        n = len(parent)
        g = [[] for _ in range(n)]
        for i in range(1, n):
            p = parent[i]
            # 由于 i 是递增的，所以 g[p] 必然是有序的，下面无需排序
            g[p].append(i)

        # dfsStr 是后序遍历整棵树得到的字符串
        dfsStr = [''] * n
        # nodes[i] 表示子树 i 的后序遍历的开始时间戳和结束时间戳+1（左闭右开区间）
        nodes = [[0, 0] for _ in range(n)]
        time = 0

        def dfs(x: int) -> None:
            nonlocal time
            nodes[x][0] = time
            for y in g[x]:
                dfs(y)
            dfsStr[time] = s[x]  # 后序遍历
            time += 1
            nodes[x][1] = time
        dfs(0)

        # Manacher 模板
        # 将 dfsStr 改造为 t，这样就不需要讨论 n 的奇偶性，因为新串 t 的每个回文子串都是奇回文串（都有回文中心）
        # dfsStr 和 t 的下标转换关系：
        # (dfsStr_i+1)*2 = ti
        # ti/2-1 = dfsStr_i
        # ti 为偶数，对应奇回文串（从 2 开始）
        # ti 为奇数，对应偶回文串（从 3 开始）
        t = '#'.join(['^'] + dfsStr + ['$'])

        # 定义一个奇回文串的回文半径=(长度+1)/2，即保留回文中心，去掉一侧后的剩余字符串的长度
        # halfLen[i] 表示在 t 上的以 t[i] 为回文中心的最长回文子串的回文半径
        # 即 [i-halfLen[i]+1,i+halfLen[i]-1] 是 t 上的一个回文子串
        halfLen = [0] * (len(t) - 2)
        halfLen[1] = 1
        # boxR 表示当前右边界下标最大的回文子串的右边界下标+1
        # boxM 为该回文子串的中心位置，二者的关系为 r=mid+halfLen[mid]
        boxM = boxR = 0
        for i in range(2, len(halfLen)):
            hl = 1
            if i < boxR:
                # 记 i 关于 boxM 的对称位置 i'=boxM*2-i
                # 若以 i' 为中心的最长回文子串范围超出了以 boxM 为中心的回文串的范围（即 i+halfLen[i'] >= boxR）
                # 则 halfLen[i] 应先初始化为已知的回文半径 boxR-i，然后再继续暴力匹配
                # 否则 halfLen[i] 与 halfLen[i'] 相等
                hl = min(halfLen[boxM * 2 - i], boxR - i)
            # 暴力扩展
            # 算法的复杂度取决于这部分执行的次数
            # 由于扩展之后 boxR 必然会更新（右移），且扩展的的次数就是 boxR 右移的次数
            # 因此算法的复杂度 = O(len(t)) = O(n)
            while t[i - hl] == t[i + hl]:
                hl += 1
                boxM, boxR = i, i + hl
            halfLen[i] = hl

        # t 中回文子串的长度为 hl*2-1
        # 由于其中 # 的数量总是比字母的数量多 1
        # 因此其在 dfsStr 中对应的回文子串的长度为 hl-1
        # 这一结论可用在 isPalindrome 中

        # 判断左闭右开区间 [l,r) 是否为回文串  0<=l<r<=n
        # 根据下标转换关系得到 dfsStr 的 [l,r) 子串在 t 中对应的回文中心下标为 l+r+1
        # 需要满足 halfLen[l + r + 1] - 1 >= r - l，即 halfLen[l + r + 1] > r - l
        def isPalindrome(l: int, r: int) -> bool:
            return halfLen[l + r + 1] > r - l

        return [isPalindrome(l, r) for l, r in nodes]

sol = Solution()
result = [
    # sol.stringSequence(target = "abc"),
    # sol.numberOfSubstrings( s = "abacb", k = 2),
    # sol.numberOfSubstrings(s = "abcde", k = 1),
    sol.minOperations(nums = [25,7]),
    sol.minOperations(nums = [7,7,6]),
    sol.minOperations(nums = [1,1,1,1]),
    sol.minOperations([105,11]),
]
for r in result:
    print(r)
