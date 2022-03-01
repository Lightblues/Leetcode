const _ = require("underscore");

/**
 * @param {number[][]} grid
 * @return {number}
 */
/* 1020. 飞地的数量
0 表示海洋 1 表示陆地, 定义无法通过陆地走到矩形的边界的陆地为「飞地」

输入：grid = [[0,0,0,0],[1,0,1,0],[0,1,1,0],[0,0,0,0]]
输出：3
解释：有三个 1 被 0 包围。一个 1 没有被包围，因为它在边界上。

来源：力扣（LeetCode）
链接：https://leetcode-cn.com/problems/number-of-enclaves
著作权归领扣网络所有。商业转载请联系官方授权，非商业转载请注明出处。

DFS 即可*/
var numEnclaves = function (grid) {
    var [m, n] = [grid.length, grid[0].length];
    var directions = [
        [0, 1],
        [0, -1],
        [1, 0],
        [-1, 0],
    ];
    var isValid = function (i, j) {
        return i >= 0 && i < m && j >= 0 && j < n;
    };
    var dfs = function (i, j) {
        if (grid[i][j] != 1) {
            return;
        }
        grid[i][j] = 2;
        for (let [dx, dy] of directions) {
            if (isValid(i + dx, j + dy)) {
                dfs(i + dx, j + dy);
            }
        }
    };
    for (let i = 0; i < m; i++) {
        dfs(i, 0);
        dfs(i, n - 1);
    }
    for (let j = 0; j < n; j++) {
        dfs(0, j);
        dfs(m - 1, j);
    }
    var result = 0;
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (grid[i][j] == 1) {
                result++;
            }
        }
    }
    return result;
};

/* 方法二: 写成并查集
并查集的核心: 维护一个 father 数组, 其中每个元素的值为其父节点的索引
实现 1. find 查找根; 2. union 合并两个节点; 3. same 判断两个节点是否同根 (并集)
在合并过程中, 利用 rank 来将较小的集合合并到较大的集合中, 并且更新 rank, 简化

此题中, 维护一个 onEdge 数组判断每个节点是为飞地. 注意每次总是更新父节点 (因为查询的时候, 总是先 find 跟节点, 然后判断是否相连)
*/
class UnionFind {
    constructor(grid) {
        const [m, n] = [grid.length, grid[0].length];
        this.parent = new Array(m * n).fill(0);
        this.onEdge = new Array(m * n).fill(false);
        this.rank = new Array(m * n).fill(0);
        for (let i = 0; i < m; i++) {
            for (let j = 0; j < n; j++) {
                if (grid[i][j] == 1) {
                    const index = i * n + j;
                    this.parent[index] = index;
                    if (i === 0 || i === m - 1 || j === 0 || j === n - 1) {
                        this.onEdge[index] = true;
                    }
                }
            }
        }
    }
    find(i) {
        if (this.parent[i] != i) {
            this.parent[i] = this.find(this.parent[i]);
        }
        return this.parent[i];
    }
    union(x, y) {
        const rootx = this.find(x);
        const rooty = this.find(y);
        if (rootx != rooty) {
            if (this.rank[rootx] > this.rank[rooty]) {
                this.parent[rooty] = rootx;
                this.onEdge[rootx] |= this.onEdge[rooty];
            } else if (this.rank[rootx] < this.rank[rooty]) {
                this.parent[rootx] = rooty;
                this.onEdge[rooty] |= this.onEdge[rootx];
            } else {
                this.parent[rooty] = rootx;
                this.rank[rootx]++;
                this.onEdge[rootx] |= this.onEdge[rooty];
            }
        }
    }
    ifOnEdge(i) {
        return this.onEdge[this.find(i)];
    }
}
var numEnclaves2 = function (grid) {
    const [m, n] = [grid.length, grid[0].length];
    const uf = new UnionFind(grid);
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (grid[i][j] === 1) {
                const index = i * n + j;
                // 注意, 仅需要两个方向即可! 而不是 DFS 中四个方向
                if (j + 1 < n && grid[i][j + 1] === 1) {
                    uf.union(index, index + 1);
                }
                if (i + 1 < m && grid[i + 1][j] === 1) {
                    uf.union(index, index + n);
                }
            }
        }
    }
    let enclaves = 0;
    for (let i = 0; i < m; i++) {
        for (let j = 0; j < n; j++) {
            if (grid[i][j] === 1 && !uf.ifOnEdge(i * n + j)) {
                enclaves++;
            }
        }
    }
    return enclaves;
};

