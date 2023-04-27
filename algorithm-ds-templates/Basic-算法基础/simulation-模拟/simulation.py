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
https://leetcode.cn/tag/simulation/problemset/

Easonsi @2023 """
class Solution:
    """ 0068. 文本左右对齐 #hard #simu 排版单词, 满足一定的要求, 具体见说明网页
给定一个单词数组和一个长度maxWidth，重新排版单词，使其成为每行恰好有maxWidth个字符，且左右两端对齐的文本。
[official](https://leetcode.cn/problems/text-justification/solution/wen-ben-zuo-you-dui-qi-by-leetcode-solut-dyeg/)
    """
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        wordlens = [len(w) for w in words]
        nwords = len(words)
        start = 0
        output = []
        while start <= nwords-1:
            acc = wordlens[start]
            p = start
            while p+1<=nwords-1 and acc+wordlens[p+1]+1 <= maxWidth:
                p += 1
                acc += wordlens[p]+1
            # [start, p] 之前的 word 作为一行
            n_words = p-start+1
            n_spaces = maxWidth-sum(wordlens[start:p+1])
            if n_words == 1:
                s = words[start] + ' '*n_spaces
            else:
                if p != nwords-1:
                    avg_spaces, q = divmod(n_spaces, (n_words-1))
                    s = ''
                    for i in range(q):
                        s += words[start+i] + ' '*(avg_spaces+1)
                    s += (' '*avg_spaces).join(words[start+q: p+1])
                else:
                    # 最后的几个 words
                    s = ' '.join(words[start: p+1]) + ' '*(n_spaces-(p-start))
            output.append(s)
            start = p+1
        return output

    """ 0043. 字符串相乘 #medium #simu #题型 给定两个数字字符串, 实现乘法
思路1: 枚举b的每一位, 模拟「竖式乘法」的方法计算乘积, 然后进行字符串加法
    关联「0415. 字符串相加」
    复杂度: O(mn + n^2)
思路2: 优化来用int数组存储结果
    上面, 字符串的加法操作比较繁琐, 我们直接用int数组来记录每一个数位的情况, 最后转为数字字符串
    复杂度: O(mn)
[lc](https://leetcode.cn/problems/multiply-strings/solution/zi-fu-chuan-xiang-cheng-by-leetcode-solution/)
    """
    def multiply(self, num1: str, num2: str) -> str:
        # 思路1: 枚举b的每一位, 模拟「竖式乘法」的方法计算乘积, 然后进行字符串加法
        if num1 == "0" or num2 == "0":
            return "0"
        ans = "0"
        m, n = len(num1), len(num2)
        for i in range(n - 1, -1, -1):
            add = 0
            y = int(num2[i])
            curr = ["0"] * (n - i - 1)
            for j in range(m - 1, -1, -1):
                product = int(num1[j]) * y + add
                curr.append(str(product % 10))
                add = product // 10
            if add > 0:
                curr.append(str(add))
            curr = "".join(curr[::-1])
            # 调用「0415. 字符串相加」
            ans = self.addStrings(ans, curr)
        return ans
    def addStrings(self, num1: str, num2: str) -> str:
        # 「0415. 字符串相加」
        i, j = len(num1) - 1, len(num2) - 1
        add = 0
        ans = list()
        while i >= 0 or j >= 0 or add != 0:
            x = int(num1[i]) if i >= 0 else 0
            y = int(num2[j]) if j >= 0 else 0
            result = x + y + add
            ans.append(str(result % 10))
            add = result // 10
            i -= 1
            j -= 1
        return "".join(ans[::-1])

    """ 0054. 螺旋矩阵 #medium #模拟 按照顺时针返回数组中所有元素 """
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        if not matrix or not matrix[0]:
            return list()

        rows, columns = len(matrix), len(matrix[0])
        order = list()
        left, right, top, bottom = 0, columns - 1, 0, rows - 1
        
        while left <= right and top <= bottom:
            # 每次循环一圈
            for column in range(left, right + 1):
                order.append(matrix[top][column])
            for row in range(top + 1, bottom + 1):
                order.append(matrix[row][right])
            # 只剩下一行/一列 的情况下, 下面是不需要的
            if left < right and top < bottom:
                for column in range(right - 1, left, -1):
                    order.append(matrix[bottom][column])
                for row in range(bottom, top, -1):
                    order.append(matrix[row][left])
            left, right, top, bottom = left + 1, right - 1, top + 1, bottom - 1
        return order
    
    
    
    
    
    

    
sol = Solution()
result = [
    sol.fullJustify(["What","must","be","acknowledgment","shall","be"], 16),
]
for r in result:
    print(r)
