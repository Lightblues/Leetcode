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
https://www.bilibili.com/video/BV1mY411D7f6/

0046. 全排列 https://leetcode.cn/problems/permutations/solutions/2079585/hui-su-bu-hui-xie-tao-lu-zai-ci-jing-que-6hrh/
0051. N 皇后 https://leetcode.cn/problems/n-queens/solutions/2079586/hui-su-tao-lu-miao-sha-nhuang-hou-shi-pi-mljv/
0052. N皇后 II #hard 相较于 0052, 只需要返回解的数量


Easonsi @2023 """
class Solution:
    """ 0046. 全排列 #medium 对于不含重复数字的数组, 得到其全排列 限制: n 6
思路1: #回溯
    1.1 DFS 形式为 dfs(i, s), 搜索在全局path的情况下, 第i个位置可以选集合s中的元素
    1.2 形式为 dfs(i), 另外用一个 on_path 数组记录元素是否已经用到了 path中
"""
    def permute(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        path = [0]*n
        ans = []
        def dfs(i, s):
            # 1.1 DFS 形式为 dfs(i, s), 搜索在全局path的情况下, 第i个位置可以选集合s中的元素
            if i==n:
                ans.append(path[:])
                return
            for x in s:
                path[i] = x
                dfs(i+1,s-{x})
        dfs(0,set(nums))
        return ans
    def permute(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        ans = []
        path = [0] * n
        on_path = [False] * n
        def dfs(i: int) -> None:
            # 1.2 形式为 dfs(i), 另外用一个 on_path 数组记录元素是否已经用到了 path种
            if i == n:
                ans.append(path.copy())
                return
            for j, on in enumerate(on_path):
                if not on:
                    path[i] = nums[j]
                    on_path[j] = True
                    dfs(i + 1)
                    on_path[j] = False  # 恢复现场
        dfs(0)
        return ans

    """ 0051. N 皇后 #hard 求解N皇后的所有解 限制: n 9
思路1: #回溯 类似「0046. 全排列」的两种写法
    1.1 通过一个 is_valid(r,c) 判断当前位置和 path上的其他点是否会冲突, 这样检查的复杂度为 O(n)
        复杂度: O(n^2 n!), 在每个节点中, 生成答案复杂度 O(N^2), for循环加上is_valid的复杂度也是 O(n^2)
    1.2 通过类似 on_path 的方式, 对于两条对角线也进行检查, 这样检查的复杂度为 O(1)
        复杂度: 瓶颈在生成答案的时候, 若不生成答案复杂度为 O(n n!)
"""
    def solveNQueens(self, n: int) -> List[List[str]]:
        # 1.1 需要写一个 is_valid(r,c)
        ans = []
        path = [0] * n
        def is_valid(r,c):
            for r2,c2 in enumerate(path[:r]):
                if r+c==r2+c2 or r-c==r2-c2:
                    return False
            return True
        def dfs(i,scol):    # scol 是剩余的不冲突列
            if i==n:
                ans.append(['.'*x+'Q'+'.'*(n-x-1) for x in path])
                return 
            for x in scol:
                # 检查两个斜方向上不冲突
                if not is_valid(i,x): continue
                path[i] = x
                dfs(i+1,scol-{x})
        dfs(0, set(range(n)))
        return ans
    def solveNQueens(self, n: int) -> List[List[str]]:
        # 1.2 另外用三个数组来检查冲突
        m = n * 2 - 1
        ans = []
        col = [0] * n
        on_path = [False] * n   # 用于记录列是否已经用到了
        diag1, diag2 = [False] * m, [False] * m
        def dfs(r: int) -> None:
            if r == n:
                ans.append(['.' * c + 'Q' + '.' * (n - 1 - c) for c in col])
                return
            for c, on in enumerate(on_path):
                # 充分利用Python支持负index的特性
                if not on and not diag1[r + c] and not diag2[r - c]:
                    col[r] = c
                    on_path[c] = diag1[r + c] = diag2[r - c] = True
                    dfs(r + 1)
                    on_path[c] = diag1[r + c] = diag2[r - c] = False  # 恢复现场
        dfs(0)
        return ans

    """ 0052. N皇后 II #hard 相较于 0052, 只需要返回解的数量
思路1: 类似0051的两种回溯方式. 其中1.2更快, 可以理解为「基于set的回溯」
思路2: 基于位运算的回溯 #hard
"""
    def totalNQueens(self, n: int) -> int:
        # 思路1:基于set的回溯
        m = n * 2 - 1
        ans = 0
        col = [0] * n
        on_path = [False] * n   # 用于记录列是否已经用到了
        diag1, diag2 = [False] * m, [False] * m
        def dfs(r: int) -> None:
            nonlocal ans
            if r == n:
                ans+=1
                return
            for c, on in enumerate(on_path):
                # 充分利用Python支持负index的特性
                if not on and not diag1[r + c] and not diag2[r - c]:
                    col[r] = c
                    on_path[c] = diag1[r + c] = diag2[r - c] = True
                    dfs(r + 1)
                    on_path[c] = diag1[r + c] = diag2[r - c] = False  # 恢复现场
        dfs(0)
        return ans
    def totalNQueens(self, n: int) -> int:
        # 思路2: 基于位运算的回溯 #hard
        def solve(row, columnes, diagonal1, diagonal2):
            # columnes, diagonal1, diagonal2 分别是位表示的每一列的冲突位置
            if row == n:
                return 1
            else:
                count = 0
                # 当前冲突的位置包括了 columnes | diagonal1 | diagonal2
                availavle_positions = ((1<<n)-1) & (~(columnes | diagonal1 | diagonal2))
                while availavle_positions:
                    position = availavle_positions & (-availavle_positions)             # 得到最低位 1
                    availavle_positions = availavle_positions & (availavle_positions-1) # 将最低位1置为 0
                    # 递归下一列, 注意压缩表示的变化
                    count += solve(row+1, columnes|position, (diagonal1|position)<<1, (diagonal2|position)>>1)
                return count
        return solve(0, 0, 0, 0)


sol = Solution()
result = [
    sol.solveNQueens(4),
]
for r in result:
    print(r)
