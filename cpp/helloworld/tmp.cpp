#include<stdio.h>

/* 找到数组中的指定元素删除 */
int main() {
    // j 标记所找到的元素的位置
    int x, j = -1;
    int a[10] = { 1,2,3,4,5,6,7,8,9,10 };
    printf("请输入一个数："); scanf("%d", &x);

    for (int i = 0; i < 10; i++) {
        if (a[i] == x) {
            j = i;
            break;
        }
    }
    // 没找到
    if (j==-1) {
        printf("此数组中没有您想要删除的数字。");
        return 0;
    }
    // 找到了, 删除, 将后面的元素前移
    for (int i = j + 1; i < 10; i++)
        a[i - 1] = a[i];
    for (int i = 0; i < 9; i++)
        printf("%5d", a[i]);
    return 0;
}