/**
 * @param {string} text
 * @return {number}
 */
/* 1189. “气球” 的最大数量
 */
var maxNumberOfBalloons = function (text) {
    let map = {};
    for (let i = 0; i < text.length; i++) {
        if (map[text[i]]) {
            map[text[i]]++;
        } else {
            map[text[i]] = 1;
        }
    }
    let balloon = {};
    for (let char of "balloon") {
        balloon[char] = balloon[char] ? balloon[char] + 1 : 1;
    }
    let count = Infinity;
    function min(a, b) {
        return a < b ? a : b;
    }
    for (let char in balloon) {
        if (!map[char]) {
            return 0;
        }
        count = min(count, parseInt(map[char] / balloon[char]));
    }
    return count;
};

/**
 * @param {number[]} nums
 * @return {number}
 */
/* 540. 有序数组中的单一元素
有序数组中仅有一个元素为单一, 其他都有两个, 找出单一元素

你设计的解决方案必须满足 O(log n) 时间复杂度和 O(1) 空间复杂度。*/
var singleNonDuplicate0 = function (nums) {
    var before,
        flag = false;
    for (let num of nums) {
        if (num !== before) {
            if (flag) {
                return before;
            }
            flag = true;
            before = num;
        } else {
            flag = false;
        }
    }
    return before;
};
/* 注意到, 由于是有序数组中只有一个单一元素, 该单一元素的位置一定是在 偶数位 x
在x之前, 2i, 2i+1 相同, 在 x之后, 2i-1, 2i 相同 (注意以0开始) 
二分查找 */
var singleNonDuplicate = function (nums) {
    var left = 0,
        right = nums.length - 1;
    while (left < right) {
        var mid = Math.floor((left + right) / 2);
        // 当 mid 为偶数时, 比较 mid, mid+1; 当 mid 为奇数时, 比较 mid, mid-1; 可以统一写成 mid, mid^1
        if (nums[mid] === nums[mid ^ 1]) {
            left = mid + 1;
        } else {
            right = mid;
        }
    }
    return nums[left];
};

/** 1380. 矩阵中的幸运数
 * @param {number[][]} matrix
 * @return {number[]}
 */
/* 1380. 矩阵中的幸运数
给一个矩阵找出所有幸运数字: 定义幸运数字为, 该行最小, 该列最大的数字. */
var luckyNumbers = function (matrix) {
    [m, n] = [matrix.length, matrix[0].length];
    let res = [];
    for (let i = 0; i < m; i++) {
        let min = Infinity;
        let minIndex = -1;
        for (let j = 0; j < n; j++) {
            if (matrix[i][j] < min) {
                min = matrix[i][j];
                minIndex = j;
            }
        }
        let flag = true;
        for (let j = 0; j < m; j++) {
            if (matrix[j][minIndex] > min) {
                flag = false;
                break;
            }
        }
        if (flag) {
            res.push(min);
        }
    }
    return res;
};

