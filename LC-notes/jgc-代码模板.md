# 算法题目模板

## 二分查找

整数二分中，将一个区间切分成两部分——左边与右边。

```c++
// 区间[l, r]被划分成[l, mid]和[mid + 1, r]时使用。即寻找右边区间的左端点，这时候check函数检验的是是否满足右边区间的性质。
int bsearch_1(int l, int r)
{
    while (l < r)
    {
        int mid = l + r >> 1;
        if (check(mid)) r = mid;    // check()判断mid是否满足性质
        else l = mid + 1;
    }
    return l;
}

// 区间[l, r]被划分成[l, mid - 1]和[mid, r]时使用。即寻找左边区间的右端点，这时候check函数检验的是是否满足左边区间的性质。
int bsearch_2(int l, int r)
{
    while (l < r)
    {
        int mid = l + r + 1 >> 1;
        if (check(mid)) l = mid;
        else r = mid - 1;
    }
    return l;
}
```

## 三分查找

用于求出单峰函数的极值点，与二分法基本思想类似，但每次操作需在当前区间$[l,r]$内任取两点$lmid, rmid(lmid<rmid)$。现在假设要求函数$f$的极小值点，$f$先减后增，如果$f(lmid) < f(rmid)$，则在$[rmid, r]$中函数必然递增，最小值所在点必然不在这一区间内，可以舍去这一区间，反之亦然。三分法每次操作会舍去两侧区间中的其中一个。为了减少三分法的操作次数，应使两侧区间尽可能大。因此，每一次操作时$lmid$和$rmid$分别取$mid-\varepsilon$和$mid+\varepsilon$是一个不错的选择。

```c++
int eps = 1;
while (r - l > eps) {
    int mid = (lmid + rmid) >> 1;
    lmid = mid - eps;
    rmid = mid + eps;
    if (f(lmid) < f(rmid))
        r = mid;
    else
        l = mid;
}
```

## 高精度计算

面对长度较大的大数字之间的运算，往往通过数组模拟运算规则进行计算来保证精度。

### 高精度加法

压位最多可以压9位

```c++
// 高精度加法
// C = A + B, A >= 0, B >= 0
vector<int> add(vector<int> &A, vector<int> &B)
{
    if (A.size() < B.size()) return add(B, A);

    vector<int> C;
    int t = 0;
    for (int i = 0; i < A.size(); i ++ )
    {
        t += A[i];
        if (i < B.size()) t += B[i];
        C.push_back(t % 10);
        t /= 10;
    }

    if (t) C.push_back(t);
    return C;
}
```

### 高精度减法

```c++
// 高精度减法
// C = A - B, 满足A >= B, A >= 0, B >= 0
vector<int> sub(vector<int> &A, vector<int> &B)
{
    vector<int> C;
    for (int i = 0, t = 0; i < A.size(); i ++ )
    {
        t = A[i] - t;
        if (i < B.size()) t -= B[i];
        C.push_back((t + 10) % 10);
        if (t < 0) t = 1;
        else t = 0;
    }

    while (C.size() > 1 && C.back() == 0) C.pop_back();
    return C;
}
```

### 高精度乘法

```c++
// 高精度乘低精度
// C = A * b, A >= 0, b > 0
vector<int> mul(vector<int> &A, int b)
{
    vector<int> C;
    int t = 0;
    for (int i = 0; i < A.size() || t; i ++ )
    {
        if (i < A.size()) t += A[i] * b;
        C.push_back(t % 10);
        t /= 10;
    }

    return C;
}
```

### 高精度除法

```c++
// 高精度除以低精度
// A / b = C ... r, A >= 0, b > 0
vector<int> div(vector<int> &A, int b, int &r)
{
    vector<int> C;
    r = 0;
    for (int i = A.size() - 1; i >= 0; i -- )
    {
        r = r * 10 + A[i];
        C.push_back(r / b);
        r %= b;
    }
    reverse(C.begin(), C.end());
    while (C.size() > 1 && C.back() == 0) C.pop_back();
    return C;
}
```

## 链表实现

单链表

```c++
void init() // 初始化
{
    head = -1;
    idx = 0;
}

void add_to_head(int x) // 将值x插入到头指针后面
{
    e[idx] = x, ne[idx] = head, head = idx, idx ++ ;
}

void add(int k, int x) // 将值x插入到第k个结点后面
{
    e[idx] = x, ne[idx] = ne[k], ne[k] = idx, idx ++ ;
}

void remove(int k) // 删除第k个结点
{
    ne[k] = ne[ne[k]];
}
```

双链表

