from typing import List, Optional
import collections
import math
import bisect
import heapq

from structures import ListNode

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220306 补 """
class Solution:
    """ 6024. 数组中紧跟 key 之后出现最频繁的数字 """
    def mostFrequent(self, nums: List[int], key: int) -> int:
        cnt = collections.Counter()
        for i in range(len(nums)-1):
            if nums[i] == key:
                cnt[nums[i+1]] += 1
        return cnt.most_common(1)[0][0]

    """ 5217. 将杂乱无章的数字排序
mapping 对应了10进制中每一位的映射, 要求根据映射后的数字对于原数字排序.

输入：mapping = [8,9,4,0,2,1,3,5,7,6], nums = [991,338,38]
输出：[338,38,991]
解释：
将数字 991 按照如下规则映射：
1. mapping[9] = 6 ，所有数位 9 都会变成 6 。
2. mapping[1] = 9 ，所有数位 1 都会变成 8 。
所以，991 映射的值为 669 。
338 映射为 007 ，去掉前导 0 后得到 7 。
38 映射为 07 ，去掉前导 0 后得到 7 。
由于 338 和 38 映射后的值相同，所以它们的前后顺序保留原数组中的相对位置关系，338 在 38 的前面。
所以，排序后的数组为 [338,38,991] 。
 """
    def sortJumbled(self, mapping: List[int], nums: List[int]) -> List[int]:
        map = {
            str(i): str(mapping[i]) for i in range(len(mapping))
        }
        mappedNums = [int("".join(map[i] for i in str(n))) for n in nums]
        return [i[1] for i in sorted(zip(mappedNums, nums), key=lambda x: x[0])] # 注意, 对于变换后的相同的结果, 保留原来的顺序


    """ 5300. 有向无环图中一个节点的所有祖先
给一个 DAG, 要求返回每一个节点的所有祖先节点 (排序)

输入：n = 8, edgeList = [[0,3],[0,4],[1,3],[2,4],[2,7],[3,5],[3,6],[3,7],[4,6]]
输出：[[],[],[],[0,1],[0,2],[0,1,3],[0,1,2,3,4],[0,1,2,3]]
解释：
上图为输入所对应的图。
- 节点 0 ，1 和 2 没有任何祖先。
- 节点 3 有 2 个祖先 0 和 1 。
- 节点 4 有 2 个祖先 0 和 2 。
- 节点 5 有 3 个祖先 0 ，1 和 3 。
- 节点 6 有 5 个祖先 0 ，1 ，2 ，3 和 4 。
- 节点 7 有 4 个祖先 0 ，1 ，2 和 3 。

思路一: 可以通过 DFS 找到节点的所有孩子, 在 逆图 上做即可
 """
    def getAncestors(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        # construct graph
        g = [[] for _ in range(n)]
        reversedG = [[] for _ in range(n)]
        for u, v in edges:
            g[u].append(v)
            reversedG[v].append(u)
        
        # dfs
        visited = [False] * n
        res = [[] for _ in range(n)]
        def dfs(u):
            if visited[u]:
                return res[u]
            descendants = set(reversedG[u])
            for v in reversedG[u]:
                descendants = descendants.union(dfs(v))
            # descendants.sort()
            res[u] = sorted(list(descendants))
            visited[u] = True
            return descendants

        starts = [n for n in range(len(g)) if not g[n]]
        for s in starts:
            dfs(s)
        return res

    """ 2193. 得到回文串的最少操作次数 #hard #贪心
给一个字符串, 仅有的操作为交换相邻两个字符, 要求转为回文串的最小交换次数

输入：s = "letelt"
输出：2
解释：
通过 2 次操作从 s 能得到回文串 "lettel" 。
其中一种方法是："letelt" -> "letetl" -> "lettel" 。
其他回文串比方说 "tleelt" 也可以通过 2 次操作得到。
可以证明少于 2 次操作，无法得到回文串。


