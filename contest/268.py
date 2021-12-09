from typing import List
import bisect
from collections import defaultdict

class Solution268:
    """ 2078. 两栋颜色不同且距离最远的房子
    给一个数字列表, 计算其中不同的两个数字间隔最大值

    输入：colors = [1,8,3,8,3]
    输出：4
    解释：上图中，颜色 1 标识成蓝色，颜色 8 标识成黄色，颜色 3 标识成绿色。
    两栋颜色不同且距离最远的房子是房子 0 和房子 4 。
    房子 0 的颜色是颜色 1 ，房子 4 的颜色是颜色 3 。两栋房子之间的距离是 abs(0 - 4) = 4 。

    下面的暴力求解也可以通过. 实际上,左右各遇到一个和另一端颜色不同的即可输出, 参见 go 实现. 
    """
    def maxDistance(self, colors: List[int]) -> int:
        ans = 0 
        for i, x in enumerate(colors): 
            if x != colors[0]: ans = max(ans, i)
            if x != colors[-1]: ans = max(ans, len(colors)-1-i)
        return ans 


    """ 2079. 给植物浇水
    输入：plants = [2,2,3,3], capacity = 5
    输出：14
    解释：从河边开始，此时水罐是装满的：
    - 走到植物 0 (1 步) ，浇水。水罐中还有 3 单位的水。
    - 走到植物 1 (1 步) ，浇水。水罐中还有 1 单位的水。
    - 由于不能完全浇灌植物 2 ，回到河边取水 (2 步)。
    - 走到植物 2 (3 步) ，浇水。水罐中还有 2 单位的水。
    - 由于不能完全浇灌植物 3 ，回到河边取水 (3 步)。
    - 走到植物 3 (4 步) ，浇水。
    需要的步数是 = 1 + 1 + 2 + 3 + 3 + 4 = 14 。

    输入：plants = [1,1,1,4,2,3], capacity = 4
    输出：30
    解释：从河边开始，此时水罐是装满的：
    - 走到植物 0，1，2 (3 步) ，浇水。回到河边取水 (3 步)。
    - 走到植物 3 (4 步) ，浇水。回到河边取水 (4 步)。
    - 走到植物 4 (5 步) ，浇水。回到河边取水 (5 步)。
    - 走到植物 5 (6 步) ，浇水。
    需要的步数是 = 3 + 3 + 4 + 4 + 5 + 5 + 6 = 30 。

    模拟行走, 累计即可. 
    """
    def wateringPlants(self, plants: List[int], capacity: int) -> int:
        result = 0; remains = capacity
        for i in range(len(plants)):
            if remains >= plants[i]:
                result +=1 
                remains -= plants[i]
            else:
                result += 2*i+1
                remains = capacity - plants[i]
        return result

    """ 2080. 区间内查询数字的频率
    请你实现 RangeFreqQuery 类：
    RangeFreqQuery(int[] arr) 用下标从 0 开始的整数数组 arr 构造一个类的实例。
    int query(int left, int right, int value) 返回子数组 arr[left...right] 中 value 的 频率 。

    输入：
    ["RangeFreqQuery", "query", "query"]
    [[[12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]], [1, 2, 4], [0, 11, 33]]
    输出：
    [null, 1, 2]
    解释：
    RangeFreqQuery rangeFreqQuery = new RangeFreqQuery([12, 33, 4, 56, 22, 2, 34, 33, 22, 12, 34, 56]);
    rangeFreqQuery.query(1, 2, 4); // 返回 1 。4 在子数组 [33, 4] 中出现 1 次。
    rangeFreqQuery.query(0, 11, 33); // 返回 2 。33 在整个子数组中出现 2 次。

    主要应对的查询情况, 为了优化较多的查询, 建立了对应数字的列表, 从而查询时候可以用二分查找. 
    """
    class RangeFreqQuery:
        def __init__(self, arr: List[int]):
            # self.arr = arr
            self.numList = defaultdict(list)
            for i,n in enumerate(arr):
                self.numList[n].append(i)

        def query(self, left: int, right: int, value: int) -> int:
            # count = 0
            # for i in self.arr[left: right+1]:
            #     if value == i:
            #         count += 1
            # return count
            # s = [i for i in self.arr[left:right+1] if i==value]
            # return len(s)
            targetList = self.numList[value]
            # 二分查找 left right，注意查询区间是包括左右index 的, 即 [left, righ]
            i = bisect.bisect(targetList, left - 1)
            j = bisect.bisect(targetList, right)
            return j-i
        
        # TODO 实现二分查找
        # def bisearch(nums: List, target: int, bigger: bool):
        #     left, right = 0, len(nums)
        #     while True:
        #         index = (left+right)//2

        # O(n) 直接遍历, 非二分查找, 不能 AC
        def query(self, left: int, right: int, value: int) -> int:
            records = self.record[value]
            if not records:
                return 0
            index1, index2 = 0, len(records)-1
            while index1<len(records) and records[index1]<left:
                index1 += 1
            while index2>=0 and records[index2]>right:
                index2 -= 1
            return index2-index1+1


    """ 2081. k 镜像数字的和
    一个 k 镜像数字 指的是一个在十进制和 k 进制下从前往后读和从后往前读都一样的 没有前导 0 的 正 整数。

    比方说，9 是一个 2 镜像数字。9 在十进制下为 9 ，二进制下为 1001 ，两者从前往后读和从后往前读都一样。
    相反地，4 不是一个 2 镜像数字。4 在二进制下为 100 ，从前往后和从后往前读不相同。
    给你进制 k 和一个数字 n ，请你返回 k 镜像数字中 最小 的 n 个数 之和 。
    """
    def kMirror(self, k: int, n: int) -> int:
        def isPalindrome(x: int) -> bool:
            # 判断 10进制回文数 x 是否为 k 进制回文
            # 转为 k 进制数组
            kNums = []
            while x:
                kNums.append(x%k)
                x //= k
            return kNums==kNums[::-1]
        # 每次搜索 [left, left*10) 位数不变
        left = 1
        cnt, cumsum = 0,0
        while cnt<n: 
            for op in [0,1]:        # 分别控制生成长度为 奇数、偶数 的回文数
                for i in range(left, left*10):
                    if cnt==n:
                        break
                    # 1234 -> 1234321
                    # 1234 -> 12344321
                    tmp = (i // 10) if op==0 else i
                    while tmp:
                        i = i*10+tmp%10
                        tmp //= 10
                    if isPalindrome(i):
                        cnt += 1
                        cumsum += i
            left *= 10
        return cumsum

    

class Solution269:
    """ 2089. 找出数组排序后的目标下标
 """
    def targetIndices(self, nums: List[int], target: int) -> List[int]:
        nums.sort()
        result =[]
        for i, n in enumerate(nums):
            if n == target:
                result.append(i)
            elif n > target:
                break
        return result

    """ 2090. 半径为 k 的子数组平均值 """
    def getAverages(self, nums: List[int], k: int) -> List[int]:
        result = [-1 for _ in range(len(nums))]
        if len(nums) < 2*k+1:
            return result
        cumsum = sum(nums[:2*k+1])
        result[k] = cumsum // (2*k+1)
        # out of time
        # for i in range(k, len(nums)-k):
        #     result[i] = sum(nums[i-k: i+k+1]) // (2*k+1)
        for i in range(k+1, len(nums)-k):
            cumsum = cumsum + nums[i+k] - nums[i-k-1]
            result[i] = cumsum // (2*k+1)
        return result

    """ 2091. 从数组中移除最大值和最小值 """
    def minimumDeletions(self, nums: List[int]) -> int:
        minIndex, maxIndex = 0,0
        for i in range(len(nums)):
            if nums[i] > nums[maxIndex]:
                maxIndex = i
            elif nums[i] < nums[minIndex]:
                minIndex = i
        index1, index2 = min(minIndex, maxIndex), max(minIndex, maxIndex)
        return min(max(index1, index2)+1, len(nums)-min(index1, index2), index1+1+len(nums)-index2)

    """ 2092. 找出知晓秘密的所有专家
    给你一个整数 n ，表示有 n 个专家从 0 到 n - 1 编号。另外给你一个下标从 0 开始的二维整数数组 meetings ，其中 meetings[i] = [xi, yi, timei] 表示专家 xi 和专家 yi 在时间 timei 要开一场会。一个专家可以同时参加 多场会议 。最后，给你一个整数 firstPerson 。
    专家 0 有一个 秘密 ，最初，他在时间 0 将这个秘密分享给了专家 firstPerson 。接着，这个秘密会在每次有知晓这个秘密的专家参加会议时进行传播。更正式的表达是，每次会议，如果专家 xi 在时间 timei 时知晓这个秘密，那么他将会与专家 yi 分享这个秘密，反之亦然。
    秘密共享是 瞬时发生 的。也就是说，在同一时间，一个专家不光可以接收到秘密，还能在其他会议上与其他专家分享。
    在所有会议都结束之后，返回所有知晓这个秘密的专家列表。你可以按 任何顺序 返回答案。

    输入：n = 6, meetings = [[0,2,1],[1,3,1],[4,5,1]], firstPerson = 1
    输出：[0,1,2,3]
    解释：
    时间 0 ，专家 0 将秘密与专家 1 共享。
    时间 1 ，专家 0 将秘密与专家 2 共享，专家 1 将秘密与专家 3 共享。
    因此，在所有会议结束后，专家 0、1、2 和 3 都将知晓这个秘密。
    """
    # 不知道为啥有bug, 放弃 —— 在特殊情况下复杂度较高
    def findAllPeople(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        # meetings = sorted(meetings, key=lambda x: x[2])
        time2meeting = defaultdict(list)
        for x,y,t in meetings:
            time2meeting[t].append((x,y))
        secretSet = set([0, firstPerson])
        def recc(meets):
            added = False
            random.shuffle(meets)
            for i, (x,y) in enumerate(meets):
                if x in secretSet or y in secretSet:
                    del meets[i]
                if x in secretSet and y not in secretSet:
                    secretSet.add(y)
                    added = True
                if y in secretSet and x not in secretSet:
                    secretSet.add(x)
                    added = True
            if added:
                recc(meets)
        for t, meets in sorted(time2meeting.items()):
            recc(meets)
        return list(secretSet)


    def findAllPeople2(self, n: int, meetings: List[List[int]], firstPerson: int) -> List[int]:
        meetings.sort(key=lambda x: x[2])
        secret = [False]*n
        secret[0] = secret[firstPerson] = True

        i = 0
        while i<len(meetings):
            # find meetings at same time
            j = i
            while j+1<len(meetings) and meetings[j+1][2]==meetings[j][2]:
                j+= 1
            # construct graph
            edges = defaultdict(list)
            for s,e,_ in meetings[i:j+1]:
                edges[s].append(e)
                edges[e].append(s)
            # propagate
            q = deque([e for e in edges.keys() if secret[e]])
            while q:
                u = q.popleft()
                for v in edges[u]:
                    if not secret[v]:
                        secret[v] = True
                        q.append(v)
            # update next i
            i = j+1
        return [i for i in range(len(secret)) if secret[i]]

sol = Solution268()
result = [
    sol.kMirror(2,5),
    sol.kMirror(3,7),
]
for r in result:
    print(r)