```c++
void init()
{
    r[0] = 1, l[1] = 0; // 0表示左端点，1表示右端点
    idx = 2;
}

void add(int k, int x) // 在下标是k的点的右边插入x
{
    e[idx] = x;
    r[idx] = r[k];
    l[idx] = k;
    l[r[k]] = idx;
    r[k] = idx;
    idx ++ ;
}

void remove(int k) // 删除第k个点
{
    r[l[k]] = r[k];
    l[r[k]] = l[k];
}
```

## 单调栈与单调队列

单调栈：求一堆数中每个数最靠近它的最大或者最小值。与双指针算法类似，关键是从中中找出可以优化的性质。

单调队列：求一组数中滑动窗口的最大最小值。

```c++
// 栈
int stk[N], tt = 0;

stk[ ++ tt] = x; // 压栈
tt -- ; // 弹出一个数
stk[tt]; // 栈顶的值
if (tt > 0) 1; // 判断是否为空

//队列
int q[N], hh = 0, tt = -1;

q[ ++ tt] = x; // 入队
hh ++ ; // 出队
q[hh]; // 从队头弹出一个数
if (hh <= tt) 1; // 判断是否为空
```

## KMP算法

KMP算法就是解决字符串匹配问题的一个算法，其在暴力算法中进行优化，在每次匹配失败时，暴力做法是将模板串后移一位重新匹配，而这之前模板串与模式串已经有一部分是匹配好的，所以我们只需要将模板串移动到其当前下标对应的位置（匹配失败之前的模板子字符串中，如果其具有一致的最长前缀后缀，因为之前匹配中后缀是与原来的模式串匹配成功的，那么当我们移动模板串到其对应的前缀位置时，之前的子串也是保证匹配成功的），这样可以跳过大多数匹配失败的步骤，从而优化匹配过程。

```c++
#include <iostream>

using namespace std;

const int N = 1e5+10, M = 1e6+10;

int n, m; // n是模板串长度，m是模式串长度
char p[N], s[M]; // p是模板串，s是模式串
int ne[N]; // next数组，存储的是每个下标对应的匹配前缀值

int main()
{
    cin >> n >> p + 1 >> m >> s + 1;

    // 求next数组的过程
    for (int i = 2, j = 0; i <= n; i ++ )
    {
        while (j && p[i] != p[j + 1]) j = ne[j];
        if (p[i] == p[j + 1]) j ++ ;
        ne[i] = j;
    }

    // 匹配过程
    for (int i = 1, j = 0; i <= m; i ++ )
    {
        while (j && s[i] != p[j + 1]) j = ne[j];
        if (s[i] == p[j + 1]) j ++ ;
        if (j == n) // 匹配成功
        {
            cout << i-n << ' '; // 这里输出的是模式串中匹配成功开始的下标
            j = ne[j];
        }
    }

    return 0;
}
```

## Trie树

Trie树：高效的存储和查找字符串集合的数据结构，本质是前缀树。

```c++
int son[N][26], cnt[N], idx; // 下标是0的点，既是根节点，又是空节点。idx是当前插入不同字符串的个数，也是唯一下标，用来访问cnt的个数。
char str[N];

void insert(char str[])
{
    int p = 0;
    for (int i = 0; str[i]; i ++ )
    {
        int u = str[i] - 'a';
        if (!son[p][u]) son[p][u] = ++ idx;
        p = son[p][u];
    }
    cnt[p] ++ ;
}

int query(char str[])
{
    int p = 0;
    for (int i = 0; str[i]; i ++ )
    {
        int u = str[i] - 'a';
        if (!son[p][u]) return 0;
        p = son[p][u];
    }
    return cnt[p];
}

```

## 并查集

并查集可以快速的支持如下的操作（几乎$O(1)$）：

- 将两个集合合并
- 询问两个元素是否在一个集合当作

基本原理：每个集合用一棵树来表示。树根的编号就是整个集合的编号。每个节点存储它的父节点，`p[x]`表示 `x`的父节点。

问题1：如何判断树根：`if (p[x] == x)`
问题2：如何求 `x`的集合编号（复杂度主要来源）：`while (p[x] != x) x = p[x];`
问题3：如何合并两个集合：假设 `p[x]`是 `x`的集合编号，`p[y]`是 `y`的集合编号：`p[x] = y;`

如何优化：**路径压缩**与**按秩合并**（不常用）。

```c++
int p[N];

int find(int x) // 返回x的祖宗节点 + 路径压缩
{
    if (p[x] != x) p[x] = find(p[x]); // 路径压缩
    return p[x];
}
```

## 堆

