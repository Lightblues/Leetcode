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
https://leetcode.cn/contest/weekly-contest-371
https://leetcode.cn/circle/discuss/2g47c7/

T4 出了少见字典树!
Easonsi @2023 """
class Solution:
    """ 2932. 找出强数对的最大异或值 I """
    def maximumStrongPairXor(self, nums: List[int]) -> int:
        n = len(nums)
        mx = 0
        for i in range(n):
            for j in range(i+1, n):
                if abs(nums[i]-nums[j]) > min(nums[i], nums[j]): continue
                mx = max(mx, nums[i]^nums[j])
        return mx
    
    """ 2933. 高访问员工 """
    def findHighAccessEmployees(self, access_times: List[List[str]]) -> List[str]:
        name2times = defaultdict(list)
        for name, time in access_times:
            hour, minus = int(time[:2]), int(time[2:])
            name2times[name].append(hour*60+minus)
        names = []
        for name, times in name2times.items():
            times = sorted(times)
            for i in range(2, len(times)):
                if times[i] - times[i-2] < 60:
                    names.append(name)
                    break
        return names
    
    """ 2934. 最大化数组末位元素的最少操作次数 #medium 给定两个数组, 操作可以交换对应位置的元素, 要求每个数组都满足, 最后一个元素是其最大值
思路1: 
    定义 op1, op2 分别记录需要进行交换的次数
       """
    def minOperations(self, nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        if nums1[-1] > nums2[-1]: nums1, nums2 = nums2, nums1
        mx1, mx2 = nums1[-1], nums2[-1]
        op1 = 0     # 经过交换可以满足的
        op2 = 0     # 交换不交换都满足的
        for x,y in zip(nums1[:-1], nums2[:-1]):
            if x > mx2: return -1
            elif mx1 < x <= mx2:
                if y > mx1: return -1
                op1 += 1
            else:
                if y > mx2: return -1
                elif y <= mx1:
                    op2 += 1
        return min(op1, n-op1-op2)  # n-op1-op2: 交互最后一个元素

    """ 2935. 找出强数对的最大异或值 II #hard 定义 |x-y|<=min(x,y) 的数对是「强数对」, 求所有强数对的最大异或值
限制: n 5e4; x 1<<20
思路1: #二叉树 记录出现过的数字, 其实叫「0-1 trie」

[灵神](https://leetcode.cn/problems/maximum-strong-pair-xor-ii/solutions/2523213/0-1-trie-hua-dong-chuang-kou-pythonjavac-gvv2/)
    其实可以先排序! 
#字典树
1707. 与数组中元素的最大异或值 2359
1803. 统计异或值在范围内的数对有多少 2479
1938. 查询最大基因差 2503
2479. 两个不重叠子树的最大异或值（会员题）
    """
    def maximumStrongPairXor(self, nums: List[int]) -> int:
        class Node:
            def __init__(self):
                self.left = None
                self.right = None
                self.mx = None
                self.mn = None

            def add_value(self, val):
                self.val = val
                self.mn = val
                self.mx = val
        
            def update_value(self, val):
                self.mn = min(self.mn, val) if self.mn is not None else val
                self.mx = max(self.mx, val) if self.mx is not None else val

        def add_num(root, num):
            node = root
            for i in range(20, -1, -1):
                node.update_value(num)
                if num & (1<<i):
                    if node.right is None:
                        node.right = Node()
                    node = node.right
                else:
                    if node.left is None:
                        node.left = Node()
                    node = node.left
            node.add_value(num)

        def check(node:Node, num):
            for v in (node.mn, node.mx):
                if abs(v-num) <= min(v, num):
                    return True
            return False

        def query(root, num):
            node = root
            for i in range(20, -1, -1):
                if num & (1<<i):
                    if node.left is not None and check(node.left, num):
                        node = node.left
                    else:
                        node = node.right
                else:
                    if node.right is not None and check(node.right, num):
                        node = node.right
                    else:
                        node = node.left
            return node.mx ^ num

        root = Node()
        for num in nums:
            add_num(root, num)
        ans = 0
        for num in nums:
            ans = max(ans, query(root, num))
        return ans

sol = Solution()
result = [
    # sol.maximumStrongPairXor(nums = [1,2,3,4,5]),
    # sol.findHighAccessEmployees(access_times = [["cd","1025"],["ab","1025"],["cd","1046"],["cd","1055"],["ab","1124"],["ab","1120"]]),
    # sol.findHighAccessEmployees(access_times = [["d","0002"],["c","0808"],["c","0829"],["e","0215"],["d","1508"],["d","1444"],["d","1410"],["c","0809"]]),
    # sol.minOperations(nums1 = [1,2,7], nums2 = [4,5,3]),
    # sol.minOperations(nums1 = [2,3,4,5,9], nums2 = [8,8,4,4,4]),
    # sol.minOperations(nums1 = [1,5,4], nums2 = [2,5,3]),
    # sol.minOperations([9,12,2,4,13,1,8,17,14,11,15,14,8,18,1,20,20,6,14,10,1,10,9,3,20,19,18], [12,16,3,8,4,19,18,11,13,12,9,9,3,2,2,12,17,7,14,18,2,8,19,6,8,16,20]),
    sol.maximumStrongPairXor(nums = [1,2,3,4,5]),
    sol.maximumStrongPairXor(nums = [10,100]),
    sol.maximumStrongPairXor(nums = [500,520,2500,3000]),

]
for r in result:
    print(r)
