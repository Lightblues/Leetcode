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

""" 
https://leetcode.cn/company/bytedance/problemset/
@2022 """
class Solution:
    """ 给定一个数组, 返回其中第三大的数 """
    
    """ DR两个派别在会议上依次投票. 在每一轮中, D阵营的可以将R的某一人永久禁言(无法参加本轮和后面的投票). 当某一轮中会议只剩下一个阵营时胜利. 问都在最优决策下获胜党.
限制: 1e4
思路1: #贪心, 每一个可投票的人, 禁言其后面第一个对方阵营的人.
    注意到, 先投票的人有着一定的优势. 因此需要让对方的人减少的同时阻止前面的人投票.
"""
    def predictPartyVictory(self, senate: str) -> str:
        # DR 阵营中还没有投票的人
        remainD, remainR = 0, 0
        ans = ""
        for c in senate:
            if c=='D':
                if remainR >0: remainR -=1
                else:   # remainR==0 无法对c禁言.
                    # 优先对后面的对方阵营禁言.
                    remainD +=1 
                    ans += 'D'
            else:
                if remainD>0: remainD-=1
                else: 
                    remainR+=1
                    ans += 'R'
        # remainD, remainR 可能还有剩余, 则最优决策是对下一轮中对方阵营先投票的人禁言.
        res = ""
        for c in ans:
            if c=='D':
                if remainR>0: remainR -=1
                else: res += 'D'
            else:
                if remainD>0: remainD-=1
                else: res += 'R'
        if len(set(res))==1: return 'Radiant' if res[0]=='R' else 'Dire'
        return self.predictPartyVictory(res)
        
    """ 0735. 行星碰撞 #medium
有左右两个方向运动的行星, 若两个行星发生碰撞, 质量较小的那一个发生爆炸. 问最后剩余的行星情况. (速度都相等). 限制: 数量 1e4
思路1: 顺序遍历, 用一个数组保留向右移动的行星 (可能发生碰撞的). 遍历过程中模拟碰撞.
"""
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        ans = []
        rights = []
        for a in asteroids:
            if a<0:
                while len(rights)>0 and -a>rights[-1]: rights.pop()
                if len(rights)==0: ans.append(a)
                else:
                    if rights[-1]==-a: rights.pop()
                    elif rights[-1]>-a: pass
            else: rights.append(a)
        return ans+rights

    
sol = Solution()
result = [
    # sol.predictPartyVictory("RD"),
    # sol.predictPartyVictory("RDD"),
    sol.asteroidCollision(asteroids = [5,10,-5]),
    sol.asteroidCollision(asteroids = [8,-8]),
]
for r in result:
    print(r)
