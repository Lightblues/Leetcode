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


Easonsi @2023 """
class Solution:
    """ 0136. 只出现一次的数字 #easy 一个数字中, 除了一个数字出现一次外, 其他数字都出现两次. 找到那个特殊值.
思路2: 进阶要求是使用 O(1) 的空间. 可以用到 xor 的性质!
"""
    def singleNumber(self, nums: List[int]) -> int:
        return reduce(xor, nums)
    
    """ 0137. 只出现一次的数字 II #medium 数组中, 除了一个数字出现一次外, 其他数字都出现三次. 找到那个特殊值. 
限制: 元素范围为 32位有符号整数
思路1: 利用 set 并求和
    时间复杂度: O(n); 空间复杂度: O(n)
思路2: 考虑每一位的计数
    对于那些出现三次的数字, 每个bit的元素之和是 0/3, 都是3的倍数! 
    因此, 对所有的bit求和, 那些不能被3整除的就是答案
    时间复杂度: O(nC), 其中C为数位长度 (32); 空间复杂度: O(1)
注意: 负数的位运算 见 [补码](https://zh.wikipedia.org/wiki/%E4%BA%8C%E8%A3%9C%E6%95%B8)
    对于负数, 还是按照补码的方式进行运算 (高位补1), 例如 -1<<1 = -2; -1>>10 = -1
    本题中, 假设答案是一个负数, 最高位需要进行特殊判断!
思路3: 使用两个位掩码: seen_once 和 seen_twice
    通过下面的操作, 可以完成: 原本两个mask都是0; 数字x出现一次, 被记录在 seen_once; 数字x出现两次, 被记录在 seen_twice; 数字x出现三次, 两个mask都被清零
    复杂度: 时间O(n), 空间O(1)
[官答](https://leetcode.cn/problems/single-number-ii/solution/zhi-chu-xian-yi-ci-de-shu-zi-ii-by-leetc-23t6/)
"""
    def singleNumber(self, nums):
        # 方法一：HashSet
        return (3 * sum(set(nums)) - sum(nums)) // 2
    
    def singleNumber(self, nums: List[int]) -> int:
        # 思路2: 考虑每一位的计数
        ans = 0
        for i in range(32):
            total = sum((num >> i) & 1 for num in nums)
            if total % 3:
                # Python 这里对于最高位需要特殊判断
                if i == 31:
                    ans -= (1 << i)
                else:
                    ans |= (1 << i)
        return ans
    def singleNumber(self, nums):
        # 方法三：位运算符：NOT，AND 和 XOR
        seen_once, seen_twice = 0, 0
        for num in nums:
            seen_once = ~seen_twice & (seen_once ^ num)
            seen_twice = ~seen_once & (seen_twice ^ num)
        return seen_once
    
    """ 0260. 只出现一次的数字 III #medium 数组中, 除了两个数字出现一次外, 其他数字都出现两次. 找到那两个特殊值. 
思路1: 将两个数字分到两组中, 转为 「0136. 只出现一次的数字」
    注意到, num1^num2 至少有一bit是1, 因此可以根据这一位, 将数组分成两组!
"""
    def singleNumber(self, nums: List[int]) -> List[int]:
        xorsum = 0
        for num in nums:
            xorsum ^= num
        
        lsb = xorsum & (-xorsum)    # 找到最低位的1
        type1 = type2 = 0
        for num in nums:
            if num & lsb:
                type1 ^= num
            else:
                type2 ^= num
        
        return [type1, type2]

    
sol = Solution()
result = [
    sol.singleNumber([-2,-2,1,1,4,1,4,4,-4,-2]),
]
for r in result:
    print(r)
