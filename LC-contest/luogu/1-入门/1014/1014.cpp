#include <cstdio>
// https://www.luogu.com.cn/blog/char32-t/solution-p1014
int main() {
    int n, i=0, j=0;//前i条斜线一共j个数
    scanf("%d", &n);
    while(n>j) {//找到最小的i使得j>=n
        i++;
        j+=i;
    }
    if(i%2==1)
        printf("%d/%d",j-n+1,i+n-j);//i的奇偶决定着斜线上数的顺序,n是第i条斜线上倒数第j-n+1个数
    else
        printf("%d/%d",i+n-j,j-n+1);//若i是偶数，第i条斜线上倒数第i个元素是(i+1-i)/i
    return 0;
}