堆（手写、以小根堆为例）需要支持如下操作：

- 插入一个数：`heap[ ++ size] = x; up(size);`
- 求集合当中的最小值：`heap[1];`
- 删除最小值：`heap[1] = heap[size]; size -- ; down(1);`
- 删除任意一个元素：`heap[k] = heap[size]; size -- ; down(k); up(k);`
- 修改任意一个元素：`heap[k] = x; down(k); up(k);`

堆本质是一个完全二叉树，使用一维数组存储。下标为$i$的左右儿子下标分别为$2i$与$2i+1$。

```c++
int h[N], ph[N], hp[N], size;
// ph是插入数在数组的下标，hp是数组下标对应的插入数

void heap_swap(int a, int b)
{
    swap(ph[hp[a]], ph[hp[b]]);
    swap(hp[a], hp[b]);
    swap(h[a], h[b]);
}

void down(int u)
{
    int t = u;
    if (u*2 <= size && h[u*2] < h[t]) t = u*2;
    if (u*2 + 1 <= size && h[u*2 + 1] < h[t]) t = u*2 + 1;
    if (u != t)
    {
        heap_swap(u, t);
        down(t);
    }
}

void up(int u)
{
    while (u/2 && h[u/2] > h[u])
    {
        heap_swap(u/2, u);
        u /= 2;
    }
}

for (int i = n/2; i; i -- ) down(i); // O(n)建堆
```

## 哈希表

哈希表的存储结构：开放寻址法、拉链法。

```c++
// 拉链法
int h[N], e[N], ne[N], idx;

// 向哈希表中插入一个数
void insert(int x)
{
    int k = (x % N + N) % N;
    e[idx] = x;
    ne[idx] = h[k];
    h[k] = idx ++ ;
}

// 在哈希表中查询某个数是否存在
bool find(int x)
{
    int k = (x % N + N) % N;
    for (int i = h[k]; i != -1; i = ne[i])
        if (e[i] == x)
            return true;

    return false;
}
```

```c++
// 开放寻址法
int h[N];

// 如果x在哈希表中，返回x的下标；如果x不在哈希表中，返回x应该插入的位置
int find(int x)
{
    int t = (x % N + N) % N;
    while (h[t] != null && h[t] != x)
    {
        t ++ ;
        if (t == N) t = 0;
    }
    return t;
}
```

字符串哈希方式：字符串前缀哈希法。核心思想：将字符串看成P进制数，P的经验值是131或13331，取这两个值的冲突概率低。小技巧：取模的数用2^64，这样直接用unsigned long long存储，溢出的结果就是取模的结果。

```c++
typedef unsigned long long ULL;
ULL h[N], p[N]; // h[k]存储字符串前k个字母的哈希值, p[k]存储 P^k mod 2^64

// 初始化
p[0] = 1;
for (int i = 1; i <= n; i ++ )
{
    h[i] = h[i - 1] * P + str[i];
    p[i] = p[i - 1] * P;
}

// 计算子串 str[l ~ r] 的哈希值
ULL get(int l, int r)
{
    return h[r] - h[l - 1] * p[r - l + 1];
}
```

## 树与图的存储

树是一种特殊的图，与图的存储方式相同。对于无向图中的边ab，存储两条有向边a->b，b->a。因此我们可以只考虑有向图的存储。

邻接矩阵：g[a][b]存储边a->b。
邻接表：

```c++
// 对于每个点k，开一个单链表，存储k所有可以走到的点。h[k]存储这个单链表的头结点
int h[N], e[N], ne[N], idx;

// 添加一条边a->b
void add(int a, int b)
{
    e[idx] = b, ne[idx] = h[a], h[a] = idx ++ ;
}
```

## 树与图的遍历

```c++
// DFS
bool st[N]
int e[N], ne[N]; // 点是否被遍历过的记录数组
void dfs(int u)
{
    st[u] = true; // st[u] 表示点u已经被遍历过
    for (int i = h[u]; i != -1; i = ne[i])
    {
        int j = e[i];
        if (!st[j]) dfs(j);
    }
}

// BFS
queue<int> q;
st[1] = true; // 表示1号点已经被遍历过
q.push(1);

while (q.size())
{
    int t = q.front();
    q.pop();

    for (int i = h[t]; i != -1; i = ne[i])
    {
        int j = e[i];
        if (!st[j])
        {
            st[j] = true; // 表示点j已经被遍历过
            q.push(j);
        }
    }
}
```

## 拓扑排序

只有有向图才会有拓扑序列，从而进行拓扑排序。