/* 1719. 重构一棵树的方案数 hard
定义一颗树的祖先展开: 结果是一组 (x_i, y_i) 包括了一颗有根树中所有的祖先关系
例如, 对于 [[1,2],[2,3]] 重构是唯一的
而对于 [[1,2],[2,3],[1,3]], 可知对应的树有很多, 例如 1->2->3 就是一颗

现在给定一个数组 (祖先方向不定), 要求判断是否是一颗树的展开, 如果不是返回0, 结果是否唯一返回 1/2

from [here](https://leetcode-cn.com/problems/number-of-ways-to-reconstruct-a-tree/solution/zhong-gou-yi-ke-shu-de-fang-an-shu-by-le-36e1/)
分析节点度数:
假定给定的数组满足条件, 可知: 1. root 的读书为 n-1; 2. 若 (x,y) 为祖先关系, 则子节点 y 满足 degree[x]>=degree[y], 且 adj[x] \superset adj[y]; 3. 若 degree[x]=degree[y], 则两个节点一定是单链关系, 此时两个节点是可以互换的 (不唯一)
因此总结
1. 若 degree[x]>degree[y], 则 x 为祖先
2. 若 degree[x]<degree[y], 则 y 为祖先
3. 若 degree[x]=degree[y], 则结果不唯一

如何解题? 遍历节点, 构造度. 1. 首先检测是否存在根节点; 2. 然后对于每一个节点 x, 寻找其「父节点」 (从度数大于它的集合中找, 选其中度数最小的); 若找到的节点度数 =degree[x], 当所有节点都满足时说明结果不唯一. 

 */
/**
 * @param {number[][]} pairs
 * @return {number}
 */
var checkWays = function (pairs) {
    const adj = new Map();
    for (const p of pairs) {
        if (!adj.has(p[0])) {
            adj.set(p[0], new Set());
        }
        if (!adj.has(p[1])) {
            adj.set(p[1], new Set());
        }
        adj.get(p[0]).add(p[1]);
        adj.get(p[1]).add(p[0]);
    }
    // 找根节点
    let root = -1
    const entries = new Set()
    for (const entry of adj.entries()) {
        entries.add(entry)
    }
    for (const [node, neg] of entries) {
        if (neg.size === adj.size - 1) {
            root = node;
        }
    }
    if (root === -1) {
        return 0;
    }
    // 判断是否都有祖先节点
    let res = 1;
    for (const [node, neg] of entries) {
        if (root === node) {
            continue
        }
        const currDegree = neg.size;
        let parentNod = -1;
        let parentDegree = Number.MAX_SAFE_INTEGER;
        for (const neighbour of neg) {
            if (adj.has(neighbour) && adj.get(neighbour).size < parentDegree && adj.get(neighbour).size >= currDegree) {
                parentNod = neighbour;
                parentDegree = adj.get(neighbour).size;
            }
        }
        if (parentNod === -1) {
            return 0;
        }
        // 检测父节点是否包含所有孩子节点
        for (const neighbour of neg) {
            if (neighbour === parentNod) {
                continue;
            }
            if (!adj.get(parentNod).has(neighbour)) {
                return 0;
            }
        }
        if (parentDegree === currDegree) {
            res = 2;
        }
    }
    return res;
};

/* 688. 骑士在棋盘上的概率 medium
在一个 `n x n` 的国际象棋棋盘上，一个骑士从单元格 `(row, column)` 开始，并尝试进行 `k` 次移动。
求最后留在棋盘上的概率 (出去之后不再移动).

输入: n = 3, k = 2, row = 0, column = 0
输出: 0.0625
解释: 有两步(到(1,2)，(2,1))可以让骑士留在棋盘上。
在每一个位置上，也有两种移动可以让骑士留在棋盘上。
骑士留在棋盘上的总概率是0.0625。

维护一个 Map 记录当前步留在每个位置的概率. 初始化 (row, column) 的概率为 1.
 */
/**
 * @param {number} n
 * @param {number} k
 * @param {number} row
 * @param {number} column
 * @return {number}
 */
