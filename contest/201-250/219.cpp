#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>

using namespace std;

class Solution {
public:
    void printVector(vector<int>& v) {
        // for (int i = 0; i < v.size(); i++) {
        //     cout << v[i] << " ";
        // }
        for (auto a:v) cout << a << " ";
        cout << endl;
    }
    void printInt(int a) {
        cout << a << endl;
    }


/* 1688. 比赛中的配对次数 */
    int numberOfMatches(int n) {
        int ans = 0;
        while (n>1) {
            if (n%2==0) {
                ans += n/2;
                n /= 2;
            } else {
                // int 整除
                ans += n/2;
                n = n/2 + 1;
            }
        }
        return ans;
    }
/* 1689. 十-二进制数的最少数目 */
    int minPartitions(string n) {
        int ans = 0;
        // 遍历字符串, 计算差值
        for (char c:n) {
            ans = max(c-'0', ans);
        }
        return ans;
    }

/* 1690. 石子游戏 VII
 */
    int stoneGameVII(vector<int>& stones) {
        int n = stones.size();
        vector<vector<int>> sum(n, vector<int>(n, 0));
        for (int i=0; i<n; i++) {
            for (int j=i; j<n; j++) {
                if (i==j) sum[i][j] = stones[i];
                else sum[i][j] = stones[j] + sum[i][j-1];
            }
        }
        vector<vector<int>> f(n, vector<int>(n, 0));
        for (int i=n-1; i>=0; i--) {
            for (int j=i+1; j<n; j++) {
                f[i][j] = max(sum[i+1][j] - f[i+1][j], sum[i][j-1] - f[i][j-1]);
            }
        }
        return f[0][n-1];
    }
    void testStoneGameVII(){
        vector<int> stones = {5,3,1,4,2};
        int result = stoneGameVII(stones);
        printInt(result);
        stones = {7,90,5,1,100,10,10,2};
        result = stoneGameVII(stones);
        printInt(result);
    }

/* 1691. 堆叠长方体的最大高度 #hard */
int maxHeight(vector<vector<int>>& cuboids) {
    int n = cuboids.size();
    for (auto& cubic: cuboids) {
        // 排序
        sort(cubic.begin(), cubic.end());
    }
    // 保证枚举关系拓扑性的排序都可以
    // sort(cuboids.begin(), cuboids.end());
    sort(cuboids.begin(), cuboids.end(), [](const auto& u, const auto& v){
        return pair(u[2], u[0]+u[1]) < pair(v[2], v[0]+v[1]);
    });     // 自定义排序函数
    vector<int> f(n);
    for (int i=0; i<n; i++) {
        for (int j=0; j<i; j++) {
            if (cuboids[j][0]<=cuboids[i][0] && cuboids[j][1]<=cuboids[i][1] && cuboids[j][2]<=cuboids[i][2] ) {
                f[i] = max(f[i], f[j]);
            }
        }
        f[i] += cuboids[i][2];
    }
    return *max_element(f.begin(), f.end());
}
};


Solution s;
// vector<int> ans = {
//     // s.numberOfMatches(7),
//     // s.numberOfMatches(8),
//     // s.minPartitions("11"),
//     // s.minPartitions("27346209830709182346"),
// };

int main() {
    
    // s.testTwoSum();
    s.testStoneGameVII();
    // for (auto a:ans) {
    //     s.printInt(a);
    // }
    // s.printVector(ans);





    return 0;
}
