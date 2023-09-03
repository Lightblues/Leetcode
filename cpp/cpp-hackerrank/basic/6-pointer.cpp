/* 
https://www.hackerrank.com/challenges/c-tutorial-pointer/problem?isFullScreen=true&h_r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen

wiki [pointer](https://en.wikipedia.org/wiki/Pointer_%28computer_programming%29)

利用指针, 可以对于不属于当前元素的变量进行操作, 例如:
void increment(int *v) {
    (*v)++;
}
 */

#include <stdio.h>

void update(int *a,int *b) {
    /* 实现分别设置 a,b 为 a+b, abs(a-b) */
    // Complete this function  
    int tmp = *a + *b;
    *b -= *a;
    if (*b < 0){*b = -*b;}
    *a = tmp;
}

int main() {
    int a, b;
    int *pa = &a, *pb = &b;
    
    scanf("%d %d", &a, &b);
    update(pa, pb);
    printf("%d\n%d", a, b);

    return 0;
}