思路一: 两次贪心 [here](https://leetcode-cn.com/problems/minimum-number-of-moves-to-make-palindrome/solution/de-dao-hui-wen-chuan-de-zui-shao-cao-zuo-nnis/)
首先需要理解: 逆序数等于一个序列要变成**升序排列**所需要的**相邻元素**交换的**最小**次数。 [here](https://leetcode-cn.com/problems/shu-zu-zhong-de-ni-xu-dui-lcof/solution/ni-xu-shu-yu-pai-xu-de-nei-zai-lian-xi-wu-dai-ma-b/)

- 先考虑偶数长度的情况: 可知, 对于 2m 个字符ch, 其中的前m个字符, 也一定在最终的回文串的前一半中, 并且它们之间的相对位置保持不变.
    - 因此, 分解为两步: (1) 组间交换. 先划分左右两个子串. 由于不改变相对位置, 其实我们就知道了原本字符串的每一个位置的元素, 在分为好左右组的字符串中的位置.
    - (2) 组内交换, 也即使得左右子串转换为对称. 由于没有相对位置变化, 因此我们固定左子串, 则对于右子串中每一个字符最终的位置其实我们就确定了 —— 等于求逆序数.
- 而对于奇数情况, 简单令右子串多一个元素, 然后在左子串后加上那个中心的(奇数)字符, 则约束了右串排序中将其移动到中间.

 """
    def minMovesToMakePalindrome0(self, s: str) -> int:
        freq = collections.Counter(s)

        ans = 0
        left, right = collections.defaultdict(list), collections.defaultdict(list) # 记录每一个字符, 出现在左 (右) 子串中的位置
        lcnt, rcnt = 0, 0

        # 1. 统计「组间交换」的操作次数
        for i, c in enumerate(s):
            if len(left[c])+1 <= freq[c]//2: # 若为奇数, 则令右串多一个字符
                lcnt += 1
                left[c].append(lcnt) # 该字符在左子串中的idx, 从1开始 (因为是一个「排序」)
                ans += (i-lcnt+1) # 需要相邻交换的次数
            else:
                rcnt += 1
                right[c].append(rcnt)
        # 如果长度为奇数，需要在前一半末尾添加一个中心字母
        if len(s)%2 == 1:
            for c, occ in freq.items():
                if occ%2 == 1:
                    lcnt += 1
                    left[c].append(lcnt)
        
        # 2. 统计「组内交换」的操作次数
        # 计算 right子串要交换为 left子串, 原本各个字符对应到最终应该在的index
        perm = [0] * ((len(s)+1)//2)
        # (1)要使得right等于left, 直接将原本的序号放在对应位置上即可
        # for c in right:
        #     for x,y in zip(left[c], right[c]):
        #         perm[y-1] = x
        # (2)要使得right的逆序等于left, 则在逆序排列中, 原本的位置应该 [::-1] 交错对应
        for c in right:
            for x,y in zip(left[c], right[c][::-1]):
                perm[y-1] = x
        perm = perm[::-1]


        # 计算逆序对，统计「组内交换」的操作次数
        # 暴力法
        def get_brute_force() -> int:
            n = len(perm)
            cnt = 0
            for i in range(n):
                for j in range(i+1, n):
                    if perm[i] > perm[j]:
                        cnt += 1
            return cnt
        return ans + get_brute_force()
    
    """ 思路二: 贪心 [here](https://leetcode-cn.com/problems/minimum-number-of-moves-to-make-palindrome/solution/tan-xin-zheng-ming-geng-da-shu-ju-fan-we-h57i/)
其实在上面的思路中, 我们已经知道了最终的回文串是怎样的 —— 左子串由所有字符的前一半出现位置决定, 右子串对称.
因此, 更为贪心的策略是: 每次保留左侧的第一个字符, 将最右边的该字符移动到右侧, 这样就完成了匹配.
对于奇数的情况, 只需要将其移动到中心即可.
 """
    def minMovesToMakePalindrome(self, s: str) -> int:
        ans = 0
        n = len(s)
        # 维持左右对称的指针
        l,r = 0, n-1
        recordedL = 0
        while l<r:
            # 从右往左搜索该字符
            k = r
            flag = False # 记录是否为奇数的中心字符
            while k>l:
                if s[k] == s[l]:
                    # 模拟交换
                    ans += r-k
                    s = s[:k] + s[k+1:r+1] + s[k] + s[r+1:]
                    flag = True
                    break
                k -= 1
            
            # 注意最后的中心一定会在 left 指针上
            if not flag: # 奇数
                ans += n//2 - l
                # 此时, 不需要模拟! 应该是最后移动到中心
                # s = s[:l] + s[l+1:n//2+1] + s[l] + s[n//2+1:]
                recordedL = l
                l += 1 # 需要跳过该指针!!
            else:
                l, r = l+1, r-1

        # 若还要输出s, 可以用一个变量 recordedL 记录位置
        if len(s)%2 == 1:
            s = s[:recordedL] + s[recordedL+1:n//2+1] + s[recordedL] + s[n//2+1:]
        print(s)
        return ans


sol = Solution()
result = [
    # sol.mostFrequent(nums = [1,100,200,1,100], key = 1),
    # sol.sortJumbled(mapping = [8,9,4,0,2,1,3,5,7,6], nums = [991,338,38]),
    # sol.getAncestors(n = 8, edges = [[0,3],[0,4],[1,3],[2,4],[2,7],[3,5],[3,6],[3,7],[4,6]]),

    sol.minMovesToMakePalindrome("aabb"),
    sol.minMovesToMakePalindrome(s = "letelt"),
    sol.minMovesToMakePalindrome("skwhhaaunskegmdtutlgtteunmuuludii") # 163
]
for r in result:
    print(r)