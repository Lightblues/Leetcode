from typing import List, Optional
import collections
import math
import bisect
import heapq

from structures import ListNode

""" 
https://leetcode-cn.com/contest/biweekly-contest-71
@20220223 补 """
class Solution:
    """ 2129. 将标题首字母大写 """
    def capitalizeTitle(self, title: str) -> str:
        words = title.split()
        for i,word in enumerate(words):
            if len(word) < 3:
                words[i] = word.lower()
            else:
                words[i] = word[0].upper() + word[1:].lower()
        return " ".join(words)

    """ 2130. 链表最大孪生和 """
    def pairSum(self, head: Optional[ListNode]) -> int:
        numbers = []
        while head:
            numbers.append(head.val)
            head = head.next
        return max([i+j for i,j in zip(numbers, reversed(numbers))])

    """ 2131. 连接两字母单词得到的最长回文串
给一组长度为2的字符串, 将他们拼接, 形成最大的回文串

考虑 1. aa 的形式, 若数量为奇数, 只能放在中间, 若为偶数, 可以两侧对应位置放置; 
2. ab + ba 的形式, 左右对称放置
 """
    def longestPalindrome(self, words: List[str]) -> int:
        diffWords = [w for w in words if w[0]!=w[1]]
        sameWords = [w for w in words if w[0]==w[1]]
        result = 0

        # aa 的形式
        sameDict = collections.Counter(sameWords)
        # result += max(list(sameDict.values()) + [0]) * 2
        flag = False
        for k,v in sameDict.items():
            if v%2!=0:
                flag = True
            result += v//2 * 2 * 2
        if flag:
            result += 2

        # ab + ba 的形式
        diffDict = collections.Counter(diffWords)
        tmp = 0
        for k,v in diffDict.items():
            if k[::-1] in diffDict:
                tmp += min(v, diffDict[k[::-1]])
        return result + tmp * 2


    """ 2132. 用邮票贴满网格图
给一个矩阵grid, 其中数字为1的位置不能使用; 要求用 stampHeight x stampWidth 的邮票去贴满所有空的位置, 返回能否实现. 矩阵不可旋转, 可以重叠.

输入：grid = [[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]], stampHeight = 4, stampWidth = 3
输出：true
解释：我们放入两个有重叠部分的邮票（图中标号为 1 和 2），它们能覆盖所有与空格子。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/stamping-the-grid
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。


 """
    """ from 评论区, hhh 用卷积来做 —— 虽然超时了 """
    def possibleToStamp(self, grid: List[List[int]], stampHeight: int, stampWidth: int) -> bool:
        import numpy as np
        from scipy.signal import convolve2d

        h,w=stampHeight,stampWidth
        g=np.array(grid)
        b=np.ones((h,w))
        # x统计以这个点为左上角的矩形能覆盖多少个1，如果为0的位置说明这个矩形能铺上
        x=convolve2d(g,b,fillvalue=1)
        # y统计能覆盖到这个位置的矩形有多少个是铺不下去的，如果为h*w说明这个点没有任何矩形能覆盖得到
        y=convolve2d(x>0,b,mode='valid')
        return not (y==(h*w))[g==0].any()

    """ from [here](https://leetcode-cn.com/problems/stamping-the-grid/solution/wu-nao-zuo-fa-er-wei-qian-zhui-he-er-wei-zwiu/)
用了 二维差分/前缀和矩阵

首先, 利用二维前缀和矩阵可以快速计算 (x1,y1), (x2,y2) 区域内的元素和.
在本题中, 计算grid的前缀和矩阵, 即可以用来判断该区域内是否有1.
     """
    def possibleToStamp(self, grid: List[List[int]], stampHeight: int, stampWidth: int) -> bool:
        # 这里的代码太赞了!!
        m, n = len(grid), len(grid[0])
        sum = [[0] * (n + 1) for _ in range(m + 1)]
        diff = [[0] * (n + 1) for _ in range(m + 1)]
        for i, row in enumerate(grid):
            for j, v in enumerate(row):  # grid 的二维前缀和
                sum[i + 1][j + 1] = sum[i + 1][j] + sum[i][j + 1] - sum[i][j] + v

        for i, row in enumerate(grid):
            for j, v in enumerate(row):
                if v == 0:
                    x, y = i + stampHeight, j + stampWidth  # 注意这是矩形右下角横纵坐标都 +1 后的位置
                    if x <= m and y <= n and sum[x][y] - sum[x][j] - sum[i][y] + sum[i][j] == 0:
                        diff[i][j] += 1
                        diff[i][y] -= 1
                        diff[x][j] -= 1
                        diff[x][y] += 1  # 更新二维差分

        # 还原二维差分矩阵对应的计数矩阵，这里用滚动数组实现
        cnt, pre = [0] * (n + 1), [0] * (n + 1)
        for i, row in enumerate(grid):
            for j, v in enumerate(row):
                cnt[j + 1] = cnt[j] + pre[j + 1] - pre[j] + diff[i][j]
                if cnt[j + 1] == 0 and v == 0:
                    return False
            cnt, pre = pre, cnt
        return True


sol = Solution()
result = [
    # sol.capitalizeTitle("capiTalIze tHe titLe"),
    # sol.longestPalindrome(words = ["ab","ty","yt","lc","cl","ab"]),
    # sol.longestPalindrome(words = ["lc","cl","gg"]),
    # sol.longestPalindrome(["dd","aa","bb","dd","aa","dd","bb","dd","aa","cc","bb","cc","dd","cc"]),
    sol.possibleToStamp(grid = [[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]], stampHeight = 4, stampWidth = 3),
    sol.possibleToStamp(grid = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]], stampHeight = 2, stampWidth = 2),
]
for r in result:
    print(r)