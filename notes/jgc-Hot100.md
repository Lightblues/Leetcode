# Leetcode Hot 100 经典题目

[🔥 LeetCode 热题 HOT 100](https://leetcode.cn/problem-list/2cktkvj/)

## 23. 合并K个升序链表

第一个思路就是使用**分治算法**，一开始将k个链表配对并将同一对中的链表合并，一轮合并后，链表数目减半，平均长度加倍，重复这一过程就可以得到最后的链表。整体时间复杂度是$O(\sum_{i=1}^\infty \frac{k}{2^i} \times 2^i n) = O(kn \log k)$

```c++
class Solution {
public:
    ListNode* mergeTwoLists(ListNode* a, ListNode* b) {
        if ((!a) || (!b)) return a ? a : b;
        ListNode head, *tail = &head, *aPtr = a, *bPtr = b;
        while (aPtr && bPtr) {
            if (aPtr->val < bPtr->val) {
                tail->next = aPtr;
                aPtr = aPtr->next;
            } else {
                tail->next = bPtr;
                bPtr = bPtr->next;
            }
            tail = tail->next;
        }
        tail->next = (aPtr ? aPtr : bPtr);
        return head.next;
    }

    ListNode* merge(vector<ListNode*>& lists, int l, int r) {
        if (l == r) return lists[l];
        if (l > r) return nullptr;
        int mid = (l + r) >> 1;
        return mergeTwoLists(merge(lists, l, mid), merge(lists, mid + 1, r));
    }

    ListNode* mergeKLists(vector<ListNode*>& lists) {
        return merge(lists, 0, lists.size() - 1);
    }
};
```

第二个思路是使用**优先队列**，每次维护当前每个链表没有被合并的元素的最前面一个，k个链表就最多有k个满足这样条件的元素，每次在这些元素里面选取值最小的元素合并到答案中，在选择这个元素的过程，可以使用优先队列来操作。

```c++
class Solution {
public:
    ListNode* mergeKLists(vector<ListNode*>& lists) {
        function<bool(ListNode*, ListNode*)> cmp = [](ListNode* a, ListNode* b) -> bool {
            return a->val > b->val;
        };
        priority_queue<ListNode*, vector<ListNode*>, decltype(cmp)> q(cmp);
        for (auto node : lists)
            if (node)
                q.push(node);
        ListNode* head = new ListNode();
        ListNode* tail = head;
        while (!q.empty()) {
            ListNode* node = q.top();
            q.pop();
            tail->next = node;
            tail = tail->next;
            if (node->next) q.push(node->next);
        }
        return head->next;
    }
};
```

## 42. 接雨水

第一个思路是**动态规划**，记录两个动态规划数组left（记录位置i及其左边的最大高度）和right（记录位置i及其右边的最大高度），先从左到右扫一遍更新left，再从右到左扫一遍更新right，最后从左到右每次对位置i计算贡献的雨水即可。时间复杂度为$O(n)$，空间复杂度为$O(n)$。

```c++
class Solution {
public:
    int trap(vector<int>& height) {
        int n = height.size();
        int left[n], right[n];
        left[0] = height[0];
        right[n-1] = height[n-1];
        for (int i = 1; i < n; i ++ )
            left[i] = max(left[i-1], height[i]);
        for (int i = n - 2; i >= 0; i -- )
            right[i] = max(right[i+1], height[i]);
        int res = 0;
        for (int i = 0; i < n; i ++ )
            res += min(left[i], right[i]) - height[i];
        return res;
    }
};
```

第二个思路是**双指针**，因为在动态规划中的数组left和right中的元素都只会使用一次，因此可以用常量记录来优化掉使用的空间。具体来说，初始化left指针和right指针为数组两端，当两个指针没有相遇时，先更新两个指针对应的方向的最大高度，然后判断当前两指针高度大小：如果height[left] < height[right]，说明肯定有leftMax < rightMax，那么left处能够接到的雨水量就是leftMax - height[left]，然后left向右移动；反之就对right进行操作。两指针移动的逻辑从一开始就是移动低高度的指针，这样可以保证过程中更新的左右最大高度和当前高度的大小关系一致。时间复杂度为$O(n)$，空间复杂度为$O(1)$。

```c++
class Solution {
public:
    int trap(vector<int>& height) {
        int n = height.size();
        int res = 0;
        int left = 0, right = n - 1;
        int leftMax = 0, rightMax = 0;
        while (left < right) {
            leftMax = max(leftMax, height[left]);
            rightMax = max(rightMax, height[right]);
            if (height[left] < height[right]) {
                res += leftMax - height[left];
                left ++ ;
            } else {
                res += rightMax - height[right];
                right -- ;
            }
        }
        return res;
    }
};
```

## 46. 全排列

经典的**回溯**题目。时间复杂度$O(n\cdot n!)$，空间复杂度$O(n)$。

```c++
class Solution {
public:
    vector<vector<int>> permute(vector<int>& nums) {
        int n = nums.size();
        vector<vector<int>> res;
        vector<int> path(n), on_path(n);
        function<void(int)> dfs = [&](int i) {
            if (i == n) {
                res.emplace_back(path);
                return;
            }
            for (int j = 0; j < n; j ++ ) {
                if (!on_path[j]) {
                    path[i] = nums[j];
                    on_path[j] = true;
                    dfs(i+1);
                    on_path[j] = false;
                }
            }
        };
        dfs(0);
        return res;
    }
};
```

## 75. 颜色分类

著名的波兰国旗问题，需要使用**快速排序partition**的思路，本质需要将数组分成三段。使用三指针，l为左指针，r为右指针，l记录的是当前需要将0插入的位置，r记录的是当前需要将2插入的位置，同时扫描指针i记录当前需要处理的位置。当nums[i] = 0时，此时应该交换l和i处的数字，互换后应该将l右移，由于i是从0开始向右移动，那么[0, i-1]均是处理过的数，而l必定在其中，所以1的区间应该是[l, i-1]，这就保证了i处交换后为1；当nums[i] = 1时，此时不需要交换，直接i右移即可；当nums[i] = 2时，应该交换r和i处的数字，但由于[i, r]处是没有处理过的区间，所以不能保证交换前r处的数字是1，因此这时候只能将r左移不能移动i。循环处理直到idx > r即可。

```c++
class Solution {
public:
    void sortColors(vector<int>& nums) {
        int n = nums.size();
        int l = 0, r = n - 1;
        for (int i = l; i <= r;) {
            if (nums[i] == 0) swap(nums[i ++ ], nums[l ++ ]);
            else if (nums[i] == 2) swap(nums[i], nums[r -- ]);
            else i ++ ;
        }
        return;
    }
};
```

## 76. 最小覆盖子串

该题目使用**滑动窗口**，窗口内的子串是否可以覆盖需要的子串的判断是使用哈希表完成的，因为该题目的覆盖操作不要求字符串顺序。使用need哈希表记录需要覆盖的字符串t的字符及其个数，window记录滑动窗口内的子串的字符及其个数。初始化窗口左指针l和右指针r都为0，初始化记录变量count为0，初始化答案变量记录字符串s中开始下标start为0，初始化答案子串长度len为INT_MAX。当右指针r未扫描完全时，如果当前r所指的字符是需要的，就将其加入到window中，判断如果当前字符的数量满足要求就count加一。然后判断count是否满足要求（即此时窗口中的子串可以覆盖t），如果这时候的子串长度比len要小，就更新答案变量start和len。然后不断的右移左指针l直至子串不满足要求，期间同时维护好window中的变量和count。做完一次操作就右移右指针r。最后输出即可。

```c++
class Solution {
public:
    string minWindow(string s, string t) {
        unordered_map<char, int> need, window;
        for (auto i:t) need[i] ++ ;
        int l = 0, r = 0, count = 0, len = INT_MAX, start = 0;
        while (r < s.size()) {
            if (need.find(s[r]) != need.end()) {
                window[s[r]] ++ ;
                if (window[s[r]] == need[s[r]]) count ++ ;
            }
            while (count == need.size()) {
                if (len > r - l + 1) {
                    start = l;
                    len = r - l + 1;
                }
                if (need.find(s[l]) != need.end()) {
                    if (need[s[l]] == window[s[l]]) count -- ;
                    window[s[l]] -- ;
                }
                l ++ ;
            }
            r ++ ;
        }
        return len == INT_MAX ? "" : s.substr(start, len);
    }
};
```

## 84. 柱状图中最大的矩形

问题思路是使用**单调栈**，当关注当前位置高度所能计算的矩形时，我们应该关注的是其左边第一个高度小于该高度的位置（left数组）和右边第一个高度小于该高度的位置（right数组），所以这些信息需要提前计算出来。先考虑左边第一个高度小于该高度的位置，因为是左边最靠近的，所以考虑使用栈（LIFO），而由于中间的元素下标对应的高度必然是单调上升的，因为如果中间有高度相等的那么总可以继续扩展，如果中间有高度比之前的低的那么计算中势必会被该元素挡住，原来的高高度元素不再需要，应该出栈，因此应该使用单调栈来计算这个下标。先从左向右扫描，事先在栈中放入下标-1（高度为0）来作为哨兵，每次弹出栈中下标高度大于等于目前下标的下标，然后更新left数组，并将该下标入栈保持栈的单调性质。反过来就是对right数组的更新，同理。最后扫描一遍计算答案即可。

```c++
class Solution {
public:
    int largestRectangleArea(vector<int>& heights) {
        int n = heights.size();
        vector<int> left(n), right(n);
        stack<int> mono_stack;
        for (int i = 0; i < n; i ++ ) {
            while (!mono_stack.empty() && heights[mono_stack.top()] >= heights[i])
                mono_stack.pop();
            left[i] = (mono_stack.empty() ? -1 : mono_stack.top());
            mono_stack.push(i);
        }

        mono_stack = stack<int>();
        for (int i = n - 1; i >= 0; i -- ) {
            while (!mono_stack.empty() && heights[mono_stack.top()] >= heights[i])
                mono_stack.pop();
            right[i] = (mono_stack.empty() ? n : mono_stack.top());
            mono_stack.push(i);
        }

        int ans = 0;
        for (int i = 0; i < n; i ++ )
            ans = max(ans, (right[i] - left[i] - 1) * heights[i]);
        return ans;
    }
};
```

## 124. 二叉树中的最大路径和

使用**递归**，对于最大路径和，要么是左子树的最大路径和，要么是右子树的最大路径和，要么是横跨两个子树经过根节点的最大路径和。对于前两个可以递归的做，但是对于最后一个需要注意能否接上根节点。因此实现一个可以简化的函数maxGain(root)，该函数计算的是二叉树中一个节点的最大贡献值，即以该节点为起点在子树中的一条路径的最大和。这就使得可以分开计算上面三种情况。在递归过程中，维护答案变量maxSum，每次计算当前节点的左节点的最大贡献和右节点的最大贡献，然后用两点贡献加根节点值更新maxSum。由于贡献值的路径不能分叉，因此返回值应该是根节点值加两者最大值。

```c++
class Solution {
private:
    int maxSum = INT_MIN;
public:
    int maxGain(TreeNode* root) {
        if (root == nullptr) return 0;
        int left = max(maxGain(root->left), 0);
        int right = max(maxGain(root->right), 0);
        int nowSum = left + right + root->val;
        maxSum = max(maxSum, nowSum);
        return root->val + max(left, right);
    }

    int maxPathSum(TreeNode* root) {
        maxGain(root);
        return maxSum;
    }
};
```

## 148. 排序链表

使用**自底向上的归并排序**可以使得有$O(n \log n)$的时间复杂度和常数级的空间复杂度。基础的函数是合并两个有序链表的merge。首先求得链表的总长度length，然后使用sublength表示每次需要排序的子链表长度，初始化为1。每次将链表拆分成若干个长度为sublength的子链表，按照每两个子链表一组进行合并，合并后即可得到若干个长度为sublength*2的有序子链表。将sublength的数值加倍，重复上述过程直到有序子链表的长度大于或等于length，整个排序完毕。

```c++
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */
class Solution {
public:
    ListNode* merge(ListNode* a, ListNode* b) {
        if ((!a) || (!b)) return a ? a: b;
        ListNode head, *tail = &head, *aPtr = a, *bPtr = b;
        while (aPtr && bPtr) {
            if (aPtr->val < bPtr->val) {
                tail->next = aPtr;
                aPtr = aPtr->next;
            } else {
                tail->next = bPtr;
                bPtr = bPtr->next;
            }
            tail = tail->next;
        }
        tail->next = (aPtr ? aPtr : bPtr);
        return head.next;
    }

    ListNode* sortList(ListNode* head) {
        if (head == nullptr) return head;
        // 计算链表长度length
        int length = 0;
        ListNode* node = head;
        while (node != nullptr) {
            length ++ ;
            node = node->next;
        }
        // 使用哑节点作为头
        ListNode* dummy = new ListNode(0, head);
        for (int sublength = 1; sublength < length; sublength <<= 1) {
            // curr用于记录拆分链表的位置
            ListNode* pre = dummy, *curr = dummy->next;
            // 如果链表没有拆完
            while (curr != nullptr) {
                ListNode* head1 = curr; // 第一个链表的头
                // 拆分出长度为sublength的子链表
                for (int i = 1; i < sublength && curr->next != nullptr; i ++ )
                    curr = curr->next;
                ListNode* head2 = curr->next; // 第二个链表的头
                curr->next = nullptr; // 断开第一个链表和第二个链表
                curr = head2;
                // 拆分出第二个链表
                for (int i = 1; i < sublength && curr != nullptr && curr->next != nullptr; i ++ )
                    curr = curr->next;
                // 记录第二个链表最后的位置
                ListNode* next = nullptr;
                if (curr != nullptr) {
                    next = curr->next;
                    curr->next = nullptr;
                }
                // 合并拆出来的两个链表
                ListNode* mergeList = merge(head1, head2);
                // 接在需要连接的位置
                pre->next = mergeList;
                // 更新到下一个需要连接的位置
                while (pre->next != nullptr)
                    pre = pre->next;
                // 找到下次拆链表开始的位置
                curr = next;
            }
        }
        return dummy->next;
    }
};
```

## 152. 乘积最大子数组

使用空间优化后的**动态规划**，由于负数乘法的变号性质，可能之前乘积非常小的结果也会很大，所以维护两个动态规划数组，$f_{\mathrm{max}}$与$f_{\mathrm{min}}$，表示以第i个元素结尾的子数组乘积的最大值和最小值，因此转移方程就是
$$
f_{\mathrm{max}}(i) = \max (f_{\mathrm{max}}(i-1)\times a[i], f_{\mathrm{min}}(i-1) \times a[i], a[i]) \\
f_{\mathrm{min}}(i) = \min (f_{\mathrm{max}}(i-1)\times a[i], f_{\mathrm{min}}(i-1) \times a[i], a[i])
$$
不难发现两个数组都只与它们前一个元素有关，可以优化掉空间只用两个变量记录即可。时间复杂度为$O(n)$，空间复杂度为$O(1)$。

```c++
class Solution {
public:
    int maxProduct(vector<int>& nums) {
        int n = nums.size();
        int max_ = nums[0], min_ = nums[0];
        int ans = nums[0];
        for (int i = 1; i < n; i ++ ) {
            int a = max_, b = min_;
            max_ = max(max(a*nums[i], b*nums[i]), nums[i]);
            min_ = min(min(a*nums[i], b*nums[i]), nums[i]);
            ans = max(ans, max_);
        }
        return ans;
    }
};
```

## 206. 反转链表

第一个思路是**迭代**的方法。记录前一个操作的节点指针pre和当前需要操作的节点指针curr，每次要把curr的next指针指向pre。因此，使用next记录curr->next，将curr->next改为pre，然后将pre移动到curr，curr移动到next即可。

```c++
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        ListNode* pre = nullptr;
        auto curr = head;
        while (curr != nullptr) {
            auto next = curr->next;
            curr->next = pre;
            pre = curr;
            curr = next;
        }
        return pre;
    }
};
```

第二个思路是**递归**的方法。每次递归处理head->next后的链表使其反转，反转后head->next实际上就是反转链表的尾部，需要将其接上head，即head->next->next改为head，然后将head->next置空。

```c++
class Solution {
public:
    ListNode* reverseList(ListNode* head) {
        if (head == nullptr || head->next == nullptr) return head;
        auto now = reverseList(head->next);
        head->next->next = head;
        head->next = nullptr;
        return now;
    }
};
```

## 207. 课程表

使用**拓扑排序**即可。

```c++
class Solution {
public:
    int h[5050], e[5050], ne[5050], idx;
    int n;
    int q[5050], d[100010];
    void add(int a, int b) {
        e[idx] = b, ne[idx] = h[a], h[a] = idx ++ ;
    }

    bool topsort() {
        int hh = 0, tt = -1;
        for (int i = 0; i < n; i ++ )
            if (!d[i]) q[ ++ tt] = i;
        while (hh <= tt) {
            int t = q[hh ++ ];
            for (int i = h[t]; i != -1; i = ne[i]) {
                int j = e[i];
                if ( -- d[j] == 0)
                    q[ ++ tt] = j;
            }
        }
        return tt == n - 1;
    }

    bool canFinish(int numCourses, vector<vector<int>>& prerequisites) {
        memset(h, -1, sizeof h);
        for (auto p:prerequisites) {
            add(p[1], p[0]);
            d[p[0]] ++ ;
        }
        n = numCourses;
        return topsort();
    }
};
```

## 236. 二叉树的最近公共祖先

使用**递归**算法，当根节点为空或者p和q中有一个是根节点时，就返回根节点。否则递归得到左子树下p和q的结果和右子树下p和q的结果，如果两个子树都不为空说明p和q位于两子树内，直接返回root，反之显然就在不为空的那个答案上。

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode(int x) : val(x), left(NULL), right(NULL) {}
 * };
 */
