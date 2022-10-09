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
https://leetcode.cn/contest/weekly-contest-180
@2022 """
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """ 1380. 矩阵中的幸运数 """
    def luckyNumbers (self, matrix: List[List[int]]) -> List[int]:
        m,n = len(matrix), len(matrix[0])
        ret = []
        for i,j in product(range(m), range(n)):
            if matrix[i][j] == min(matrix[i]) and matrix[i][j] == max([matrix[k][j] for k in range(m)]):
                ret.append(matrix[i][j])
        return ret
    
    """ 1382. 将二叉搜索树变平衡 #medium 给定一棵二叉搜索树, 要求变为「平衡」的. 何谓平衡? 每个节点的左右子树高度差不超过 1.
思路1: 先 #中序遍历 得到有序的数组结构. 然后 #二分法 构建平衡二叉树. 
    如何二分? 其实非常简单: 二分的中点就是根节点. 左边的数组构建左子树, 右边的数组构建右子树.
    正确性? 见 [官答](https://leetcode.cn/problems/balance-a-binary-search-tree/solution/jiang-er-cha-sou-suo-shu-bian-ping-heng-by-leetcod/).
"""
    def balanceBST(self, root: TreeNode) -> TreeNode:
        def inorder(root):
            if not root:
                return []
            return inorder(root.left) + [root.val] + inorder(root.right)
        vals = inorder(root)
        def build(vals):
            if not vals:
                return None
            mid = len(vals) // 2
            root = TreeNode(vals[mid])
            root.left = build(vals[:mid])
            root.right = build(vals[mid+1:])
            return root
        return build(vals)
    
    """ 1383. 最大的团队表现值 #hard 每个员工有 (speed, efficiency). 从中最多选 k个员工, 分数定义为 sum(speed) * min(efficiency). 求最大分数. 限制: n 1e5
思路1: 排序后用 #堆 记录speed最大的k个员工.
    提示: 在根据效率排序之后, 我们在可选项中选择速度最快的k个员工即可.
    先根据 efficiency 排序, 用一个 #最小堆 记录 speed 最大的 k 个员工. 在遍历过程中, 我们搭配的 min(efficiency) 直接取当前员工的效率即可. 
"""
    def maxPerformance(self, n: int, speed: List[int], efficiency: List[int], k: int) -> int:
        mod = 10**9 + 7
        people = sorted(zip(efficiency, speed), reverse=True)
        mx = 0; acc = 0
        h = []
        for i, (e, s) in enumerate(people):
            if len(h) < k:
                heappush(h, s)
                acc += s
            else:
                if h[0] < s:
                    acc += s - h[0]
                    heappushpop(h, s)
            mx = max(mx, e * acc)
        return mx % mod
    
""" 1381. 设计一个支持增量操作的栈 """
class CustomStack:
    def __init__(self, maxSize: int):
        self.maxSize = maxSize
        self.st = []

    def push(self, x: int) -> None:
        if len(self.st) < self.maxSize:
            self.st.append(x)

    def pop(self) -> int:
        if self.st:
            return self.st.pop()
        return -1

    def increment(self, k: int, val: int) -> None:
        n = min(k, len(self.st))
        for i in range(n): self.st[i] += val

    
sol = Solution()
result = [
    # sol.luckyNumbers(matrix = [[3,7,8],[9,11,13],[15,16,17]]),
#     testClass("""["CustomStack","push","push","pop","push","push","push","increment","increment","pop","pop","pop","pop"]
# [[3],[1],[2],[],[2],[3],[4],[5,100],[2,100],[],[],[],[]]"""),
    sol.maxPerformance(n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 2),
    sol.maxPerformance(n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 3),
]
for r in result:
    print(r)