var knightProbability = function (n, k, row, column) {
    var directions = [
        [2, 1],
        [2, -1],
        [-2, 1],
        [-2, -1],
        [1, 2],
        [1, -2],
        [-1, 2],
        [-1, -2]
    ]
    var checkVaild = function (x, y) {
        return x >= 0 && x < n && y >= 0 && y < n
    }
    // 初始化. 这里复杂了, 实际上可以直接初始化 (row, column) 的概率为 1
    if (k == 0) {
        return (row >= 0 && row < n && column >= 0 && column < n) ? 1 : 0;
    }
    var probs = new Map();
    for (let [dx, dy] of directions) {
        let x = row + dx;
        let y = column + dy;
        if (checkVaild(x, y)) {
            if (!probs.has(x + ',' + y)) {
                probs.set(x + ',' + y, 1 / 8);
            } else {
                probs.set(x + ',' + y, probs.get(x + ',' + y) + 1 / 8);
            }
        }
    }
    // 模拟移动
    for (let i = 1; i < k; i++) {
        let nextProbs = new Map();
        for (let [key, value] of probs) {
            let [x, y] = key.split(',').map(x => parseInt(x));
            for (let [dx, dy] of directions) {
                let nx = x + dx;
                let ny = y + dy;
                if (checkVaild(nx, ny)) {
                    if (!nextProbs.has(nx + ',' + ny)) {
                        nextProbs.set(nx + ',' + ny, value / 8);
                    } else {
                        nextProbs.set(nx + ',' + ny, nextProbs.get(nx + ',' + ny) + value / 8);
                    }
                }
            }
        }
        probs = nextProbs;
    }
    var result = 0;
    for (let [key, value] of probs) {
        result += value;
    }
    return result;
};

/* 1791. 找出星型图的中心节点 easy */
/**
 * @param {number[][]} edges
 * @return {number}
 */
var findCenter = function (edges) {
    var firstEdge = edges[0];
    let [n1, n2] = edges[1];
    if (firstEdge.indexOf(n1) != -1) {
        return n1
    } else {
        return n2
    }
};



/* 969. 煎饼排序 medium
支持的操作是翻煎饼, 即反转 [0:i] 区间的煎饼.
返回给数组arr 排序的操作序列
 
输入：[3,2,4,1]
输出：[4,2,4,3]
解释：
我们执行 4 次煎饼翻转，k 值分别为 4，2，4，和 3。
初始状态 arr = [3, 2, 4, 1]
第一次翻转后（k = 4）：arr = [1, 4, 2, 3]
第二次翻转后（k = 2）：arr = [4, 1, 2, 3]
第三次翻转后（k = 4）：arr = [3, 2, 1, 4]
第四次翻转后（k = 3）：arr = [1, 2, 3, 4]，此时已完成排序。
 */
/**
 * @param {number[]} arr
 * @return {number[]}
 */
