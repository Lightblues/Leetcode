from easonsi import utils
from easonsi.util.leetcode import *
""" 
https://leetcode.cn/contest/weekly-contest-249
@2022 """
class Solution:
    """ 1929. 数组串联 """
    def getConcatenation(self, nums: List[int]) -> List[int]:
        return nums + nums[:]
    
    """ 1930. 长度为 3 的不同回文子序列 #medium  """
    def countPalindromicSubsequence(self, s: str) -> int:
        leftMap = {}
        rightMap = {}
        for i,ch in enumerate(s):
            if ch not in leftMap:
                leftMap[ch] = i
            rightMap[ch] = i
        ans = 0
        for ch,l in leftMap.items():
            r = rightMap[ch]
            ans += len(Counter(s[l+1:r]))
        return ans
    
    """ 1931. 用三种不同颜色为网格涂色 #hard
给定一个 (m,n) 的网格, 用三种颜色涂, 要求相邻的颜色不同, 问有多少种方案.
约束: 1 <= m <= 5, 1 <= n <= 1000
思路1: #状压 #DP
    重点是grid的维度一比较小: 这样我们可以枚举所有的涂色可能性. 这样, 再遍历每一行的过程中, 仅需要考虑和上一行每一列的相邻颜色不同即可.
    考虑状压: 0,1,2 表示三种颜色, 则我们可以用 [0, 3^m) 范围内的数字表示每一行的涂色情况.
    用 `f[i][mask]` 表示遍历到第i行, 并且最后一行的颜色为mask的涂色方案数.
    状态转移: `f[i+1][mask] = sum{ f[i][mask2] }` 这里要求 mask, mask2 所对应的行涂色都是合法的, 并且两者同一列的颜色都不同.
    预处理: 可以预先计算所有合法的行涂色方案 validLines; 并且计算合法的相邻行 transMap, 其中 transMap[mask] 是所有合法的相邻行列表.
"""
    def colorTheGrid(self, m: int, n: int) -> int:
        MOD = 10**9 + 7
        def valid(mask: int) -> bool:
            pre = 3
            # while mask:
            for _ in range(m):
                mask, color = divmod(mask, 3)
                if color == pre: return False
                pre = color
            return True
        def validNeihbour(mask1, mask2):
            # while mask1 or mask2:
            for _ in range(m):
                mask1, color1 = divmod(mask1, 3)
                mask2, color2 = divmod(mask2, 3)
                if color1==color2: return False
            return True
        transMap = {}
        validLines = [i for i in range(3**m) if valid(i)]
        for line in validLines:
            transMap[line] = [l for l in validLines if validNeihbour(line, l)]
        # 
        cnt = Counter(validLines)
        for _ in range(n-1):
            newCnt = Counter()
            for line, nextLines in transMap.items():
                for nextLine in nextLines:
                    newCnt[nextLine] += cnt[line]
                    newCnt[nextLine] %= MOD
            cnt = newCnt
        return sum(cnt.values()) % MOD
    
    """ 1932. 合并多棵二叉搜索树  #hard #二叉搜索树 #树 #题型
给定n棵(合法的) 二叉搜索树,  每棵树最多两层 (也即最多root+left+right三个节点), 按照下面的方式进行合并, 问能否经过n-1 合并后成为一个合法的二叉搜索树.
合并方式为: 找到 (i,j) 对, 满足第j棵树的root值等于第i棵树的leave节点的值, 然后将这个节子节点替换为第j棵树, 并且整棵二叉搜索树仍然是合法的.
约束: 所给的n棵树的根节点值唯一
提示: **构造的唯一性**
    最重要的一点观察: 根据上述规则最终得到的结果是唯一的.
    题目保障了所有跟节点的值是唯一的, 我们可以知道, 若某一个树不是最终的root, 那么它对应的合并节点是唯一的. 
        反证法: 设该树的根值为x, 若有两个叶子节点的值均为x, 这棵树只能合并到其中一个叶子节点上, 那么最终还会有两个值相同的节点, 与最终得到一棵二叉搜索树矛盾.
    进一步有: 所有叶子节点的值也是唯一的 (因为最终二叉搜索树的节点值唯一, 而合并过程中最多只能消去一个叶子节点).
    这样, 构造就是唯一的. 遍历所有跟节点和叶节点, 我们可以找到那个唯一的跟节点 (其值不出现在叶节点的值中), 而其他树都可以与某一个叶子节点唯一对应起来.
思路1: 从上往下遍历
    关键是要找到某一节点的值的范围约束. 如果不按照特定顺序进行合并, 则较难维护叶子节点的range.
    而根据构造的唯一性, 我们可以从跟节点出发, 这样, 我们在遍历过程中可以维护新增节点的范围约束
        例如, 假设当前节点node的范围约束为 `range = (l, r)`, 我们在根节点中找到 node.val 所对应的那一棵树 replaceNode(由于我们的构造顺序, 其最多root+left+right三个节点), 我们很容易检查是否满足条件
        然后, 更新replaceNode的叶子节点的 range.
    综上, 我们维护一个queue记录从跟节点出发的树中所包含的所有叶节点, 遍历过程中, 将会发生合并的根节点替换该叶节点, 然后将新加入节点的叶节点加入queue. 最后, 若今剩下唯一的合法二叉搜索树, 则构造成功.
思路2: 直接 #中序遍历
    官答给出了一种更妙的思路: **既然构造是唯一的, 并且我们可以按照从上往下的顺序来合并, 那么直接中序遍历即可.**
    这样, 相较于思路1, 我们可以简化节点范围约束的检查: 因为中序遍历天然要求节点的值递增, 我们仅需要维护一个全局的 prev 变量, 记录上一个节点的值即可.
    [官答](https://leetcode.cn/problems/merge-bsts-to-create-single-bst/solution/he-bing-duo-ke-er-cha-sou-suo-shu-by-lee-m42t/)
"""
    def canMerge(self, trees: List[TreeNode]) -> Optional[TreeNode]:
        """ 思路0: 根据合并结果的唯一性, 从上往下生成结果. """
        trees = set(trees)
        rootMap = {}
        leaveMap = {}
        for t in trees:
            rootMap[t.val] = t
            if t.left:
                if t.left.val in leaveMap: return None
                leaveMap[t.left.val] = t.left
            if t.right:
                if t.right.val in leaveMap: return None
                leaveMap[t.right.val] = t.right
        # 找到根节点: 肯定只有一个
        root = None
        for t in trees:
            if t.val not in leaveMap:
                if root: return None
                root = t
        if root is None: return None
        trees.remove(root)
        # 从上往下生成树, 用一个队列q 维护当前树所包含的叶节点
        # (node, parent, left/right)
        q = deque()
        if root.left:
            root.left.range = (-inf, root.val)
            q.append((root.left, root, 'left'))
        if root.right:
            root.right.range = (root.val, inf)
            q.append((root.right, root, 'right'))
        while q:
            node, p, ctype = q.popleft()
            if node.val not in rootMap: continue
            rep = rootMap[node.val]
            # 
            trees.remove(rep)
            if rep.left:
                if rep.left.val <= node.range[0]: return None
                rep.left.range = (node.range[0], rep.val)
                q.append((rep.left, rep, 'left'))
            if rep.right:
                if rep.right.val >= node.range[1]: return None
                rep.right.range = (rep.val, node.range[1])
                q.append((rep.right, rep, 'right'))
            if ctype=='left':
                p.left = rep
            else:
                p.right = rep
        if len(trees)>1: return None
        return root

    def canMerge(self, trees: List[TreeNode]) -> Optional[TreeNode]:
        """ https://leetcode.cn/problems/merge-bsts-to-create-single-bst/solution/he-bing-duo-ke-er-cha-sou-suo-shu-by-lee-m42t/ """
        # 存储所有叶节点值的哈希集合
        leaves = set()
        # 存储 (根节点值, 树) 键值对的哈希映射
        candidates = dict()
        for tree in trees:
            if tree.left:
                leaves.add(tree.left.val)
            if tree.right:
                leaves.add(tree.right.val)
            candidates[tree.val] = tree
        
        # 存储中序遍历上一个遍历到的值，便于检查严格单调性
        prev = float("-inf")
        
        # 中序遍历，返回值表示是否有严格单调性
        def dfs(tree: Optional[TreeNode]) -> bool:
            if not tree:
                return True
            
            # 如果遍历到叶节点，并且存在可以合并的树，那么就进行合并
            if not tree.left and not tree.right and tree.val in candidates:
                tree.left = candidates[tree.val].left
                tree.right = candidates[tree.val].right
                # 合并完成后，将树丛哈希映射中移除，以便于在遍历结束后判断是否所有树都被遍历过
                candidates.pop(tree.val)
            
            # 先遍历左子树
            if not dfs(tree.left):
                return False
            # 再遍历当前节点
            nonlocal prev
            if tree.val <= prev:
                return False
            prev = tree.val
            # 最后遍历右子树
            return dfs(tree.right)
        
        for tree in trees:
            # 寻找合并完成后的树的根节点
            if tree.val not in leaves:
                # 将其从哈希映射中移除
                candidates.pop(tree.val)
                # 从根节点开始进行遍历
                # 如果中序遍历有严格单调性，并且所有树的根节点都被遍历到，说明可以构造二叉搜索树
                return tree if dfs(tree) and not candidates else None
        
        return None

    def test(self):
        trees = []
        treeNums = [[2,1],[3,2,5],[5,4]]
        for nums in treeNums:
            root = TreeNode(nums[0])
            root.left = TreeNode(nums[1])
            if len(nums)>2:
                root.right = TreeNode(nums[2])
            trees.append(root)
        return self.canMerge(trees)
    
    def testClass(self, inputs):
        # 用于测试 LeetCode 的类输入
        s_res = [None] # 第一个初始化类, 一般没有返回
        methods, args = [eval(l) for l in inputs.split('\n')]
        class_name = eval(methods[0])(*args[0])
        for method_name, arg in list(zip(methods, args))[1:]:
            r = (getattr(class_name, method_name)(*arg))
            s_res.append(r)
        return s_res
    
sol = Solution()
result = [
    # sol.countPalindromicSubsequence(s = "aabca"),
    # sol.countPalindromicSubsequence(s = "bbcbaba"),
    # sol.test(),
    sol.colorTheGrid(5,5),
    sol.colorTheGrid(1,1),
    sol.colorTheGrid(1,2),
]
for r in result:
    print(r)
