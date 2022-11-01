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
https://leetcode.cn/contest/weekly-contest-317
题解: https://leetcode.cn/circle/discuss/7A4iOi/
灵神: https://www.bilibili.com/video/BV1Em4y1c7Hc/
@2022 """
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """ 6220. 可被三整除的偶数的平均值 """
    def averageValue(self, nums: List[int]) -> int:
        x = [i for i in nums if i%6==0]
        return sum(x)//len(x) if len(x)>0 else 0
    
    """ 6221. 最流行的视频创作者 #排序 输出 """
    def mostPopularCreator(self, creators: List[str], ids: List[str], views: List[int]) -> List[List[str]]:
        c2v = defaultdict(int)
        c2videos = defaultdict(list)
        for c,vid,v in zip(creators, ids, views):
            c2v[c] += v
            c2videos[c].append((v, vid))
        mx = max(c2v.values())
        ans = []
        for c,v in c2v.items():
            if v==mx:
                x = sorted(c2videos[c], key=lambda x: (-x[0],x[1]))
                ans.append([c, x[0][1]])
        return ans
    
    """ 6222. 美丽整数的最小增量 #medium #题型 一个整数的「分数」为所有数字之和, 现在给定一个n, 问最少加上多少, 才能使得n的分数 <=target. 限制: n 1e12, target 150
思路1: 模拟 #进位. 注意一些 #细节
[灵神](https://leetcode.cn/problems/minimum-addition-to-make-integer-beautiful/solution/tan-xin-by-endlesscheng-f7e4/) 的代码太优雅了
"""
    def makeIntegerBeautiful(self, n: int, target: int) -> int:
        # 方便期间转为 list
        digits = list(map(int, str(n)))
        ans = []
        idx = len(digits)-1 # 当前考察的位
        while idx>=0:
            # 检查是否满足条件
            if sum(digits) <= target: break
            # 
            if digits[idx]!=0:
                ans.append(10-digits[idx])
                # 注意, 可能有连续进位
                i = idx-1
                while  i>0 and digits[i]==9:
                    digits[i]=0; i-=1
                # 因为题目保证了总有答案, 不考虑最高位进位 (分数变为 1)
                if i>=0 : digits[i] += 1
            else:
                ans.append(0)
            # 加上增量之后, 将这一位置0
            digits[idx] = 0
            idx -= 1
        if len(ans)==0: return 0
        return int("".join(reversed(list(map(str, ans)))))
    def makeIntegerBeautiful(self, n: int, target: int) -> int:
        # from 灵神的代码: 考虑进位最后得到的数字是什么
        tail = 1        # 每次考察的位
        while True:
            m = x = n + (tail - n % tail) % tail  # 进位后的数字
            s = 0
            while x:
                s += x % 10
                x //= 10
            if s <= target: return m - n
            tail *= 10

    
    """ 6223. 移除子树后的二叉树高度 #hard #题型 #树 给定一个节点值互不相同的二叉树. 对于每个查询, 减掉对应的那个节点, 返回剩下的树高. 限制: n 1e5; 查询数量 1e4 
思路1: 很不优雅的做法. 先计算每个节点的深度, 然后从叶子 (最深的层) 出发, 模拟删除该节点, 考虑删除之后该层剩余的节点.
    如何得到「删除子树之后剩余树的高度」? 统计当前层每个节点的信息 [(i, subTHeight)], 这里的 subTHeight 是该子树中的最大深度
    得到当前层的 nodes 之后, 分类讨论:
        当前层只有一个节点了 (涵盖了所有的叶子) ! 删掉就没有 level 层了, 该节点答案为 level-1
        否则, 考虑最大 subTHeight 的那些节点:
            若最大深度节点不止一个, 删除任意节点都不影响最大深度.
            否则, 其他节点不变, 那个唯一的节点删除之后, 答案为 secondSubTHeight
    如何更新上一层节点的 subTHeight 信息? 例如父子边. 
思路2: 两次 #DFS 
    如何得到「删除该节点之后的树高」? 取决于其余节点的最大深度 (非该节点对应子树)
        我们可以用 `dfs(node, depth, restH)` 进行递归. 其中 depth是当前节点深度/层, restH是其他节点的最大深度/树高. 
            递归左右子树的时候, 只需要更新 restH (加上另一个孩子所构成的最大树高),
            也即, `dfs(node.left, depth+1, max(rest_h, depth + height[node.right]))`
    因此, 两次DFS, 先得到每棵子树的高度 height; 然后根据上面的DFS得到答案. 
    见 [灵神](https://leetcode.cn/problems/height-of-binary-tree-after-subtree-removal-queries/solution/liang-bian-dfspythonjavacgo-by-endlessch-vvs4/)
思路3: 「将树通过 DFS 序转成序列」
    注意: **DFS可以将树结构根据访问顺序转为序列**, 这样每棵子树对应了序列中的一段连续数组!
    则对于每个查询, 等价于删除一段子数组后的最大值. 要求两端区间的最大值, 可以分别构建 #前缀 #后缀 数组得到.
    见 [讨论](https://leetcode.cn/circle/discuss/7A4iOi/)
"""
    def treeQueries(self, root: Optional[TreeNode], queries: List[int]) -> List[int]:
        # DFS 得到每个节点的 层高、父节点
        val2node = defaultdict(TreeNode)
        val2height = defaultdict(int)       # 每个节点的层高
        def dfs(node:TreeNode, h:int, fa:TreeNode=None):
            if node is None: return
            node.fa = fa
            val2node[node.val] = node
            val2height[node.val] = h
            dfs(node.left, h+1, node)
            dfs(node.right, h+1, node)
        dfs(root,0,None)
        # 得到 hight2nodes 列表
        mx = max(val2height.values())
        hight2nodes = [[] for i in range(mx+1)]
        for k,v in val2height.items():
            hight2nodes[v].append(k)
        # 从底层(叶子) 往上扫描, 根据规则填写 val2ans 表
        val2ans = defaultdict(int)
        level = mx  # 从下往上扫描
        nodes = [(i,mx) for i in hight2nodes[mx]] # 当前层的节点 (i, subTHeight) 这里的 subTHeight 是该子树中的最大深度
        while level>0:
            # 当前层只有一个节点了 (涵盖了所有的叶子) ! 删掉就没有 level 层了
            if len(nodes)==1:
                val2ans[nodes[0][0]] = level-1
            else:
                hs = [i[1] for i in nodes]
                mxHeight = max(hs)
                if hs.count(mxHeight) == 1:
                    # 最大深度的节点只有一个, 则删除该节点之后得到 secondHeight 的答案
                    secondHeight = max(h for h in hs if h!=mxHeight)
                    for i,h in nodes:
                        if h==mxHeight: val2ans[i] = secondHeight
                        else: val2ans[i] = mxHeight
                else:
                    # 最大深度节点不止一个, 删除任意节点都不影响最大深度.
                    for node,h in nodes: val2ans[node] = mxHeight
            # 得到上一层的节点集合 newNodes
            fa2h = defaultdict(int)     # 计算 subTHeight
            for node,h in nodes:
                fa = val2node[node].fa
                # 注意根节点的 fa为空
                if fa is None: continue
                fa2h[fa.val] = max(fa2h[fa.val], h)
            newNodes = []
            used = set()
            for fa,h in fa2h.items():
                used.add(fa)
                newNodes.append((fa,h))
            for node in hight2nodes[level-1]:
                if node not in used: newNodes.append((node,level-1))
            nodes = newNodes
            level -= 1
        # 
        return [val2ans[i] for i in queries]
    
    def treeQueries(self, root: Optional[TreeNode], queries: List[int]) -> List[int]:
        # 得到每棵子树的高度
        heights = defaultdict(int)
        def getH(node:TreeNode):
            if node is None: return 0
            h = max(getH(node.left), getH(node.right)) + 1
            heights[node.val] = h
            return h
        getH(root)
        # 第二次DFS
        val2ans = defaultdict(int)
        def dfs(node:TreeNode, depth:int, restH:int):
            # depth: 当前节点深度
            # restH: 树上其他节点构成的树高
            if node is None: return
            val2ans[node.val] = restH
            depth += 1
            # 注意 node.right 可能为空. (可以 heights 字典的键直接设置为node 来避免)
            dfs(node.left, depth, max(restH, depth + (heights[node.right.val] if node.right else 0)))
            dfs(node.right, depth, max(restH, depth + (heights[node.left.val] if node.left else 0)))
        dfs(root, -1, 0)
        return [val2ans[i] for i in queries]

# example 2
root = TreeNode(5)
root.left = TreeNode(8)
root.left.left = TreeNode(2, TreeNode(4), TreeNode(6))
root.left.right = TreeNode(1)
root.right = TreeNode(9, TreeNode(3), TreeNode(7))

sol = Solution()
result = [
    # sol.averageValue(nums = [1,3,6,10,12,15]),
    # sol.averageValue([1,2,4,7]),
    # sol.mostPopularCreator(creators = ["alice","bob","alice","chris"], ids = ["ne","two","three","four"], views = [5,10,5,4]),
    # sol.mostPopularCreator(creators = ["alice","alice","alice"], ids = ["a","b","c"], views = [1,2,2]),
    # sol.makeIntegerBeautiful(n = 16, target = 6),
    # sol.makeIntegerBeautiful(n = 467, target = 6),
    # sol.makeIntegerBeautiful(1,1),
    # sol.makeIntegerBeautiful(590, 1),
    # sol.makeIntegerBeautiful(94598, 6),
    sol.treeQueries(root, [3,2,4,8])
]
for r in result:
    print(r)