// 瞎几把实现, ⚠️ js 中的 sort 是原地操作!
var pancakeSort = function (arr) {
    sortedArr = [...arr].sort((a, b) => a - b); // js 中的 sort 是原地操作!
    let res = [];
    for (let i = arr.length - 1; i >= 0; i--) {
        // console.log(arr, sortedArr[i]);
        let max = arr.indexOf(sortedArr[i]);
        if (max != i) {
            res.push(max + 1);
            res.push(i + 1);
            arrLast = arr.slice(i + 1);
            arrFirst = arr.slice(0, i + 1);
            arrFirst = arrFirst.slice(max + 1).reverse().concat(arrFirst.slice(0, max + 1));
            arr = arrFirst.concat(arrLast);
        }
    }
    return res;
};
// https://leetcode-cn.com/problems/pancake-sorting/solution/jian-bing-pai-xu-by-leetcode-solution-rzzu/
var pancakeSort = function (arr) {
    const ret = [];
    for (let n = arr.length; n > 1; n--) {
        let index = 0;
        for (let i = 1; i < n; i++) {
            if (arr[i] >= arr[index]) {
                index = i;
            }
        }
        if (index === n - 1) {
            continue;
        }
        reverse(arr, index);
        reverse(arr, n - 1);
        ret.push(index + 1);
        ret.push(n);
    }
    return ret;
}
// 辅助函数, 翻转 arr[:end+1]
const reverse = (arr, end) => {
    for (let i = 0, j = end; i < j; i++, j--) {
        let temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
};

/* 0717. 1比特与2比特字符 `easy` 
第一种字符用 0 表示, 第二种字符用 10或11 两个比特表示
给定一个比特序列, 判断最后一个字符是否可能为一比特字符(第一种) (因为编码可能有多种?)
 
输入: bits = [1, 1, 1, 0]
输出: false
解释: 唯一的编码方式是两比特字符和两比特字符。
所以最后一个字符不是一比特字符。
 
思路1:
考虑: 1. 当最后一个比特为1时显然 false; 2. 最后一个比特为0, 则前溯, 累计有多少个连续的1, 若为奇数, false; 若为偶数, true.
思路2:
注意, 这种情况下编码是唯一的!!
*/
/**
 * @param {number[]} bits
 * @return {boolean}
 */
var isOneBitCharacter = function (bits) {
    var n = bits.length;
    if (bits[n - 1] !== 0) {
        return false;
    }
    var count = 0;
    for (var i = n - 2; i >= 0; i--) {
        if (bits[i] === 1) {
            count++;
        } else {
            break;
        }
    }
    if (count % 2 === 1) {
        return false;
    }
    return true;
};

/* 0838. 推多米诺 `medium`
给定一系列骨牌的初始状态: L,R,. 标志向左向右倒, 或者不动, 判断结束状态. 当一个牌分别受到左右两边的力时, 保持竖直.
 
自己用了极其繁琐的方式: 记录所有 L,R 牌的位置; 对于每个竖直的牌, 维护四个index分别记录其左右两边最靠近的起始向左向右的牌的index.
当 lright>lleft 时, 牌可能向右倒, 当 rleft<lright 时, 牌可能向左; 若上面两个条件都成立, 则根据距离判断. 繁琐的是要判断这些 index 是否存在.
为此, 写了 `findIndexBigger, findIndexSmaller(arr, startIndex, index)` 分别从 startIndex 出发, 在序列arr中找到大于index的最小值(小于index的最大值)
 */
/**
 * @param {string} dominoes
 * @return {string}
 */
var pushDominoes = function (dominoes) {
    var n = dominoes.length;
    var indexLeft = [],
        indexRight = [];
    for (var i = 0; i < n; i++) {
        if (dominoes[i] === 'L') {
            indexLeft.push(i);
        } else if (dominoes[i] === 'R') {
            indexRight.push(i);
        }
    }
    function findIndexBigger(arr, startIndex, index) {
        // 从指标 arr 中找到大于 index 的最小值
        var i = startIndex;
        if (arr.length === 0) {
            return -1;
        }
        while (i < arr.length && arr[i] < index) {
            i++;
        }
        if (i === arr.length) {
            return -1;
        }
        return i;
    }
    function findIndexSmaller(arr, startIndex, index) {
        // 从指标 arr 中找到小于 index 的最大值
        var i = startIndex;
        if (arr.length === 0) {
            return -1;
        }
        while (i < arr.length - 1 && arr[i + 1] < index) {
            i++;
        }
        return i;
    }
    var result = [];
    var ll = -1, lr = -1, rl = 0, rr = 0;
    var lindex, rindex;
    for (var i = 0; i < n; i++) {
        if (dominoes[i] !== '.') {
            result.push(dominoes[i]);
            continue;
        }
        // .
        rl = findIndexBigger(indexLeft, rl, i);
        rr = findIndexBigger(indexRight, rr, i);
        ll = findIndexSmaller(indexLeft, ll, i);
        lr = findIndexSmaller(indexRight, lr, i);
        lindex = undefined, rindex = undefined;
        if (lr !== -1) {
            if (ll === -1 || indexRight[lr] > indexLeft[ll]) {
                lindex = indexRight[lr];
            }
        }
        if (rl !== -1) {
            if (rr === -1 || indexRight[rr] > indexLeft[rl]) {
                rindex = indexLeft[rl];
            }
        }
        if (lindex !== undefined && rindex === undefined || lindex !== undefined && rindex !== undefined && (i - lindex) < (rindex - i)) {
            result.push('R');
        } else if (rindex !== undefined && lindex === undefined || lindex !== undefined && rindex !== undefined && (i - lindex) > (rindex - i)) {
            result.push('L');
        } else {
            result.push('.');
        }
    }
    return result.join("");

};


/* 1994. 好子集的数目 `hard`
给定一组数字, 都不大于30. 求满足条件的所有子集的数量, 条件为: 子集中所有数字的乘积可以 = 不同的质数的乘积.
 
输入：nums = [4,2,3,15]
输出：5
解释：好子集为：
- [2]：乘积为 2 ，可以表示为质数 2 的乘积。
- [2,3]：乘积为 6 ，可以表示为互不相同质数 2 和 3 的乘积。
- [2,15]：乘积为 30 ，可以表示为互不相同质数 2，3 和 5 的乘积。
- [3]：乘积为 3 ，可以表示为质数 3 的乘积。
- [15]：乘积为 15 ，可以表示为互不相同质数 3 和 5 的乘积。
 
[here](https://leetcode-cn.com/problems/the-number-of-good-subsets/solution/hao-zi-ji-de-shu-mu-by-leetcode-solution-ky65/)
由于数字都比较小, 可以罗列所有的质数 primes=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
对于一组数字, 它们所用到的质数可以通过状态压缩来表示, 即 01 表示以上10个质数用到了哪几个, 记为 mask
考虑 DP: 用 dp[i][mask] 表示只使用数字 2~i, 并且所用的数字质数为 mask, 这样的子集的数量.
状态转移方程: 若 数字i本身包含平方因子, 例如 4, 12 等, 则该数字无法采用, dp[i][mask] = dp[i-1][mask];
否则, 假设i包含的质数组合为 subset, 则 dp[i][mask] = dp[i-1][mask] + dp[i-1][mask\subset], 其中的 subset 必然是 mask 的子集, mask\subset 可以异或得到
因此, 从 i=2开始遍历到 30, 最后的结果即 sum(dp[30][1:])
需要注意的是数字 1, 其可以取任意数量, 因此初始化 df[1][0] = 2**freq[1]
 */
/**
 * @param {number[]} nums
 * @return {number}
 */
var numberOfGoodSubsets = function (nums) {
    var primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29];
    var mod = 10 ** 9 + 7;
    var maxValue = 30;

    var freq = new Array(maxValue + 1).fill(0);
    for (let num of nums) {
        freq[num] += 1;
    }
    var f = new Array(1 << primes.length).fill(0);
    // 数字1, 初始化
    // 不同于Python, 可以用 pow 指定mod, 这里要注意溢出!
    // f[0] = (2 ** freq[1]) % mod;
    f[0] = 1;
    for (let i = 0; i < freq[1]; i++) {
        f[0] = (f[0] * 2) % mod;
    }

    for (let i = 2; i <= maxValue; i++) {
        // 从2开始遍历
        var occ = freq[i];
        if (occ === 0) { continue }
        // 检查 i 的每个质因数是否均不超过 1 个
        var subset = 0, x = i;
        var check = true;
        for (let j = 0; j < primes.length; j++) {
            if (x % (primes[j] * primes[j]) === 0) {
                check = false;
                break;
            }
            if (x % primes[j] === 0) {
                subset |= 1 << j;
            }
        }
        if (!check) {
            continue
        }
        // DP
        for (let mask = (1 << primes.length) - 1; mask > 0; mask--) {
            if ((mask & subset) === subset) {
                f[mask] = (f[mask] + f[mask ^ subset] * occ) % mod;
            }
        }
    }
    var ans = 0;
    for (let mask = 1; mask < (1 << primes.length); mask++) {
        ans = (ans + f[mask]) % mod;
    }
    return ans;
};