class Solution {
public:
    TreeNode* lowestCommonAncestor(TreeNode* root, TreeNode* p, TreeNode* q) {
        if (root == NULL || root == p || root == q) return root;
        auto left = lowestCommonAncestor(root->left, p, q);
        auto right = lowestCommonAncestor(root->right, p, q);
        if (left && right) return root;
        return left ? left : right;
    }
};
```

## 239. 滑动窗口最大值

使用**单调队列**，队列中存储的是数组下标，队列大小不得超过窗口长度k。队列中应该保证队头到队尾对应的数组大小是严格单调减小的，因为一旦存在数组大小一样的两个序列，那么之后的选择中肯定只会选择靠后的下标而不是之前的下标。所以每次入队一个下标时，一直出队直到该下标对应的数组大小大于入队的下标对应的数组大小。时间复杂度为$O(n)$，空间复杂度为$O(k)$。

```c++
class Solution {
public:
    vector<int> maxSlidingWindow(vector<int>& nums, int k) {
        int n = nums.size();
        deque<int> q;
        for (int i = 0; i < k; i ++ ) {
            while (!q.empty() && nums[i] >= nums[q.back()]) q.pop_back();
            q.push_back(i);
        }
        vector<int> ans = {nums[q.front()]};
        for (int i = k; i < n; i ++ ) {
            while (!q.empty() && nums[i] >= nums[q.back()]) q.pop_back();
            q.push_back(i);
            while (q.front() <= i - k) q.pop_front(); // 不在窗口下标范围内
            ans.push_back(nums[q.front()]);
        }
        return ans;
    }
};
```

## 301. 删除无效的括号

使用**回溯**算法。所有的合法方案必然是左括号与右括号数相等，令左括号得分为1，右括号得分为-1，对于合法的方案得分和为0，预处理出最大得分。在回溯搜索中，枚举的字符分三种情况：如果是普通字符就直接添加即可；如果是左括号，得分小于max_n - 1就可以添加左括号，也可以选择不添加；如果是右括号，得分大于0就可以添加右括号，也可以选择不添加。

```c++
class Solution {
public:
    set<string> ans;
    int max_n = 0, len = 0;
    string s;
    vector<string> removeInvalidParentheses(string _s) {
        s = _s;
        int l = 0, r = 0;
        for (char c:s) {
            if (c == '(') l ++ ;
            else if (c == ')') r ++ ;
        }
        max_n = min(l, r);
        dfs(0, 0, "");
        return vector<string>(ans.begin(), ans.end());
    }