```c++
bool topsort()
{
    int hh = 0, tt = -1;

    // d[i] 存储点i的入度
    for (int i = 1; i <= n; i ++ )
        if (!d[i])
            q[ ++ tt] = i;

    while (hh <= tt)
    {
        int t = q[hh ++ ];

        for (int i = h[t]; i != -1; i = ne[i])
        {
            int j = e[i];
            if (-- d[j] == 0)
                q[ ++ tt] = j;
        }
    }

    // 如果所有点都入队了，说明存在拓扑序列；否则不存在拓扑序列。
    return tt == n - 1;
}
```

## 最短路问题算法

常见的最短路问题可以分为两大类：单源最短路（一个点到其他所有点的最短路）与多源汇最短路（起点与终点不确定）。其中单源最短路还可以分成两类问题：一类是所有边权都是正数的情况、一类是存在负权边的情况。只有正数权边有两种算法解决：朴素Dijkstra算法（适合稠密图）与堆优化版的Dijkstra算法（适合稀疏图）。存在负权边有两种算法解决：Bellman-Ford算法和SPFA算法。对于多源汇最短路只有一种算法解决：Floyd算法。

```c++
// 朴素Dijkstra算法
int g[N][N];  // 存储每条边，因为是稠密图
int dist[N];  // 存储1号点到每个点的最短距离
bool st[N];   // 存储每个点的最短路是否已经确定

// 求1号点到n号点的最短路，如果不存在则返回-1
int dijkstra()
{
    memset(dist, 0x3f, sizeof dist);
    dist[1] = 0;

    for (int i = 0; i < n - 1; i ++ )
    {
        int t = -1; // 在还未确定最短路的点中，寻找距离最小的点
        for (int j = 1; j <= n; j ++ )
            if (!st[j] && (t == -1 || dist[t] > dist[j]))
                t = j;

        // 用t更新其他点的距离
        for (int j = 1; j <= n; j ++ )
            dist[j] = min(dist[j], dist[t] + g[t][j]);

        st[t] = true;
    }

    if (dist[n] == 0x3f3f3f3f) return -1;
    return dist[n];
}

// 堆优化版Dijkstra算法
typedef pair<int, int> PII;

int n;  // 点的数量
int h[N], w[N], e[N], ne[N], idx;   // 邻接表存储所有边，因为是稀疏图
int dist[N];    // 存储所有点到1号点的距离
bool st[N]; // 存储每个点的最短距离是否已确定

// 求1号点到n号点的最短距离，如果不存在，则返回-1
int dijkstra()
{
    memset(dist, 0x3f, sizeof dist);
    dist[1] = 0;
    priority_queue<PII, vector<PII>, greater<PII>> heap; // 小根堆
    heap.push({0, 1});  // first存储距离，second存储节点编号

    while (heap.size())
    {
        auto t = heap.top();
        heap.pop();

        int ver = t.second, distance = t.first;

        if (st[ver]) continue;
        st[ver] = true;

        for (int i = h[ver]; i != -1; i = ne[i])
        {
            int j = e[i];
            if (dist[j] > distance + w[i])
            {
                dist[j] = distance + w[i];
                heap.push({dist[j], j});
            }
        }
    }

    if (dist[n] == 0x3f3f3f3f) return -1;
    return dist[n];
}
```

```c++
// Bellman-Ford算法
int n, m; // n表示点数，m表示边数
int dist[N]; // dist[x]存储1到x的最短路距离

struct Edge // 边，a表示出点，b表示入点，w表示边的权重
{
    int a, b, w;
}edges[M];

// 求1到n的最短路距离，如果无法从1走到n，则返回-1。
int bellman_ford()
{
    memset(dist, 0x3f, sizeof dist);
    dist[1] = 0;

    // 如果第n次迭代仍然会松弛三角不等式，就说明存在一条长度是n+1的最短路径，由抽屉原理，路径中至少存在两个相同的点，说明图中存在负权回路。
    for (int i = 0; i < n; i ++ )
    {
        for (int j = 0; j < m; j ++ )
        {
            int a = edges[j].a, b = edges[j].b, w = edges[j].w;
            if (dist[b] > dist[a] + w)
                dist[b] = dist[a] + w;
        }
    }

    if (dist[n] == 0x3f3f3f3f) return -1;
    return dist[n];
}
```

