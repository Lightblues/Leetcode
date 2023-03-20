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
https://leetcode-cn.com/contest/biweekly-contest-95


@2022 """
class Solution:
    """ 6287. 根据规则将箱子分类 #easy 分类模拟题 """
    def categorizeBox(self, length: int, width: int, height: int, mass: int) -> str:
        L = 10000
        vol = length*width*height
        b = False
        h = False
        if length>=L or width>=L or height>=L or vol>=10**9: b=True
        if mass>=100: h=True
        if b and h: return "Both"
        elif b: return "Bulky"
        elif h: return "Heavy"
        else: return "Neither"
    
    """ 6289. 查询数组 Xor 美丽值 #medium #题型 #位运算
给定一个数组, 定义 (i,j,k) 三个下标的值为 `(nums[i] | nums[j]) & nums[k]`, 对于所有的下标组, 求它们的异或和. 
注意这里的ijk没有约束, 可以相等! 限制: n 1e5
思路1:
    先考虑单个k的异或和: 它和所有的 (i,j) 坐标组计算值, 再求异或. 
        注意到, 由于 (i,j),(j,i) 得到的结果是相同的, 因此异或结果为0!
        因此, 变成 `xor_i{ nums[i] & nums[k] } = xor_i{nums[i]} & nums[k]`
    然后对于 k进行累计求异或即可. 
"""
    def xorBeauty(self, nums: List[int]) -> int:
        _xor = reduce(operator.xor, nums)
        ans = 0
        for num in nums:
            ans ^= _xor & num
        return ans
    
    
    """ 2528. 最大化城市的最小供电站数目 #hard 给定一个数组表示每个城市供电站数量, 给定r表示每个发电站可以覆盖的范围为 [i-r,i+r]; 在新增最多k个的限制下, 要求最大化 min{每个城市可接受到的发电站数量}.
限制: n 1e5; r<n, k 1e9
思路1: #二分 + #贪心
    观察k的数量, 可以尝试二分.
    如何判断能够构造满足min值至少为x? 可以用贪心
    具体而言, #滑动窗口 考查每个城市所被覆盖的范围, 若没有被满足, 则在最右边贪心补上所需的发电站.
        细节: 注意由于在滑动过程中需要新增/修改发电站数量, 在被移除滑窗的时候也需要被删掉, 因此需要用格外的数组来进行记录!!
"""
    def maxPower(self, stations: List[int], r: int, k: int) -> int:
        pass

""" 6288. 找到数据流中的连续整数 #medium 简单的类实现 """
class DataStream:
    def __init__(self, value: int, k: int):
        self.value = value
        self.k = k
        self.acc = 0

    def consec(self, num: int) -> bool:
        if num==self.value: self.acc+=1
        else: self.acc=0
        return True if self.acc>=self.k else False
    
sol = Solution()
result = [
    # sol.categorizeBox(length = 1000, width = 35, height = 700, mass = 300),
    # sol.categorizeBox(length = 200, width = 50, height = 800, mass = 50),
#     testClass("""["DataStream", "consec", "consec", "consec", "consec"]
# [[4, 3], [4], [4], [4], [3]]"""),
    # sol.xorBeauty([1,4]),
    # sol.xorBeauty(nums = [15,45,20,2,34,35,5,44,32,30]),
    sol.maxPower(stations = [1,2,4,5,0], r = 1, k = 2),
    sol.maxPower(stations = [4,4,4,4], r = 0, k = 3),
    sol.maxPower([4,2],1,1),
]
for r in result:
    print(r)
