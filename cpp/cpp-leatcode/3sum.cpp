/**
 * 3Sum
 *
 * Given an array S of n integers, are there elements a, b, c in S such that
 * a + b + c = 0?  Find all unique triplets in the array which gives the sum of
 * zero.
 *
 * Note:
 *
 *    - Elements in a triplet (a, b, c) must be in non-descending order (i.e.,
 *      a <= b <= c).
 *
 *    - The solution set must not contain duplicate triplets.
 *      For example, given array S = {-1 0 1 2 -1 -4},
 *      A solution set is:
 *         (-1, 0, 1)
 *         (-1, -1, 2)
 *
 * Tags: Array, Two Pointers
 */

#include <iostream>
#include <string>
#include <sstream>
#include <vector>
#include <iterator>
#include <algorithm>

using namespace std;

class Solution {
public:
    vector<vector<int>> threeSum(vector<int>& num) {
        vector<vector<int>> triplets;
        sort(num.begin(), num.end());
        for (int i = 0; i < int(num.size()-2); ++i) {
            if (i > 0 && num[i] == num[i-1])
                continue;
            int j = i+1;
            int k = num.size()-1;
            while (j < k) {
                if (j > i+1 && num[j] == num[j-1]) {
                    ++j;
                    continue;
                }
                if (k < num.size()-1 && num[k] == num[k+1]) {
                    --k;
                    continue;
                }
                if (num[i] + num[j] + num[k] < 0)
                    ++j;
                else if (num[i] + num[j] + num[k] > 0)
                    --k;
                else {
                    triplets.push_back({num[i], num[j], num[k]});
                    ++j, --k;
                }
            }
        }
        return triplets;
    }

    vector<vector<int>> threeSum2(vector<int> &num) {
        vector<vector<int>> triplets;
        sort(num.begin(), num.end());
        for (int i = 0; i < num.size()-2; ++i) {
            int j = i + 1;
            int k = num.size()-1;
            while (j < k) {
                if (num[i] + num[j] + num[k] < 0)
                    ++j;
                else if (num[i] + num[j] + num[k] > 0)
                    --k;
                else {
                    triplets.push_back(vector<int>{num[i], num[j], num[k]});
                    ++j, --k;
                }
            }
        }
        sort(triplets.begin(), triplets.end());
        triplets.erase(unique(triplets.begin(), triplets.end()), triplets.end());
        return triplets;
    }
};

int main(int argc, char *argv[]) {
    string line;
    while (getline(cin, line)) {
        istringstream iss(line);
        // Initialize num
        vector<int> num((istream_iterator<int>(iss)), istream_iterator<int>());
        // Get all triplets (a, b, c) where a + b + c = 0
        vector<vector<int>> triplets = Solution().threeSum2(num);
        // Print all triplets
        for (const auto& triplet : triplets) {
            copy(triplet.begin(), triplet.end(), ostream_iterator<int>(cout, " "));
            cout << endl;
        }
    }
    return 0;
}