```c++
// SPFA算法（队列优化的Bellman-Ford算法）
int n;  // 总点数
int h[N], w[N], e[N], ne[N], idx;   // 邻接表存储所有边
int dist[N];    // 存储每个点到1号点的最短距离
bool st[N]; // 存储每个点是否在队列中

// 求1号点到n号点的最短路距离，如果从1号点无法走到n号点则返回-1
int spfa()
{
    memset(dist, 0x3f, sizeof dist);
    dist[1] = 0;

    queue<int> q;
    q.push(1);
    st[1] = true; // st表示点是否在队列中

    while (q.size())
    {
        auto t = q.front();
        q.pop();

        st[t] = false;

        for (int i = h[t]; i != -1; i = ne[i])
        {
            int j = e[i];
            if (dist[j] > dist[t] + w[i])
            {
                dist[j] = dist[t] + w[i];
                if (!st[j]) // 如果队列中已存在j，则不需要将j重复插入
                {
                    q.push(j);
                    st[j] = true;
                }
            }
        }
    }

    if (dist[n] == 0x3f3f3f3f) return -1;
    return dist[n];
}

// SPFA判断是否存在负环
int n; // 总点数
int h[N], w[N], e[N], ne[N], idx; // 邻接表存储所有边
int dist[N], cnt[N]; // dist[x]存储1号点到x的最短距离，cnt[x]存储1到x的最短路中经过的点数
bool st[N]; // 存储每个点是否在队列中

// 如果存在负环，则返回true，否则返回false。
bool spfa()
{
    // 不需要初始化dist数组
    // 原理：如果某条最短路径上有n个点（除了自己），那么加上自己之后一共有n+1个点，由抽屉原理一定有两个点相同，所以存在环。

    queue<int> q;
    for (int i = 1; i <= n; i ++ )
    {
        q.push(i);
        st[i] = true;
    }

    while (q.size())
    {
        auto t = q.front();
        q.pop();

        st[t] = false;

        for (int i = h[t]; i != -1; i = ne[i])
        {
            int j = e[i];
            if (dist[j] > dist[t] + w[i])
            {
                dist[j] = dist[t] + w[i];
                cnt[j] = cnt[t] + 1;
                if (cnt[j] >= n) return true; // 如果从1号点到x的最短路中包含至少n个点（不包括自己），则说明存在环
                if (!st[j])
                {
                    q.push(j);
                    st[j] = true;
                }
            }
        }
    }

    return false;
}
```

```c++
// Floyd算法
//初始化：
for (int i = 1; i <= n; i ++ )
    for (int j = 1; j <= n; j ++ )
        if (i == j) d[i][j] = 0;
        else d[i][j] = INF;

// 算法结束后，d[a][b]表示a到b的最短距离
void floyd()
{
    for (int k = 1; k <= n; k ++ )
        for (int i = 1; i <= n; i ++ )
            for (int j = 1; j <= n; j ++ )
                d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
}
```

## 最小生成树

最小生成树问题一般有两个算法：Prim算法与Kruskal算法。Prim算法有稀疏图和稠密图两种版本，稠密图使用朴素版Prim，稀疏图使用堆优化版Prim。

```c++
// 朴素版Prim
int n; // n表示点数
int g[N][N]; // 邻接矩阵，存储所有边
int dist[N]; // 存储其他点到当前最小生成树的距离
bool st[N]; // 存储每个点是否已经在生成树中


// 如果图不连通，则返回INF(值是0x3f3f3f3f), 否则返回最小生成树的树边权重之和
int prim()
{
    memset(dist, 0x3f, sizeof dist);

    int res = 0;
    for (int i = 0; i < n; i ++ )
    {
        int t = -1;
        for (int j = 1; j <= n; j ++ )
            if (!st[j] && (t == -1 || dist[t] > dist[j]))
                t = j;

        if (i && dist[t] == INF) return INF;

        if (i) res += dist[t];
        st[t] = true;

        for (int j = 1; j <= n; j ++ ) dist[j] = min(dist[j], g[t][j]);
    }

    return res;
}
```

```c++
// Kruskal算法
int n, m; // n是点数，m是边数
int p[N]; // 并查集的父节点数组

struct Edge // 存储边
{
    int a, b, w;

    bool operator< (const Edge &W)const
    {
        return w < W.w;
    }
}edges[M];

int find(int x) // 并查集核心操作
{
    if (p[x] != x) p[x] = find(p[x]);
    return p[x];
}

int kruskal()
{
    sort(edges, edges + m);

    for (int i = 1; i <= n; i ++ ) p[i] = i;    // 初始化并查集

    int res = 0, cnt = 0;
    for (int i = 0; i < m; i ++ )
    {
        int a = edges[i].a, b = edges[i].b, w = edges[i].w;

        a = find(a), b = find(b);
        if (a != b) // 如果两个连通块不连通，则将这两个连通块合并
        {
            p[a] = b;
            res += w;
            cnt ++ ;
        }
    }

    if (cnt < n - 1) return INF;
    return res;
}
```

