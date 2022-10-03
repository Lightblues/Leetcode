#include <iostream>
using namespace std;

/* [789. 数的范围](https://www.acwing.com/problem/content/791/)
给定一个数组, 每次查询找到其中x出现的范围, 没有出现的话返回 -1
 */

const int N = 1e5 + 10;
int n,m;
int q[N];


int main(){
    scanf("%d%d",&n,&m);
    for (int i = 0; i < n; i ++ ) scanf("%d", &q[i]);
    while (m--) {
        int x;
        scanf("%d", &x);
        // 查找第一个大于等于x的数
        int l = 0, r = n - 1;
        while (l < r) {
            // 1) 这里更新方式 l = mid + 1, 因此可取 mid = l + r >> 1
            int mid = (l + r) >> 1;
            if (q[mid] >= x) r = mid;
            else l = mid + 1;
        }
        if (q[l]!=x) {
            // 没找到. 直接返回
            cout << "-1 -1" << endl;
        } else {
            cout << l << ' ';
            int l = 0, r = n - 1;
            while (l < r) {
            // 2) 这里 l = mid, 因此mid不能取左侧, 需要 mid = l + r + 1 >> 1
                int mid = (l + r + 1) >> 1;
                if (q[mid] <= x) l = mid;
                else r = mid - 1;
            }
            cout << r << endl;
        }
    }
}