    void dfs(int pos, int score, string res) {
        if (score < 0 || score > max_n) return;
        if (pos == s.size()) {
            if (score == 0 && res.size() >= len) {
                if (res.size() > len) ans.clear();
                len = res.size();
                ans.insert(res);
            }
            return;
        }
        char c = s[pos ++ ];
        if (c == '(') {
            dfs(pos, score + 1, res + c);
            dfs(pos, score, res);
        } else if (c == ')') {
            dfs(pos, score - 1, res + c);
            dfs(pos, score, res);
        } else
            dfs(pos, score, res + c);
    }
};
```

## 309. 最佳买卖股票时机含冷冻期

使用**动态规划**，用dp[i]表示第i天结束后的答案结果，因此会有三种状态：

- dp[i][0]表示目前持有一支股票
- dp[i][1]表示目前不持有股票处于冷冻期
- dp[i][2]表示目前不持有股票但不处于冷冻期

因此可以得到对应的状态转移：dp[i][0] = max(dp[i-1][0], dp[i-1][2] - price[i])；dp[i][1] = dp[i-1][0] + price[i]；dp[i][2] = max(dp[i-1][2], dp[i-1][1])。最终答案就是max(dp[n-1][0], dp[n-1][1], dp[n-1][2])

```c++
class Solution {
public:
    int dp[5010][3];
    int maxProfit(vector<int>& prices) {
        int n = prices.size();
        dp[0][0] = -prices[0];
        for (int i = 1; i < n; i ++ ) {
            dp[i][0] = max(dp[i-1][0], dp[i-1][2] - prices[i]);
            dp[i][1] = dp[i-1][0] + prices[i];
            dp[i][2] = max(dp[i-1][1], dp[i-1][2]);
        }
        return max(dp[n-1][1], dp[n-1][2]);
    }
};
```

## 337. 打家劫舍 III

使用**树形DP**，该问题主要学习树形DP的一些写法，并且注意unordered_map的key可以是TreeNode*即可。

```c++
/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    unordered_map<TreeNode*, int> f, g;

    void dfs(TreeNode* node) {
        if (!node) return;
        dfs(node->left);
        dfs(node->right);
        f[node] = g[node->left] + g[node->right] + node->val;
        g[node] = max(f[node->left], g[node->left]) + max(f[node->right], g[node->right]);
    }

    int rob(TreeNode* root) {
        dfs(root);
        return max(f[root], g[root]);
    }
};
```