## 二分图

二分图主要有两种算法：染色法何匈牙利算法。染色法可以判断一个图是否是二分图，使用了图论的经典结论：一个图是二分图当且仅当图可以被二染色。一个图是二分图当且仅当图中不含奇数环，从而可以唯一二染色。匈牙利算法可以在二分图中成功匹配中匹配最大的数量。

```c++
int n; // n表示点数
int h[N], e[M], ne[M], idx; // 邻接表存储图
int color[N]; // 表示每个点的颜色，-1表示未染色，0表示白色，1表示黑色

// 参数：u表示当前节点，father表示当前节点的父节点（防止向树根遍历），c表示当前点的颜色
bool dfs(int u, int father, int c)
{
    color[u] = c;
    for (int i = h[u]; i != -1; i = ne[i])
    {
        int j = e[i];
        if (color[j] == -1)
        {
            if (!dfs(j, u, !c)) return false;
        }
        else if (color[j] == c) return false;
    }

    return true;
}

bool check()
{
    memset(color, -1, sizeof color);
    bool flag = true;
    for (int i = 1; i <= n; i ++ )
        if (color[i] == -1)
            if (!dfs(i, -1, 0))
            {
                flag = false;
                break;
            }
    return flag;
}
```

```c++
// 匈牙利算法
int n; // n表示点数
int h[N], e[M], ne[M], idx; // 邻接表存储所有边
int match[N]; // 存储每个点当前匹配的点
bool st[N]; // 表示每个点是否已经被遍历过

bool find(int x)
{
    for (int i = h[x]; i != -1; i = ne[i])
    {
        int j = e[i];
        if (!st[j])
        {
            st[j] = true;
            if (match[j] == 0 || find(match[j]))
            {
                match[j] = x;
                return true;
            }
        }
    }
    return false;
}

// 求最大匹配数
int res = 0;
for (int i = 1; i <= n; i ++ )
{
    memset(st, false, sizeof st);
    if (find(i)) res ++ ;
}
```

## 数学知识

质数的知识也常常出现在算法题目中，主要有试除法$O(\sqrt{n})$判定质数、试除法$O(\sqrt{n})$做质因数分解、朴素筛法$O(n\log n)$统计前n个数中的质数个数、埃氏筛法$O(n\log \log n)$统计前n个数中的质数个数、线性筛法$O(n)$统计前n个数中的质数个数。

```c++
// 试除法判断质数：从整数2到根号n来判断能不能整除n
bool is_prime(int n)
{
    if (n < 2) return false;
    for (int i = 2; i <= n / i; i ++ )
        if (n % i == 0)
            return false;
    return true;
}
```

```c++
// 试除法分解质因数：从2到根号n枚举质因数，如果n中有因子i就统计因子i的个数
void divide(int n)
{
    for (int i = 2; i <= n / i; i ++ )
        if (n % i == 0)
        {
            int s = 0;
            while (n % i == 0) n /= i, s ++ ;
            cout << i << ' ' << s << endl;
        }
    if (n > 1) cout << n << ' ' << 1 << endl;
}
```

```c++
// 朴素筛法
int primes[N], cnt; // primes[]存储所有素数
bool st[N]; // st[x]存储x是否被筛掉

void get_primes(int n)
{
    for (int i = 2; i <= n; i ++ )
    {
        if (st[i]) continue;
        primes[cnt ++ ] = i;
        for (int j = i; j <= n; j += i)
            st[j] = true;
    }
}

// 线性筛法：每个数n只会被n的最小质因子筛掉
int primes[N], cnt; // primes[]存储所有素数
bool st[N]; // st[x]存储x是否被筛掉

void get_primes(int n)
{
    for (int i = 2; i <= n; i ++ )
    {
        if (!st[i]) primes[cnt ++ ] = i;
        for (int j = 0; primes[j] <= n / i; j ++ )
        {
            st[primes[j] * i] = true;
            if (i % primes[j] == 0) break;
        }
    }
}
```

约数同样会在题目中出现，一般有试除法$O(\sqrt{n})$求一个数的所有约数、约数个数（基于算术基本定理，如果关注的数$N$有质因数分解为$N = p_1^{\alpha_1}p_2^{\alpha_2}\cdots p_k^{\alpha_k}$，则其所有约数个数为$\prod_{i=1}^k (\alpha_i+1)$）、约数之和（$\prod_{i=1}^k \sum_{j=1}^{\alpha_i} p_i^j$）。

