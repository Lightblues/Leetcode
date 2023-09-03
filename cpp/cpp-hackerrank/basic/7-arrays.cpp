/* 
https://www.hackerrank.com/challenges/arrays-introduction/problem?isFullScreen=true&h_r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen

An array is a series of elements of the same type placed in contiguous memory locations that can be individually referenced by adding an index to a unique identifier.

Note Unlike C, C++ allows dynamic allocation of arrays at runtime without special calls like malloc(). If , int arr[n] will create an array with space for  integers.


4
1 4 3 2
 */

#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;


int main() {
    /* Enter your code here. Read input from STDIN. Print output to STDOUT */   
    int n;
    scanf("%d", &n);
    int arr[n];
    for (int i=0; i<n; i++) {
        scanf("%d", &(arr[i]));
    }
    for (int i=n-1; i>=0; i--) {
        cout << arr[i] << " ";
    }
    return 0;
}
