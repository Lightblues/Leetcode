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
https://leetcode.cn/contest/weekly-contest-318
讨论: https://leetcode.cn/circle/discuss/HhkSf4/view/pK06Qb/
T2滑动窗口经典. T3的两个堆结构也比较典型. T4 的DP比赛时没想出来有些菜.
@2022 """
class Solution:
    """ 6229. 对数组执行操作 #easy #模拟 """
    def applyOperations(self, nums: List[int]) -> List[int]:
        n = len(nums)
        for i in range(n-1):
            if nums[i]==nums[i+1]:
                nums[i]=2*nums[i]
                nums[i+1]=0
        idx = 0
        for i,x in enumerate(nums):
            if x!=0:
                nums[idx] = x
                idx += 1
        for i in range(idx, n):
            nums[i] = 0
        return nums
    
    """ 6230. 长度为 K 子数组中的最大和 #medium 对于数组的所有长度为k子数组, 求最大和, 要求子数组的每个元素不相同. 限制: k,n 1e5 #滑动窗口 复杂度 O(n) """
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = 0
        # 用字典计数, 这样不会超时
        cntK = Counter(nums[:k])
        s = sum(nums[:k])
        if len(cntK)==k: ans = max(ans, s)
        for i in range(k, n):
            s += nums[i] - nums[i-k]
            cntK[nums[i]] += 1
            cntK[nums[i-k]] -= 1
            if cntK[nums[i-k]]==0: del cntK[nums[i-k]]
            if len(cntK)==k: ans = max(ans, s)
        return ans
    
    """ 6231. 雇佣 K 位工人的总代价 #medium 需要雇佣k个工人, 每次筛选的方式是, 从前后各candidates个人共选择代价最小的. 限制: n 1e5, k 1e5 
思路1: 维护两个 #最小堆 记录前后 candidates 个工人, 每次选择最小的那个代价.
    细节: 避免讲一个元素重复加入到两个堆, 在push的时候注意两个指针的边界判断. 
    复杂度: O(k log(n))
"""
    def totalCost(self, costs: List[int], k: int, candidates: int) -> int:
        h1 = []
        h2 = []
        acc = 0
        # 两个指针来记录下一个元素. 
        l = 0; r = len(costs)-1
        # 初始化
        for i in range(candidates):
            heappush(h1, costs[l])
            l+=1
        for i in range(candidates):
            # # 避免重复加入左右两个堆
            if l<=r:
                heappush(h2, costs[r])
                r-=1
        # 遍历: 取出k个工人
        for _ in range(k):
            # 比较左右堆的最小元素
            mn1 = inf if not h1 else h1[0]
            mn2 = inf if not h2 else h2[0]
            if mn1<=mn2:    # <= 当两边的最小元素想等时, 取idx较小的那个
                acc += heappop(h1)
                if l<=r:
                    heappush(h1, costs[l])
                    l+=1
            else:
                acc += heappop(h2)
                if l<=r:
                    heappush(h2, costs[r])
                    r-=1
        return acc

    """ 6232. 最小移动总距离 #hard 有一组机器人和一组工厂, 机器人的位置各不相同, 工厂的位置也各不相同. 每个工厂 (p,limit) 最多修理limit个机器人. (题目保证了每个机器人都能被修理). 问机器人的最少移动距离和.
限制: 位置 +/-1e9. 机器人数 n 工厂数 m 100. 
思路0: 暴力搜索 f(i,j, k) 表示第i个机器人到第j个工厂, 这个工厂还剩余k个位置
    尝试了乱七八糟的剪枝... 结果还是 #TLE
    启发: 对于两个机器人 x<y, 所选的工厂 fx<=fy. 
思路1: #DP #背包
    记 `f[i,j]` 表示前i个工厂修复前j个机器人的最小分数. 
    递推: `f[i,j] = min{ cost(k...j) + f[i-1,k-1] }` 这里的cost是将 k...j 这些机器人都安排给第i个工厂的代价.
    复杂度: 状态数 mn, 每次尝试枚举limit, 也即机器人数n, 因此总体复杂度 O(mn^2) 
反思: 比赛的时候有点想歪了, 思路局限在搜索上, 针对 DP (背包) 问题还有待加强.
[灵神](https://leetcode.cn/problems/minimum-total-distance-traveled/solution/ji-yi-hua-sou-suo-by-endlesscheng-qctr/) 还给了 #记忆化 搜索的代码
关联: 1478. 安排邮筒 #hard
"""
    def minimumTotalDistance(self, robot: List[int], factory: List[List[int]]) -> int:
        factory = [i for i in factory if i[1]!=0]
        n,m = len(robot),len(factory)
        robot.sort()
        factory.sort()
        # 
        caps = [c for i,c in factory]
        for j in range(m-2,-1,-1):
            caps[j] += caps[j+1]
        ans = inf
        cache = defaultdict(lambda: inf)
        def f(i,j, k, cost=0):
            # 第i个机器人到第j个工厂, 这个工厂剩余k个位置
            # 剪枝 1) (i,j,k) 可能发生重复!
            if cache[(i,j,k)] <= cost: return
            cache[(i,j,k)] = cost
            nonlocal ans
            dist = abs(robot[i]-factory[j][0])
            cost += dist
            # 剪枝 2) 全局 ans
            if cost>=ans: return 
            if i==n-1:
                ans = min(ans, cost)
                return
            # 剪枝 3) 尝试失败. 因为若 i选择了后面的那个工厂, 可能导致后续的机器人所选工厂不是最优的. 
            # e.g. [9,11,99,101], [[10,1],[7,1],[14,1],[100,1],[96,1],[103,1]]
            # if j<m-1 and caps[j+1]>=n-i and abs(robot[i]-factory[j+1][0])<dist:
            #     return
            
            k -= 1
            if k>0: 
                f(i+1, j, k, cost)
            for jj in range(j+1,m):
                # 剪枝 3) 后面的工厂容量不够了
                if caps[jj] < n-1-i: break
                f(i+1, jj, factory[jj][1], cost)
        for j in range(m):
            f(0,j,factory[j][1],0)
        return ans
    def minimumTotalDistance(self, robot: List[int], factory: List[List[int]]) -> int:
        robot.sort(); factory.sort(key=lambda f: f[0])
        n,m = len(robot),len(factory)
        f = [0] + [inf]*n
        for x,limit in factory:
            # 事实上, j从后往前递归, 可以不用nf. 
            nf = [0] + [inf]*(n)
            for j in range(n):
                cost = 0
                mn = f[j+1]
                for i in range(limit):
                    if j-i<0: break
                    cost += abs(robot[j-i]-x)
                    mn = min(mn, cost+f[j-i])
                nf[j+1] = mn
            f = nf
        return f[-1]
    
    
    """ 1478. 安排邮筒 #hard 有一组房子在数轴上, 要在其中安排k个邮筒, 要求距离和最小. 限制: n 100, 位置 1e4
关联: 6232. 最小移动总距离 #hard
思路1: #DP
    记 `f[i,j]` 表示前i个邮筒负责前j个房子安排的最小距离和.
    递推: `f[i,j] = min{ cost[k..j] +f[i-1,k-1] }` 
        如何求安排连续的一组房子的代价 `cost[k..j]`? 显然可以选位置的中位数. 下面的 getCost(i,j) 递归实现. 
参见 [官答](https://leetcode.cn/problems/allocate-mailboxes/solution/an-pai-you-tong-by-leetcode-solution-t4oz/) 太长不想看
"""
    def minDistance(self, houses: List[int], k: int) -> int:
        houses.sort()
        n = len(houses)
        f = [0] + [inf]*(n)
        @lru_cache(None)
        def getCost(i,j):
            if i==j: return 0
            elif j==i+1: return houses[j]-houses[i]
            else: return getCost(i+1,j-1) + houses[j]-houses[i]
        for i in range(1,k+1):
            for j in range(n, 0, -1):
                for k in range(j-1, -1, -1):
                    cost = getCost(k,j-1)
                    f[j] = min(f[j], cost+f[k])
        return f[-1]
        
    
