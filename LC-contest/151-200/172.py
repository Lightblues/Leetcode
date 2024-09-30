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
https://leetcode.cn/contest/weekly-contest-172

T4有点意思, 贪心的思路很巧妙~

#专题: 贪心的「跳跃游戏」
    0055. 跳跃游戏 #medium 基本题型. 计数
    0045. 跳跃游戏 II #medium 简化, 判断是否可达
    1024. 视频拼接 #medium 综合, 计数! 
    1326. 灌溉花园的最少水龙头数目 #hard 变种, 难度更高一点


@2022 """
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    """ 1323. 6 和 9 组成的最大数字 """
    def maximum69Number (self, num: int) -> int:
        return int(str(num).replace('6','9',1))
    
    """ 1324. 竖直打印单词 """    
    def printVertically(self, s: str) -> List[str]:
        words = s.split()
        max_len = max([len(w) for w in words])
        res = []
        for i in range(max_len):
            res.append(''.join([w[i] if i<len(w) else ' ' for w in words]).rstrip())
        return res
    
    """ 1325. 删除给定值的叶子节点 """
    def removeLeafNodes(self, root: Optional[TreeNode], target: int) -> Optional[TreeNode]:
        if not root:
            return None
        root.left = self.removeLeafNodes(root.left, target)
        root.right = self.removeLeafNodes(root.right, target)
        if root.left == root.right and root.val == target:
            return None
        return root

    """ 1326. 灌溉花园的最少水龙头数目 #hard #题型 #review 有个在数轴上的长n的线段 [0,n]. 在每个整数点有一个水龙头, 可以浇灌 [i+/-ranges[i]] 的区域. 问至少需要多少个水龙头可以覆盖
限制: n 1e4; . ranges 的数据范围 [0,100]
问题转化. 可以将各个range的范围限制在 [0,n] 范围内. 这样, 问题变为经典的「在一组区间中选最少数量进行覆盖」.
思路1: #DP
    我们这里的端点都是整数 (共 n+1), 记 `prev[i]` 表示所有右端点为i的线段中, 左端点最小的 (贪心).
    这样, 令 `f[i]` 表示覆盖到 [0,i] 区间所需的最少数量, 则有转移 `f[i] = min{ f[j] } + 1. prev[i]<=j<i`.
    复杂度: O(n * R). 其中R是区间长度.
思路2: #贪心
    不妨倒过来考虑: 一开始肯定选择 prev[n]. 我们在这一区间内选择最远的右端点.
关联: 0045. 跳跃游戏 II #medium; 1024. 视频拼接 #medium
"""
    def minTaps(self, n: int, ranges: List[int]) -> int:
        # 思路1: #DP
        # prev[i]:  将 i 作为右端点, 左端点最小的线段
        prev = list(range(n+1))
        for i,r in enumerate(ranges):
            l = max(0, i-r)
            r = min(n, i+r)
            prev[r] = min(prev[r], l)
        f = [float('inf')] * (n+1)
        f[0] = 0
        for i in range(1, n+1):
            # if prev[i] == -1: continue
            for j in range(prev[i], i):
                f[i] = min(f[i], f[j]+1)
        return f[n] if f[n] < float('inf') else -1
    def minTaps(self, n: int, ranges: List[int]) -> int:
        # 思路2: #贪心
        # prev[i]:  将 i 作为右端点, 左端点最小的线段
        prev = list(range(n+1))
        for i,r in enumerate(ranges):
            l = max(0, i-r)
            r = min(n, i+r)
            prev[r] = min(prev[r], l)
        # 贪心
        cnt = 1
        llimit = prev[n]        # 当前区间的边界
        new_llimit = n          # 当前区间内, 得到的下一个边界
        for i in range(n-1, -1, -1):
            if i < llimit:
                # 若新边界不够, 说明无法覆盖, 直接返回.
                if i< new_llimit: return -1
                cnt += 1
                llimit = new_llimit
            else:
                new_llimit = min(new_llimit, prev[i])
        return cnt

    """ 1326. 灌溉花园的最少水龙头数目 #hard 在 [0,1...n] 有n+1个水龙头, 每个可以覆盖的范围为 [i-x, i+x], 返回可以覆盖整个 [0,n] 区间的最少水龙头数目
限制: n 1e4; x 1e2
思路1: 转化为 {跳跃游戏}
    可以将所有的水龙头覆盖的区域看作是一系列的 "桥", 我们统计每个位置 "作为桥的左端点所能覆盖的最远右端点", 就转化为了 "跳跃游戏"!