/* 0917. 仅仅反转字母 `easy` */
/**
 * @param {string} s
 * @return {string}
 */
var reverseOnlyLetters = function (s) {
    var indexs = [];
    for (let i = 0; i < s.length; i++) {
        if (s[i] >= 'a' && s[i] <= 'z' || s[i] >= 'A' && s[i] <= 'Z') {
            indexs.push(i);
        }
    }
    var result = s.split("");
    for (let i = 0; i < indexs.length; i++) {
        result[indexs[i]] = s[indexs[indexs.length - i - 1]];
    }
    return result.join("");
}

/* 1706. 球会落何处 `medium`
用一个grid表示该位置挡板的方向, 从最上边的每一个位置放小球, 返回小球最后落在的位置, 若无法掉出来 (挡板呈现V字形) 则返回 -1.
注意球无法掉下来的条件: 出现V字形或者到达边界无法再往边界方向.
 */
/**
 * @param {number[][]} grid
 * @return {number[]}
 */
var findBall = function (grid) {
    var [m, n] = [grid.length, grid[0].length];
    var res = [];
    for (let i = 0; i < n; i++) {
        res.push(i);
    }
    for (let j = 0; j < m; j++) {
        for (let i = 0; i < n; i++) {
            var now = res[i];
            if (now === -1) {
                continue;
            }
            if (grid[j][now] === 1) {
                if (now < n - 1 && grid[j][now + 1] !== -1) {
                    res[i] = now + 1;
                } else {
                    res[i] = -1;
                }
            } else {
                if (now > 0 && grid[j][now - 1] !== 1) {
                    res[i] = now - 1;
                } else {
                    res[i] = -1;
                }
            }
        }
    }
    return res;
};

