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
    """ 0075. 颜色分类 对于0/1/2三种元素排序, 时间 O(n)
见 [sw-循环不变量]
     """
    def sortColors(self, nums: List[int]) -> None:
        n = len(nums)
        p0 = 0      # 下一个要放 0 的位置
        p2 = n-1    # 下一个放 2 的位置
        # 循环指针
        i = 0
        while i <= p2:
            num = nums[i]
            if num == 0:
                nums[p0], nums[i] = nums[i], nums[p0]
                p0 += 1
            if num == 2:
                nums[p2], nums[i] = nums[i], nums[p2]
                p2 -= 1
            i += 1
    
    
    
    
    

    
sol = Solution()
result = [
    
]
for r in result:
    print(r)
