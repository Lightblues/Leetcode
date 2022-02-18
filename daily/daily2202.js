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


];
for (let r of results) {
    console.log(r);
}
