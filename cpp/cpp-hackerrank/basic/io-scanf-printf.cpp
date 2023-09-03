/* 
主要参见 https://www.hackerrank.com/domains/cpp
*/

#include <iostream>
#include <cstdio>
// #include <bits/stdc++.h>
using namespace std;

/* 
3 12345678912345 a 334.23 14049.30493
 */
int main() {
    // Complete the code.
    int a;
    long b;
    char c;
    float d;
    double e;
    scanf("%d %ld %c %f %lf", &a, &b, &c, &d, &e);
    printf("%d\n%ld\n%c\n%f\n%lf", a,b,c,d,e);
    return 0;
}