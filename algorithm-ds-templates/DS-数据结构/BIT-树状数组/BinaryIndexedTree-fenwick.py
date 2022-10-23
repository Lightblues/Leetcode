from easonsi.util.leetcode import *

# from utils_leetcode import testClass
# from structures import ListNode, TreeNode, linked2list, list2linked

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
[树状数组](https://oi-wiki.org/ds/fenwick/) 参见 [here](https://blog.csdn.net/Yaokai_AssultMaster/article/details/79492190)
图参见上面的链接. 简言之, 希望 0100 能够存储数组中 0001-0100 四个位置之和 (从1开始计数), 1010能够存储 1001, 1010 两个位置数字之和
从而, 希望得到数组前 1010之和时, 能够进行分解 sum[1010] = l[1010] + l[1000]
要更新数组 1010位置的数字 (+某一数值), 则需要更新 1010, 1100 即每次加上最低1位 (这里假设 10000 超过了数组长度)
因此, 1. 求前缀和, 每次减去数字最低的数字1位, 累计; 2. 对某一个idx的数字更新, 每次加上最低数字1位, 直到数组最大长度.

ref: [区间操作？一个树状数组就够了](https://mp.weixin.qq.com/s?__biz=MzkyMzI3ODgzNQ==&mid=2247483674&idx=1&sn=263595b26950ac60e5bf789839d70c9e&chksm=c1e6cd86f691449062d780b96d9af6d9590a71872ebfee98)

LC list: https://leetcode.cn/tag/binary-indexed-tree/problemset/

== 基本应用: 统计区间内的最大/最小值. 一般配合离散化技巧
0315. 计算右侧小于当前元素的个数 #hard #题型
    给定一个数组, 要求返回一个等长的数组, 其中 `count[i]` 是 `nums[i+1:]` 范围内小于 `nums[i]` 的个数.
    思路一: 逆序遍历, 每次找更小数字范围内的前缀和即可.
1584. 连接所有点的最小费用 #medium #题型 可以有更巧妙的 #hard 解法
    平面上有一组点, 问将所有点都联通所需的最小距离和. 也即, 求 #最小生成树.
    思路3: 建图优化的 Kruskal #hard 基本思想是, 思路1的复杂度高是因为边过多 (全联通图). 这里利用了一个intuition将每个点连接的边的数量限制
    这里树状数组的应用, 也是统计区间内的最小值. 不过整体非常复杂.
    
"""


""" 基本 BIT
作用: 单点更新, 区间查询
基本原理: 用 0100 存储数组中 0001-0100 四个位置之和 (从1开始计数), 用 1010 存储 1001, 1010 两个位置数字之和
update(idx, val): 给第idx个数加上val
query(x): 求前缀和
"""
class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n+1)     # 从1开始计数
    @staticmethod
    def lowbit(x):
        return x & (-x)
    def update(self, i, delta=1):
        # 对于位置i的元素, 增加delta
        while i <= self.n:
            self.tree[i] += delta
            i += self.lowbit(i)
    def query(self, x):
        # 查询位置i的前缀和
        res = 0
        while x > 0:
            res += self.tree[x]
            # 下面两种等价!! 
            # x -= self.lowbit(x)
            x &= x-1        # 也是去掉最低位的1
        return res


""" 增加了用一个数组来初始化, 复杂度 O(n)
用一个数组来初始化树状数组, 这里 idx 从 1 开始
add(self, idx, delta): 在 idx 处添加 delta
getPrefixSum(self, idx): 返回到 idx 的前缀和
getRangeSum(self, l, r): 返回 [l, r] 的和
 """
def lowbit(x): return x & -x
class BinaryIndexedTree:
    def __init__(self, l) -> None:
        # 根据数组 l 进行初始化

        # 这种初始化需要 O(nlogn)
        # self.l = [0] * (len(l) + 1)
        # for i in range(len(l)):
        #     self.add(i+1, l[i])
        
        # 这样复杂度 O(n) [实际上就是简化了重复的累加操作]
        self.l = [0] * (len(l) + 1)
        for i in range(len(l)):
            self.l[i+1] = l[i]
        for i in range(1, len(l)+1):
            j = i + lowbit(i)
            if j <= len(l):
                self.l[j] = self.l[j] + self.l[i]
        
        # 这种初始化需要 O(nlogn)
        self.l = [0] * (len(l) + 1)
        for i in range(len(l)):
            self.add(i+1, l[i])

    def add(self, idx, delta):
        # 对于 idx 位置的元素 +delta
        # idx += 1
        while idx < len(self.l):
            self.l[idx] += delta
            idx += lowbit(idx)
    
    def getPrefixSum(self, idx):
        # 计算 0...idx 的和
        # idx += 1
        ret = 0
        while idx > 0:
            ret += self.l[idx]
            idx -= lowbit(idx)
        return ret

    def getRangeSum(self, l, r):
        return self.getPrefixSum(r) - self.getPrefixSum(l-1)


class Solution:
    """ 0315. 计算右侧小于当前元素的个数 #hard #题型
给定一个数组, 要求返回一个等长的数组, 其中 `count[i]` 是 `nums[i+1:]` 范围内小于 `nums[i]` 的个数.
思路一: #离散化 #树状数组
    从右往左遍历数组, 每次检查小于x的数字有多少. 由于 #前缀和 是需要动态更新的, 采用树状数组.
    由于数字的范围较大而数组长度有限, 可以进行 #离散化 操作.
    复杂度: O(nlog(n))
    from [here](https://leetcode-cn.com/problems/count-of-smaller-numbers-after-self/solution/ji-suan-you-ce-xiao-yu-dang-qian-yuan-su-de-ge-s-7/)
方法二：归并排序
 """
    def countSmaller(self, nums: List[int]) -> List[int]:
        # 离散化
        sortedNums = sorted(set(nums))
        mapped = {n: i+1 for i, n in enumerate(sortedNums)}
        nums = [mapped[n] for n in nums]
        n = len(nums)
        ans = [0] * n
        bit = BIT(n)
        for i in range(n-1, -1, -1):
            bit.update(nums[i], 1)
            ans[i] = bit.query(nums[i]-1)
        return ans
    
    
    


    
    

    
sol = Solution()
result = [
    sol.countSmaller(nums = [5,2,6,1]),
    
]
for r in result:
    print(r)
