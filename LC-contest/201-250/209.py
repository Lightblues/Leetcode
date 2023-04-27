from easonsi import utils
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

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

""" 
https://leetcode.cn/contest/weekly-contest-209

两道hard的一次... T2考差了二叉树的深度, 用BFS即可, 不过还是WA了; T3之前写过了; T4事实上可以通过找规则得到DP, 但自己一开始没想明白, 实际上就是格雷码.


@2022 """
class Solution:
    """ 1608. 特殊数组的特征值 """
    def specialArray(self, nums: List[int]) -> int:
        n = len(nums)
        for x in range(1, n+1):
            if len([i for i in nums if i>=x]) == x: return x
        return -1
    
    """ 1609. 奇偶树 #medium #题型 BFS遍历二叉树
给定一棵二叉树, 判断其是否满足: 从上往下分别是0,1,2...层; 偶数层数字都是奇数, 并且从左往右严格递增; 奇数层相反.
思路: 利用 BFS 遍历二叉树, 判断每一层的数字是否满足条件.
"""
    def isEvenOddTree(self, root: Optional[TreeNode]) -> bool:
        queue = [root]
        flag  = 1
        while queue:
            nqueue = []
            pre = flag * inf
            for r in queue:
                if r.val % 2 != (flag==1): return False
                if (r.val - pre) * flag <= 0: return False
                pre = r.val
                if r.left is not None: nqueue.append(r.left)
                if r.right is not None: nqueue.append(r.right)
            queue = nqueue
            flag *= -1
        return True
        
    """ 1610. 可见点的最大数目 #hard #极角
你在location有一个角度为angle的视角, 现在给定一组points, 问通过该视角最多可以看到多少点?
限制: 不考虑重叠, 边界上的点可见 (若点在location则永远可见)
思路1: #双指针 先计算所有点的角度, 排序, 然后用双指针来遍历.
    要注意: 这里的遍历过程是一个「环」而非数组, 要注意边界情况! 下面用了 `j<=n-1 and angles[j]-angles[i]<=angle` 和 `j>n-1 and 360-angles[i]+angles[j%n]<=angle` 两个条件来判断从角度i出发, j是否在其逆时针angle范围内.
    复杂度: 排序 O(n log(n))
思路2: #二分 查找边界
    也是先对于角度排序, 然后对a[i] 而非查找 a[i]+angle 的边界在哪里.
    技巧: 对于「环」的问题, 官答中给出的技巧是将angles数组每个加360之后拼接到原数组后面, 构成一个长2n的递增数组.
    复杂度: 相较于双指针遍历复杂度 O(n), 对于每个位置进行二分复杂度 O(n log(n))
另外, 需要注意 #极角 的计算. 利用atan计算, 注意y=0时是没有定义的; 另外atan的取值范围为180度, 需要根据x,y的正负来另外判断.
"""
    def visiblePoints(self, points: List[List[int]], angle: int, location: List[int]) -> int:
        a,b = location
        angles = []
        bias = 0
        for x,y in points:
            x,y = x-a, y-b
            if x==0:
                if y>0: angles.append(90)
                elif y<0: angles.append(270)
                else: bias += 1
            elif x>0:
                if y>=0: angles.append(math.atan(y/x)*180/math.pi)
                else: angles.append(360+math.atan(y/x)*180/math.pi)
            else:
                if y>=0: angles.append(180+math.atan(y/x)*180/math.pi)
                else: angles.append(180+math.atan(y/x)*180/math.pi)
        n = len(angles)
        angles.sort()
        ans = 0
        j = 0
        for i in range(0, n):
            while j<=n-1 and angles[j]-angles[i]<=angle: j += 1
            while j>n-1 and 360-angles[i]+angles[j%n]<=angle: j+= 1
            if j>=i: ans = max(ans, j-i)
            else: ans = max(ans, n-i+j)
        return ans + bias
    
    """ 1611. 使整数变为 0 的最少操作次数 #hard #题型
给定一个二进制数, 可以进行两种操作: 1) 翻转最低1位的上一位; 2) 翻转最后一位. 问最少需要多少次操作才能得到0.
思路1: #找规律 #DP
    提示: 由于两种操作都是可逆的, 因此等价于将0变为目标值n
    手动计算得到 1, 10, 100,... 的过程, 可知要得到这些数字分别需要 1,3,7.. = 2^x-1 步 (或者是下面的递归形式 `2*f(n>>1) + 1`)
    并且, 这些数字都是最高位相同的数字中最后才取到的. 例如100, 需要经过 10; 110,111,101,100 得到. 我们已知了100的步数, 怎么求110? 可知110->100 等价于100->110, 也即从0变为10.
    总结: 用 #记忆化 搜索的形式. 1) 若 `n.bit_count()==1` 则按照上式计算; 2) 否则, 等于 `f(1<<mxbit) - f(n-(1<<mxbit))` 这里的 `1<<mxbit` 是最高位.
    参见 [here](https://leetcode.cn/problems/minimum-one-bit-operations-to-make-integers-zero/solution/gen-zhao-ti-shi-zhao-gui-lu-kan-liao-bie-ren-de-ge/)
思路1.1: 再给出「正向」从n变为0的 #记忆化 DP方案
    每次, 我们要消除最高位第i位的1, 易知需要变为 `110...0` 的形式, 也即要将此高位变为1; 而要得到上述形式, 则要将 i-2...0 都变为0, 递归问题.
    因此, 有递归 `f[n] = f[1^(x-1)] + f[n - 1^x] + 1` 其中第一项可以直接算出来, 第二项是递归问题.
    见 [here](https://leetcode.cn/problems/minimum-one-bit-operations-to-make-integers-zero/solution/hua-shan-yi-tiao-dao-wo-men-di-gui-zhao-zou-by-luc/)
思路1: 本质上是 #格雷码 参见 [here](https://leetcode.cn/problems/minimum-one-bit-operations-to-make-integers-zero/solution/xiang-jie-ge-lei-ma-by-simpleson/)
    总结: **二进制 - 格雷码 的转换规则为**: 从二进制编码到格雷码, 对于任意位 i, 相应变为 `gray[i] = bin[i]^bin[i+1]`; 解码, 从左到右, 第一位1不变, 剩余位 `bin[i] = gray[i]^bin[i+1]` (例如 `bin(1111)=gray(1000)`)
    化简: 由于编码规则 `num^(num>>1)=gray`. 也即 `decode(gray)^((decode(gray)>>1)=gray`, 因此有 `decode(gray)=gray^((decode(gray)>>1)`. 而根据解码规则, 显然右移操作和解码操作可交换
"""
    def minimumOneBitOperations(self, n: int) -> int:
        @lru_cache(None)
        def f(n: int):
            if n==0: return 0
            if n.bit_count()==1: return 2*f(n>>1) + 1
            mxbit = n.bit_length()-1
            return f(1<<mxbit) - f(n-(1<<mxbit))
        return f(n)

    def minimumOneBitOperations(self, n: int) -> int:
        # 思路2
        if not n:return 0
        head = 1<<int(math.log2(n))
        return head + self.minimumOneBitOperations((n^head)^(head>>1))
    def minimumOneBitOperations(self, n: int) -> int:
        # 化简版本
        if not n:return 0
        return n^self.minimumOneBitOperations(n>>1)

    
    
sol = Solution()
result = [
    # sol.specialArray(nums = [0,4,3,0,4]),
    # sol.specialArray(nums = [3,6,7,7,0]),
    # sol.visiblePoints(points = [[2,1],[2,2],[3,3]], angle = 90, location = [1,1]),
    # sol.visiblePoints(points = [[2,1],[2,2],[3,4],[1,1]], angle = 90, location = [1,1]),
    # sol.visiblePoints(points = [[1,0],[2,1]], angle = 13, location = [1,1]),
    sol.minimumOneBitOperations(n = 3),
    sol.minimumOneBitOperations(6),
]
for r in result:
    print(r)