[ling](https://leetcode.cn/problems/minimum-number-of-taps-to-open-to-water-a-garden/solutions/2123855/yi-zhang-tu-miao-dong-pythonjavacgo-by-e-wqry/)
    """
    def minTaps(self, n: int, ranges: List[int]) -> int:
        steps = [0] * (n+1)
        for i,x in enumerate(ranges):
            left = max(0, i-x)
            right = min(n, i+x)
            steps[left] = max(steps[left], right)
        # 
        ans = 0
        cur_right = 0 # 当前桥所能覆盖的最远右端点
        next_right = 0
        for i in range(n):  # NOTE: 这里没有检查位置 n, 因为下面已经保障能到n了! 
            next_right = max(next_right, steps[i])
            if i == cur_right:
                if i == next_right: return -1 # 无法到达! 
                ans += 1
                cur_right = next_right
        return ans

    """ 0055. 跳跃游戏 #medium #题型
相较于 0045, 格子元素可以是 0, 判断是否可达. 
关联: 1024. 视频拼接 #medium 要求最小的数量, 更全面一些.
"""
    def canJump(self, nums: List[int]) -> bool:
        # 思路: 贪心
        n = len(nums)
        max_pos = 0
        for i in range(n):
            if i > max_pos: return False
            max_pos = max(max_pos, i+nums[i])
        return True 
    
    
    
    """ 0045. 跳跃游戏 II #medium #题型 数组每一个数字表示可跳跃的距离. 问到达终点最少需要多少步. 限制: 长度 n 1e4 
思路1: 正向逆向都可以. 维护当前步数可以到达的最远距离. 在搜索的过程中记录下一个最远距离.
    复杂度: O(n)
关联: 0055. 跳跃游戏 #medium; 
    1326. 灌溉花园的最少水龙头数目 #hard
[官答](https://leetcode.cn/problems/jump-game-ii/solution/tiao-yue-you-xi-ii-by-leetcode-solution/)
[ling](https://leetcode.cn/problems/jump-game-ii/solutions/2926993/tu-jie-yi-zhang-tu-miao-dong-tiao-yue-yo-h2d4/)
"""
    def jump(self, nums: List[int]) -> int:
        if len(nums) == 1: return 0
        
        n = len(nums)
        steps = 1   # 从第一个格子开始跳
        limit = new_limit = nums[0]
        for i in range(1, n):
            # 早停
            if limit >= n-1: return steps
            if i > limit:
                steps += 1
                limit = new_limit
            new_limit = max(new_limit, i+nums[i])
        return steps

    """ 1024. 视频拼接 #medium #题型 #细节 有一组 [s,e] 的视频片段. 问最少需要多少个片段才能覆盖 [0,T] 区间. 限制: n 1e2; T 1e2
思路1: #贪心. 对于s排序, 然后在遍历过程中, 选择最远的e.
关联: 0055. 跳跃游戏
[官答](https://leetcode.cn/problems/video-stitching/solution/shi-pin-pin-jie-by-leetcode-solution/) 还给了 #DP 的解法
"""
    def videoStitching(self, clips: List[List[int]], time: int) -> int:
        clips.sort()
        
        cnt = 0
        limit = new_limit = 0
        for s,e in clips:
            # 边界检查1: 早停
            if limit >= time: return cnt
            if s > limit:
                # 边界检查2: 早停
                if new_limit >= time: return cnt+1
                # 无法覆盖
                if new_limit <= s: return -1
                cnt += 1
                limit = new_limit
            new_limit = max(new_limit, e)
        # 注意条件是否满足
        # if limit >= time: return cnt
        # elif new_limit >= time: return cnt+1
        # else: return -1
        # 事实上下面的检查就够了!
        return cnt+1 if new_limit >= time else -1
    
sol = Solution()
result = [
    # sol.printVertically(s = "TO BE OR NOT TO BE"),
    sol.minTaps(n = 5, ranges = [3,4,1,1,0,0]),
    sol.minTaps(n = 3, ranges = [0,0,0,0]),
    # sol.jump(nums = [2,3,1,1,4]),
    # sol.jump(nums = [2,3,0,1,4]),
    # sol.videoStitching(clips = [[0,2],[4,6],[8,10],[1,9],[1,5],[5,9]], time = 10),
    # sol.videoStitching(clips = [[0,1],[1,2]], time = 5),
    # sol.videoStitching([[0,2],[4,8]], 5),
    # sol.videoStitching([[5,7],[1,8],[0,0],[2,3],[4,5],[0,6],[5,10],[7,10]], 5),
    # sol.videoStitching([[11,28],[35,40],[28,38],[0,10],[37,39],[40,40],[18,34],[32,38],[14,36],[33,36]], 8),
]
for r in result:
    print(r)
