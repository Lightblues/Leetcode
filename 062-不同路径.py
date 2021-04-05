"""
一个机器人位于一个 m x n 网格的左上角 （起始点在下图中标记为 “Start” ）。

机器人每次只能向下或者向右移动一步。机器人试图达到网格的右下角（在下图中标记为 “Finish” ）。

问总共有多少条不同的路径？

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/unique-paths
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。
"""
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        m, n = min(m, n), max(m, n)
        l = [1]*n
        for i in range(m-1):
            for j in range(1, n):
                l[j] += l[j-1]
        return l[-1]

print(Solution().uniquePaths(3,7))
