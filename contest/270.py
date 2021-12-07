from typing import List, Optional
import collections
from collections import defaultdict, Counter

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """ 2094. 找出 3 位偶数
给你一个整数数组 digits ，其中每个元素是一个数字（0 - 9）。数组中可能存在重复元素。
你需要找出 所有 满足下述条件且 互不相同 的整数：
- 该整数由 digits 中的三个元素按 任意 顺序 依次连接 组成。
- 该整数不含 前导零
- 该整数是一个 偶数
例如，给定的 digits 是 [1, 2, 3] ，整数 132 和 312 满足上面列出的全部条件。
将找出的所有互不相同的整数按 递增顺序 排列，并以数组形式返回。

输入：digits = [2,1,3,0]
输出：[102,120,130,132,210,230,302,310,312,320]
解释：
所有满足题目条件的整数都在输出数组中列出。 
注意，答案数组中不含有 奇数 或带 前导零 的整数。

简单题, 直接暴力遍历即可
 """
    def findEvenNumbers(self, digits: List[int]) -> List[int]:
        results = set()
        n = len(digits)
        for i in range(n):
            if digits[i]==0:
                continue
            for j in range(n):
                for k in range(n):
                    if i==j or j==k or k==i or digits[k]%2==1:
                        continue
                    num = 100*digits[i] + 10*digits[j] + digits[k]
                    results.add(num)
        return sorted(results)


        # digitsMap = sorted(collections.Counter(digits).items())
        # results = []
        # tmp = []
        # def dfs(remain, index, used=0):
        #     if remain == 0 and not tmp[-1]%2:
        #         results.append(int(''.join([str(i) for i in tmp])))
        #     for digit,c in digitsMap[index:]:
        #         for _ in range(c-used):
        #             tmp.append(digit)
        #             dfs(remain-1, index, used-1)
        #     return
        # dfs(3, 0)

        # digits = sorted(digits)
        # global tmp
        # tmp = 0
        # results = []
        # def dfs(remain, index):
        #     global tmp
        #     if remain==0 :
        #         if tmp%2==0:
        #             results.append(tmp)
        #         return
        #     for i in range(index, len(digits)):
        #         if tmp==0 and digits[i]==0:
        #             continue
        #         if i>0 and digits[i]==digits[i-1]: 
        #             continue
        #         tmp = 10*tmp+digits[i]
        #         dfs(remain-1, i+1)
        #         tmp = tmp//10
        # dfs(3, 0)
        # return results

    def deleteMiddle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        first = ListNode(0, head)
        p1, p2 = first, first
        while p1:
            p1 = p1.next
            if p1 and p1.next:
                p2 = p2.next
                p1 = p1.next
        if p2.next and p2.next.next:
            p2.next = p2.next.next
        else:
            p2.next = None
        return first.next

    """ 2096. 从二叉树一个节点到另一个节点每一步的方向
给你一棵 二叉树 的根节点 root ，这棵二叉树总共有 n 个节点。每个节点的值为 1 到 n 中的一个整数，且互不相同。给你一个整数 startValue ，表示起点节点 s 的值，和另一个不同的整数 destValue ，表示终点节点 t 的值。
请找到从节点 s 到节点 t 的 最短路径 ，并以字符串的形式返回每一步的方向。每一步用 大写 字母 'L' ，'R' 和 'U' 分别表示一种方向：
'L' 表示从一个节点前往它的 左孩子 节点。
'R' 表示从一个节点前往它的 右孩子 节点。
'U' 表示从一个节点前往它的 父 节点。
请你返回从 s 到 t 最短路径 每一步的方向。

输入：root = [5,1,2,3,null,6,4], startValue = 3, destValue = 6
输出："UURL"
解释：最短路径为：3 → 1 → 5 → 2 → 6 。 """
    def getDirections(self, root: Optional[TreeNode], startValue: int, destValue: int) -> str:
        path = []
        pathRecord = [None, None]
        def dfs(node):
            if node == None:
                return
            if node.val == startValue:
                pathRecord[0] = path[:]
            elif node.val == destValue:
                pathRecord[1] = path[:]
            if node.left:
                path.append("L")
                dfs(node.left)
                path.pop()
            if node.right:
                path.append("R")
                dfs(node.right)
                path.pop()
        dfs(root)
        pathStart, pathDest = pathRecord
        i = 0
        while i<min(len(pathStart),len(pathDest)) and pathStart[i]==pathDest[i]:
            i+=1
        pathStart, pathDest = pathStart[i:], pathDest[i:]
        return "".join(["U"] * len(pathStart) + pathDest)

    """ 2097. 合法重新排列数对
给你一个下标从 0 开始的二维整数数组 pairs ，其中 pairs[i] = [starti, endi] 。如果 pairs 的一个重新排列，满足对每一个下标 i （ 1 <= i < pairs.length ）都有 endi-1 == starti ，那么我们就认为这个重新排列是 pairs 的一个 合法重新排列 。
请你返回 任意一个 pairs 的合法重新排列。
注意：数据保证至少存在一个 pairs 的合法重新排列。 

输入：pairs = [[5,1],[4,5],[11,9],[9,4]]
输出：[[11,9],[9,4],[4,5],[5,1]]
解释：
输出的是一个合法重新排列，因为每一个 endi-1 都等于 starti 。"""
    def validArrangement(self, pairs: List[List[int]]) -> List[List[int]]:
        # startEnd = collections.defaultdict(lambda: [[], []])
        # for i,(s, e) in enumerate(pairs):
        #     startEnd[s][0].append(i)
        #     startEnd[e][1].append(i)
        # startValue, endValue = None, None
        # for value, (starts, ends) in startEnd.items():
        #     if len(starts) > len(ends):
        #         startValue = value
        #     if len(starts) < len(ends):
        #         endValue = value
        # result = []
        # if startValue:
        #     startIndex = startEnd[startValue][0][0]
        # else:
        #     startIndex = 0
        # startEnd[pairs[startIndex][0]][0].remove(startIndex)
        # for i in range(len(pairs)):
        #     result.append(pairs[startIndex])
        #     eValue = pairs[startIndex][1]
        #     if startEnd[eValue][0]:
        #         startIndex = startEnd[eValue][0].pop()
        
        edges = defaultdict(list)
        outDegree, inDegree = Counter(), Counter()
        for u,v in pairs:
            edges[u].append(v)
            outDegree[u] += 1
            inDegree[v] += 1
        start = pairs[0][0]
        for u in outDegree:
            if outDegree[u] > inDegree[u]:
                start = u
                break
        result = []
        # 深度优先搜索（Hierholzer 算法）求解欧拉通路
        def dfs(u):
            while edges[u]:
                v = edges[u].pop()
                dfs(v)
                result.append([u,v])
        dfs(start)
        return result[::-1]

sol = Solution()
print(sol.findEvenNumbers([2,2,8,8,2]))
# print(sol.validArrangement([[5,1],[4,5],[11,9],[9,4]]))
# print(sol.validArrangement([[8,5],[8,7],[0,8],[0,5],[7,0],[5,0],[0,7],[8,0],[7,8]]))