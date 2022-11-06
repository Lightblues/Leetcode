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
https://leetcode.cn/contest/weekly-contest-150
T4做不来... Python的字符串也太作弊了...

@2022 """
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    """ 1160. 拼写单词 """
    def countCharacters(self, words: List[str], chars: str) -> int:
        chars_cnt = collections.Counter(chars)
        ans = 0
        for word in words:
            word_cnt = collections.Counter(word)
            for c in word_cnt:
                if chars_cnt[c] < word_cnt[c]:
                    break
            else:
                ans += len(word)
        return ans
    """ 1161. 最大层内元素和 """
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        sum = []
        def dfs(node: TreeNode, level: int) -> None:
            if level == len(sum):
                sum.append(node.val)
            else:
                sum[level] += node.val
            if node.left:
                dfs(node.left, level + 1)
            if node.right:
                dfs(node.right, level + 1)
        dfs(root, 0)
        return sum.index(max(sum)) + 1  # 层号从 1 开始

    """ 1162. 地图分析 #medium 对于一个 0/1 grid表示海洋/陆地. 问所有的海洋节点中, 距离陆地的最远距离. 限制 m,n 100
思路1: #BFS
其他思路: 多源最短路; DP
[官答](https://leetcode.cn/problems/as-far-from-land-as-possible/solution/di-tu-fen-xi-by-leetcode-solution/)
 """
    def maxDistance(self, grid: List[List[int]]) -> int:
        n = len(grid)
        q = []
        seen = set()
        for i,j in product(range(n), range(n)):
            if grid[i][j]==1:
                q.append((i,j)); seen.add((i,j))
        # 全是陆地/海洋
        if len(q)==0 or len(q)==n*n: return -1
        dist = 0
        dirs = [(0,-1), (0,1), (1,0), (-1,0)]
        while q:
            nq = []
            for x,y in q:
                for dx,dy in dirs:
                    nx,ny = x+dx,y+dy
                    if not (0<=nx<n and 0<=ny<n): continue
                    if (nx,ny) in seen: continue
                    seen.add((nx,ny))
                    nq.append((nx,ny))
            if len(nq)==0: break
            dist += 1
            q = nq
        return dist
    
    """ 1163. 按字典序排在最后的子串 #hard 对于给定s的所有子串, 找到 #字典序 最大的那个 限制: n 5e4
提示: 答案肯定是 s[mxidx:] 并且 mxidx位置的字符是s中的最大字符. 
思路0:
    对于 zzzzz 这种情况如何处理? 
    假设我们记录的当前最好为 left, 则我们遍历右指针 right.
        若遇到了更大的字符, 则直接更新right
        若遇到了相同的最大字符, 比较 s[right], s[right]+1.... 注意到, 假设比较到 idx 结束, 我们可以直接从 idx+1 开始!!
todo...
https://leetcode.cn/problems/last-substring-in-lexicographical-order/
"""
    def lastSubstring(self, s: str) -> str:
        # 思路0, 错误的...
        mxChar = chr(ord('a')-1)
        left = -1
        right = 0
        n = len(s)
        while right<n:
            if s[right]>mxChar:
                mxChar = s[right]
                left = right
            elif s[right]==mxChar:
                d = 1
                while right+d<n and s[left+d]==s[right+d]:
                    d += 1
                if right+d==n: break
                if s[right+d]>s[left+d]:
                    left = right
                right += d
            # 
            right += 1
        return s[left:]

    def lastSubstring(self, s):
        """ from https://zhuanlan.zhihu.com/p/379043216
实际的复杂度应该也是 n^2, 例子 cacaca....cb
"""
        res = 0
        now = 1
        l = 0   # 相同前缀的长度
        while now + l < len(s):
            # 遇到了更大的字符
            if s[res] < s[now + l]:
                res = now + l
                now = res + 1
                l = 0
            elif s[res + l] == s[now + l]:
                l += 1
            elif s[res + l] < s[now + l]:
                res = now
                now += 1
                l = 0
            else:
                # now 无法更新 res!! 
                now += l + 1
                l = 0
        return s[res:]
    
    def lastSubstring(self, s: str) -> str:
        # Python 暴力字符串比较居然能过... 而且挺快的
        mx = ""
        for i in range(len(s)):
            mx = max(mx, s[i:])
        return mx

sol = Solution()
result = [
    # sol.maxDistance(grid = [[1,0,0],[0,0,0],[0,0,0]]),
    sol.lastSubstring("leetcode"),
    sol.lastSubstring('abab'),
    sol.lastSubstring('cacacb'),
    sol.lastSubstring("babcbd"),
    sol.lastSubstring('ca' * 10000 + 'cb'),
]
for r in result:
    print(r)
