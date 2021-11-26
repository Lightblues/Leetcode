from typing import List
import bisect

""" 2078. 两栋颜色不同且距离最远的房子
给一个数字列表, 计算其中不同的两个数字间隔最大值

输入：colors = [1,8,3,8,3]
输出：4
解释：上图中，颜色 1 标识成蓝色，颜色 8 标识成黄色，颜色 3 标识成绿色。
两栋颜色不同且距离最远的房子是房子 0 和房子 4 。
房子 0 的颜色是颜色 1 ，房子 4 的颜色是颜色 3 。两栋房子之间的距离是 abs(0 - 4) = 4 。

下面的暴力求解也可以通过. 实际上,左右各遇到一个和另一端颜色不同的即可输出, 参见 go 实现. 
"""
class Solution:
    def maxDistance(self, colors: List[int]) -> int:
        ans = 0 
        for i, x in enumerate(colors): 
            if x != colors[0]: ans = max(ans, i)
            if x != colors[-1]: ans = max(ans, len(colors)-1-i)
        return ans 


""" 2079. 给植物浇水
输入：plants = [2,2,3,3], capacity = 5
输出：14
解释：从河边开始，此时水罐是装满的：
- 走到植物 0 (1 步) ，浇水。水罐中还有 3 单位的水。
- 走到植物 1 (1 步) ，浇水。水罐中还有 1 单位的水。
- 由于不能完全浇灌植物 2 ，回到河边取水 (2 步)。
- 走到植物 2 (3 步) ，浇水。水罐中还有 2 单位的水。
- 由于不能完全浇灌植物 3 ，回到河边取水 (3 步)。
- 走到植物 3 (4 步) ，浇水。
需要的步数是 = 1 + 1 + 2 + 3 + 3 + 4 = 14 。

输入：plants = [1,1,1,4,2,3], capacity = 4
输出：30
解释：从河边开始，此时水罐是装满的：
- 走到植物 0，1，2 (3 步) ，浇水。回到河边取水 (3 步)。
- 走到植物 3 (4 步) ，浇水。回到河边取水 (4 步)。
- 走到植物 4 (5 步) ，浇水。回到河边取水 (5 步)。
- 走到植物 5 (6 步) ，浇水。
需要的步数是 = 3 + 3 + 4 + 4 + 5 + 5 + 6 = 30 。

模拟行走, 累计即可. 
"""
class Solution2079:
    def wateringPlants(self, plants: List[int], capacity: int) -> int:
        result = 0; remains = capacity
        for i in range(len(plants)):
            if remains >= plants[i]:
                result +=1 
                remains -= plants[i]
            else:
                result += 2*i+1
                remains = capacity - plants[i]
        return result

""" 2080. 区间内查询数字的频率
请你实现 RangeFreqQuery 类：
RangeFreqQuery(int[] arr) 用下标从 0 开始的整数数组 arr 构造一个类的实例。
int query(int left, int right, int value) 返回子数组 arr[left...right] 中 value 的 频率 。

输入：
["RangeFreqQuery", "query", "query"]
[[[12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]], [1, 2, 4], [0, 11, 33]]
输出：
[null, 1, 2]
解释：
RangeFreqQuery rangeFreqQuery = new RangeFreqQuery([12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]);
rangeFreqQuery.query(1, 2, 4); // 返回 1 。4 在子数组 [33, 4] 中出现 1 次。
rangeFreqQuery.query(0, 11, 33); // 返回 2 。33 在整个子数组中出现 2 次。

主要应对的查询情况, 为了优化较多的查询, 建立了对应数字的列表, 从而查询时候可以用二分查找. 
"""
class RangeFreqQuery:
    def __init__(self, arr: List[int]):
        # self.arr = arr
        from collections import defaultdict
        self.numList = defaultdict(list)
        for i,n in enumerate(arr):
            self.numList[n].append(i)

    def query(self, left: int, right: int, value: int) -> int:
        # count = 0
        # for i in self.arr[left: right+1]:
        #     if value == i:
        #         count += 1
        # return count
        # s = [i for i in self.arr[left:right+1] if i==value]
        # return len(s)
        targetList = self.numList[value]
        # 二分查找 left right
        i = bisect.bisect(targetList, left - 1)
        j = bisect.bisect(targetList, right)
        return j-i
    
    # TODO 实现二分查找
    # def bisearch(nums: List, target: int, bigger: bool):
    #     left, right = 0, len(nums)
    #     while True:
    #         index = (left+right)//2

# Your RangeFreqQuery object will be instantiated and called as such:
# obj = RangeFreqQuery(arr)
# param_1 = obj.query(left,right,value)




""" 2081. k 镜像数字的和
一个 k 镜像数字 指的是一个在十进制和 k 进制下从前往后读和从后往前读都一样的 没有前导 0 的 正 整数。

比方说，9 是一个 2 镜像数字。9 在十进制下为 9 ，二进制下为 1001 ，两者从前往后读和从后往前读都一样。
相反地，4 不是一个 2 镜像数字。4 在二进制下为 100 ，从前往后和从后往前读不相同。
给你进制 k 和一个数字 n ，请你返回 k 镜像数字中 最小 的 n 个数 之和 。

 """
class Solution:
    def kMirror(self, k: int, n: int) -> int:
        int(45, base=3)