```c++
// 试除法求一个数的所有约数
vector<int> get_divisors(int x)
{
    vector<int> res;
    for (int i = 1; i <= x / i; i ++ )
        if (x % i == 0)
        {
            res.push_back(i);
            if (i != x / i) res.push_back(x / i);
        }
    sort(res.begin(), res.end());
    return res;
}
```

欧几里得算法$O(\log n)$用来求两个数的最大公约数，也叫辗转相除法，即$(a,b) = (a, b \mod a)$。

```c++
// 欧几里得算法，也可以调用库函数__gcd(a, b)，效率差不多
int gcd(int a, int b)
{
    return b ? gcd(b, a % b) : a;
}
```

欧拉函数：$1\sim N$中与$N$互质的数的个数，记作$\phi(N)$，由算术基本定理，假设$N = p_1^{\alpha_1} p_2^{\alpha_2} \cdots p_m^{\alpha_m}$，则$\phi(N) = N \times \frac{p_1-1}{p_1}\times \frac{p_2-1}{p_2}\times\cdots\times \frac{p_m-1}{p_m}$。筛法可以求1到n中每个数的欧拉函数$O(n)$。同时也有欧拉定理：若$a$与$n$互质，则$a^{\phi(n)} \equiv 1(\mod n)$。

```c++
// 欧拉函数
int phi(int x)
{
    int res = x;
    for (int i = 2; i <= x / i; i ++ )
        if (x % i == 0)
        {
            res = res / i * (i - 1);
            while (x % i == 0) x /= i;
        }
    if (x > 1) res = res / x * (x - 1);

    return res;
}

// 筛法求欧拉函数
int primes[N], cnt; // primes[]存储所有素数
int phi[N];   // 存储每个数的欧拉函数
bool st[N]; // st[x]存储x是否被筛掉


void get_eulers(int n)
{
    euler[1] = 1;
    for (int i = 2; i <= n; i ++ )
    {
        if (!st[i])
        {
            primes[cnt ++ ] = i;
            phi[i] = i - 1;
        }
        for (int j = 0; primes[j] <= n / i; j ++ )
        {
            int t = primes[j] * i;
            st[t] = true;
            if (i % primes[j] == 0)
            {
                phi[t] = phi[i] * primes[j]; // 因为质因子没有变化只是次数变化，这不影响欧拉函数的计算，只需要更改N即可
                break;
            }
            phi[t] = phi[i] * (primes[j] - 1); // 因为质因子只变化了一个p_j，其余次数变化，只需要更改N与增加一个1-1/p_j这就是乘以了p_j-1
        }
    }
}
```

快速幂常用来求解问题$a^k \mod p$的结果，其时间复杂度为$O(\log k)$。算法核心是首先预处理出$a^{2^i} \mod p$的结果，其中$i = 0, 1 ,\cdots,\log k$，然后将其乘起来组合成$a^k$即可。

```c++
// 快速幂算法
int qmi(int a, int k, int p)
{
    int res = 1;
    while (k)
    {
        if (k & 1) res = (long long)res * a % p; // 取k的二进制表示计算
        a = (long long)a * a % p; // 预处理
        k >>= 1;
    }
    return res;
}
```

裴蜀定理：给定一对正整数$a,b$，一定存在非零整数$x,y$使得$ax+by = (a,b)$。扩展欧几里得算法：求$x,y$使得$ax+by = (a,b)$。如果有一组解$x_0, y_0$满足$ax_0+by_0=(a,b)$，则通解为$x = x_0 - \frac{b}{d}k,y=y_0+\frac{a}{d}k,k\in \mathbb{Z}$。

```c++
// 扩展欧几里得算法
int exgcd(int a, int b, int x, int y)
{
    if (!b)
    {
        x = 1, y = 0;
        return a;
    }
    int d = exgcd(b, a%b, y, x);
    y -= (a/b)*x;
    return d;
}
```

中国剩余定理：给定两两互质的数$m_1, m_2, \cdots, m_k$，线性同余方程组$x \equiv a_i(\mod m_i), i = 1, 2, \cdots, k$的解可以给出，记$M = \prod_{i=1}^k m_i$，$M_i = \frac{M}{m_i}$，$M_i^{-1}$为$M_i$模$m_i$的逆元，则解为$x = \sum_{i=1}^k a_i M_i M_i^{-1}$。

高斯消元法：求解线性方程组的方法，通过对方程组做初等行变换化为阶梯型矩阵从而得到解。

