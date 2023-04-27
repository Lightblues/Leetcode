#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>

using namespace std;

class Solution {
public:
    void printVector(vector<int>& v) {
        for (auto a:v) cout << a << " ";
        cout << endl;
    }
    void printInt(int a) {
        cout << a << endl;
    }
    void printString(string s) {
        cout << s << endl;
    }



/* 1678. 设计 Goal 解析器 */
    string interpret(string command) {
        int n = command.size();
        string s;
        for (int i=0; i<n; i++) {
            if (command[i]=='G') s+= 'G';
            else if (command[i+1]==')') {
                s += 'o';
                i++;
            } else {
                s += "al";
                i += 3;
            }
        }
        return s;
    }
    void testInterpret() {
        printString(interpret("G()(al)"));
    }

/* 1679. K 和数对的最大数目 */
    int maxOperations(vector<int>& nums, int k) {
        // unordered_map
        unordered_map<int, int> freq;
        for (int num: nums) { freq[num] ++; }
        int ans = 0;
        for (auto [key, value]: freq) {
            if (key*2 == k) ans += value/2;
            else if (key*2<k && freq.count(k-key)) ans += min(value, freq[k-key]);
        }
        return ans;
    }
    void testMaxOperations(){
        vector<int> v = {1,2,3,4};
        printInt(maxOperations(v, 5));
    }

/* 1680. 连接连续二进制数字 */
    int concatenatedBinary(int n) {
        static constexpr int mod = 1000000007;

        int ans = 0;
        int shift = 0;
        for (int i=1; i<=n; i++) {
            // 如何判断是2的整数次幂? 一种方式是计算 `i & (i-1) == 0`
            if (!(i & (i-1))) {
                shift++;
            }
            // static_cast
            ans = ((static_cast<long long>(ans) << shift) + i) % mod;
        }
        return ans;
    }
    void testConcatenatedBinary(){
        printInt(concatenatedBinary(3));
        printInt(concatenatedBinary(12));
    }
};


Solution sol;
// vector<int> ans = {
//     // s.numberOfMatches(7),
//     // s.numberOfMatches(8),
//     // s.minPartitions("11"),
//     // s.minPartitions("27346209830709182346"),
// };

int main() {
    // sol.testInterpret();
    // sol.testMaxOperations();
    sol.testConcatenatedBinary();


    return 0;
}
