/* For loop
https://www.hackerrank.com/challenges/c-tutorial-for-loop/problem?isFullScreen=true&h_r=next-challenge&h_v=zen

input: 
8
11
 */

#include <iostream>
#include <cstdio>
using namespace std;

int main() {
    // Complete the code.
    int a,b;
    scanf("%d", &a); scanf("%d", &b);
    for (int n=a; n<=b; n++){
        if (n==1) {
            cout << "one";
        } else if (n==2) {
            cout << "two";
        } else if (n==3) {
            cout << "three";
        } else if (n==4) {
            cout << "four";
        } else if (n==5) {
            cout << "five";
        } else if (n==6) {
            cout << "six";
        } else if (n==7) {
            cout << "seven";
        } else if (n==8) {
            cout << "eight";
        } else if (n==9) {
            cout << "nine";
        } else if ((n/2 * 2)==n) {
            cout << "even";
        } else {
            cout << "odd";
        }
        cout << "\n";
    }
    return 0;
}