/* 2016. 增量元素之间的最大差值 `easy` */
var maximumDifference = function (nums) {
    var minNow = Number.MAX_VALUE,
        result = -1;
    for (let num of nums) {
        if (num > minNow) {
            result = Math.max(result, num - minNow);
        }
        if (num < minNow) {
            minNow = num;
        }
    }
    return result;
}

/**
 * @param {string} num1
 * @param {string} num2
 * @return {string}
 */
var complexNumberMultiply = function (num1, num2) {
    var [a, b] = num1.slice(0, num1.length - 1).split("+");
    var [c, d] = num2.slice(0, num2.length - 1).split("+");
    [a, b] = [parseInt(a), parseInt(b)];
    [c, d] = [parseInt(c), parseInt(d)];
    var x = a * c - b * d,
        y = a * d + b * c;
    return `${x}+${y}i`;
};

// ============================ results ============================
var results = [
    // numEnclaves(
    //     (grid = [
    //         [0, 0, 0, 0],
    //         [1, 0, 1, 0],
    //         [0, 1, 1, 0],
    //         [0, 0, 0, 0],
    //     ])
    // ),

    // maxNumberOfBalloons("balon"),
    // maxNumberOfBalloons("loonbalxballpoon"),
    // maxNumberOfBalloons("leetcode"),

    // _.min([1, 2, 3]),
    // singleNonDuplicate([3, 3, 7, 7, 10, 11, 11]),

    // luckyNumbers([
    //     [3, 7, 8],
    //     [9, 11, 13],
    //     [15, 16, 17],
    // ]),

    // checkWays([[1, 2], [2, 3], [1, 3]]),

    // knightProbability(n = 3, k = 2, row = 0, column = 0),


    // reverseOnlyLetters("ab-cd"),

    // pancakeSort([3, 2, 4, 1]),

    // isOneBitCharacter(bits = [1, 1, 1, 0]),

    // pushDominoes(dominoes = ".L.R...LR..L.."),
    // pushDominoes("RR.L"),
    // pushDominoes("R."),

    // numberOfGoodSubsets(nums = [1, 2, 3, 4]), // 6
    // numberOfGoodSubsets([4, 2, 3, 15]), // 5

    // findBall(grid = [[1, 1, 1, -1, -1], [1, 1, 1, -1, -1], [-1, -1, -1, 1, 1], [1, 1, 1, 1, -1], [-1, -1, -1, -1, -1]]),


    maximumDifference(nums = [7, 1, 5, 4]),

    complexNumberMultiply(num1 = "1+1i", num2 = "1+1i"),
    complexNumberMultiply(num1 = "1+-1i", num2 = "1+-1i"),

];
for (let r of results) {
    console.log(r);
}
