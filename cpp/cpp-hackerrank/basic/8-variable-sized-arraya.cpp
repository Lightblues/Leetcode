/* 

https://www.hackerrank.com/challenges/variable-sized-arrays/problem?isFullScreen=true

Click [here](http://www.cplusplus.com/reference/vector/vector/) to know more about how to create variable sized arrays in C++.
 */


#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;


int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */  
    int n,q;
    scanf("%d %d", &n, &q);
    // int arr[n][];
    vector<vector<int>> arr(n);
    for (int i=0; i<n; i++) {
        int k;
        scanf("%d", &k);
        arr[i].resize(k);
        for (int j=0; j<k; j++) {
            scanf("%d", &(arr[i][j]));
        }
    }
    // querys arr[i][j]
    for (int i=0; i<q; i++) {
        int a,b;
        scanf("%d %d", &a, &b);
        printf("%d\n", arr[a][b]);
    }
    return 0;
}