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

var results = [
    numEnclaves(
        (grid = [
            [0, 0, 0, 0],
            [1, 0, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
        ])
    ),
];
for (let r of results) {
    console.log(r);
}