```c++
// 返回值0表示唯一解，1表示无穷解，2表示无解
int gauss()
{
    int c, r;
    for (c = 0, r = 0; c < n; c ++ )
    {
        int t = r;
        for (int i = r; i < n; i ++ )
            if (fabs(a[i][c]) > fabs(a[t][c]))
                t = i;

        if (fabs(a[t][c]) < eps) continue;

        for (int i = c; i <= n; i ++ ) swap(a[t][i], a[r][i]);
        for (int i = n; i >= c; i -- ) a[r][i] /= a[r][c];
        for (int i = r + 1; i < n; i ++ )
            if (fabs(a[i][c]) > eps)
                for (int j = n; j >= c; j -- )
                    a[i][j] -= a[r][j] * a[i][c];

        r ++ ;
    }

    if (r < n)
    {
        for (int i = r; i < n; i ++ )
            if (fabs(a[i][n]) > eps)
                return 2;
        return 1;
    }

    for (int i = n - 1; i >= 0; i -- )
        for (int j = i + 1; j < n; j ++ )
            a[i][n] -= a[i][j] * a[j][n];

    return 0;
}
```

组合数：$C_a^b = \frac{a!}{b!(a-b)!}$。数据量不大时可以预处理：$C_a^b = C_{a-1}^b + C_{a-1}^{b-1}$，$a,b$较大时预处理阶乘与阶乘逆元进行计算。当$a,b$非常大时，使用卢卡斯定理$C_a^b \mod p = C_{a \mod p}^{b \mod p} * C_{a/p}^{b/p} \mod p$

```c++
// 数据量不大
const int mod = 1e9 + 7;
int c[N][N];
void init()
{
    for (int i = 0; i < N; i ++ )
        for (int j = 0; j <= i; j ++ )
        {
            if (!j) c[i][j] = 1;
            else c[i][j] = (c[i-1][j] + c[i-1][j-1]) % mod;
        }
}

// a,b较大
int fact[N], infact[N];
int qmi(int a, int m, int p)
{
    int res = 1;
    while (k)
    {
        if (k & 1) res = (LL)res * a % p;
        a = (LL)a * a % p;
        k >>= 1;
    }
    return res;
}
void init()
{
    fact[0] = infact[0] = 1;
    for (int i = 1; i < N; i ++ )
    {
        fact[i] = (LL)fact[i-1]*i % mod;
        infact[i] = (LL)infact[i-1] * qmi(i, mod - 2, mod) % mod;
    }
}

// 卢卡斯定理
int p;

int qmi(int a, int k)
{
    int res = 1;
    while (k)
    {
        if (k & 1) res = (LL)res * a % p;
        a = (LL)a * a % p;
        k >>= 1;
    }
    return res;
}

int C(int a, int b)
{
    int res = 1;
    for (int i = 1, j = a; i <= b; i ++ ,j -- )
    {
        res = (LL)res * j % p;
        res = (LL)res * qmi(i, p-2) % p;
    }
    return res;
}

int lucas(LL a, LL b)
{
    if (a < p && b < p) return C(a, b);
    return (LL)C(a % p, b % p) * lucas(a/p, b/p) % p;
}
```

容斥原理：枚举所有选法的时候，使用位运算：

```c++
for (int i = 1; i < 1 << n; i ++ )
{
    int cnt = 0;
}
```

Nim游戏：玄学SG异或

## 动态规划

闫氏DP分析法：从两个角度来考虑——状态表示和状态计算。状态表示中，一个是代表的集合是什么，另一个是集合的属性是什么。状态计算考虑每个状态表示如何计算出来，主要是动态规划的转移方程，对应于集合的划分——不重、不漏。

### 背包问题

01背包问题：$N$个物品和容量$V$的背包，每件物品最多只用一次，第$i$个物品的体积为$v_i$，价值为$w_i$，要最大化背包里面物品的价值。

完全背包问题：在01背包的基础上，每件物品可以用无限次。

多重背包问题：在01背包的基础上，每件物品可以用最多$s_i$次。**二进制优化**：将相同物品进行二进制打包，然后打包后的物品看成是新的物品从而转化成01背包问题。

分组背包问题：在01背包的基础上，物品是分组的，对于每个组里的物品只能选一个。

### 线性DP

线性DP：求解DP的顺序是线性的。

### 区间DP

区间DP：指状态表示一般是区间。

### 计数类DP

计数类DP：指状态只与数字有关的问题。

### 数位DP

分类讨论是核心。

### 状态压缩DP

状态压缩DP：状态虽然是整数，但是要看做是二进制数，对于每一位是0是1对应不同的情况。

### 树形DP

整体状态结构是树形的，一般采用记忆化搜索和DFS解决。
