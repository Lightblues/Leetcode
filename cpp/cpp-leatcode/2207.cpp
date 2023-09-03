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
    // sol.testConcatenatedBinary();
    sol.printInt(1);
    sol.printString("hello");
    // sol.printVector(vector<int>{1,2,3});


    return 0;
}