sol = Solution()
result = [
    # sol.applyOperations(nums = [1,2,2,1,1,0]),
    # sol.maximumSubarraySum(nums = [1,5,4,2,9,9,9], k = 3),
    # sol.maximumSubarraySum([4,4,4], 2),
    # sol.totalCost(costs = [17,12,10,2,7,2,11,20,8], k = 3, candidates = 4),
    # sol.totalCost(costs = [1,2,4,1], k = 3, candidates = 3),
    # sol.minimumTotalDistance(robot = [0,4,6], factory = [[2,2],[6,2]]),
    # sol.minimumTotalDistance(robot = [1,-1], factory = [[-2,1],[2,1]]),
    # sol.minimumTotalDistance([9,11,99,101], [[10,1],[7,1],[14,1],[100,1],[96,1],[103,1]]),
    # sol.minimumTotalDistance([789300819,-600989788,529140594,-592135328,-840831288,209726656,-671200998], [[-865262624,6],[-717666169,0],[725929046,2],[449443632,3],[-912630111,0],[270903707,3],[-769206598,2],[-299780916,4],[-159433745,5],[-467185764,3],[849991650,7],[-292158515,6],[940410553,6],[258278787,0],[83034539,2],[54441577,3],[-235385712,2],[75791769,3]]),
    # sol.minimumTotalDistance([9486709,305615257,214323605,282129380,763907021,-662831631,628054452,-132239126,50488558,381544523,-656107497,810414334,421675516,-304916551,571202823,478460906,-972398628,325714139,-86452967,660743346], [[-755430217,18],[382914340,2],[977509386,4],[94299927,9],[32194684,16],[-371001457,2],[-426296769,13],[-284404215,8],[-421288725,0],[-893030428,2],[291827872,17],[-766616824,8],[-730172656,17],[-722387876,1],[510570520,20],[756326049,7],[-242350340,14],[6585224,19],[-173457765,15]]),
    # sol.minimumTotalDistance([214638235,856879529,-969013166,-351484621,257375401,-80547616,518438404,-997287628,-273117503,521937307,975057367,465488898,-585542166,272304816,-561624182,570480701,392705648,-617269032,574464819,459492762,-782777452,677280078,-278094736,-415421399], [[321935623,24],[688621920,16],[457918764,23],[177135951,20],[838743003,16],[128256656,16],[844636873,19],[-555693914,4],[-823965352,19],[-566990966,19],[20757380,23],[-29163921,22],[370846310,11],[743154667,13],[-955988779,12],[100000756,1],[481077983,11],[461542541,2],[-17120695,12],[-839927181,3],[85595728,20],[-834326943,23]]),
    # sol.minimumTotalDistance([962255677,-762380105,610274894,287954409,-174071320,510854000,209588877,-627021703,929978413,-872247930,-254613561,-695693307,273170072,-129426337,258902041,-989276030,448027560,504198179,112451797,109792351,-322156405,-380712099,707713409,-472416523,728170436,-779134100,446380576,-812550074,-769951228,695511021,424224538,223803204,46344209,-15114572,-694291265,-383187880,-999006547,246881285,-818037168,543668069,668603845,158001964,576972324,120851165,-333849828,631376623,-396777663,-278402403,768654267,-292947840,-254013834,101637354,629916051,-113519946,-979293075,-69520082,-974399764,115721148,768431981,106384285,-593233852,-26727529,-177159837,341435688,-501779315,-77583181,198530612,-274592839,-4670352,-47596640,-103706810,-335160238,-836850602,788886075,336043023,587141203,-314677424,-963669904,90164672,279365649,764238393,889244647,-279030903,-980274141,452706496,-412429358,-359352345,-96367870,949411067], [[862501446,82],[130806691,39],[536699542,62],[960461717,30],[-66506845,35],[425475801,57],[-379948987,5],[-79176803,35],[791543774,64],[-896818851,70],[-714762162,70],[724321334,64],[-15419134,21],[-540512804,73],[-645047783,43],[-700555237,26],[884358537,3],[-338556156,88],[-686047305,71],[-968731566,69],[-238605164,32],[655598560,47],[-610222584,49],[443324453,59],[458880521,74],[178848810,9],[945417347,34],[-401726654,13],[492870083,82],[-698352865,45],[717554124,72],[-652972719,15],[774950957,76],[654106114,60],[987022832,42],[572527606,1],[-792322581,80],[74886721,5],[-10650224,78],[855010118,5],[829406390,52],[775843733,59],[136216918,35],[348488334,33],[-549569589,47],[216615365,39],[419335869,72],[678935972,43],[87293041,21],[605212671,41],[837466621,78],[-751548635,49],[268749781,7],[34102526,5],[205187289,39],[137453687,3],[-636914444,29],[-204800253,58],[-894087485,88],[713520819,2],[-643641067,29],[480615375,74],[516137558,32],[-232834387,51],[-845017501,77],[669128166,32],[71898632,15],[-588947881,78],[-428125224,47],[546355741,88],[-113754207,12],[700373809,56],[315929856,74],[-1032453,63],[91744921,23],[290716055,80],[958690681,51],[-46875217,45],[394398244,15],[906926938,48],[632776740,24],[-57761147,68],[-205738629,83],[-199178552,3],[365155321,5],[261708256,71],[-673282328,39],[25956262,84],[510346503,35],[324592030,89],[-222463178,8],[561735826,33],[-197197912,85],[-158885796,55],[108694393,80],[-82191069,68]]),
    sol.minDistance(houses = [2,3,5,12,18], k = 2),
    sol.minDistance(houses = [7,4,6,1], k = 1),
]
for r in result:
    print(r)
