#include<iostream>
using namespace std;

void prime1() {
    // 找到 2-100 之间的质数
    int i,j;
    for(i=2; i<100; i++){
        for(j=2; j<i/j; j++) {
            if (!(i%j)){
                break;      //说明 i 不是质数
            }
        }
        if (j>(i/j)){
            cout << i << " 是质数\n";
        }
    }
}



// 来自评论区。根据质数的倍数一定不是质数，利用线性筛法，可以让时间复杂度达到O(n）
#define MAXN_N 1000001
int v[MAXN_N],primes[MAXN_N];//primes用来存储素数
int prime2()
{
    int n,m=0;//m 是素数的数目 
    cout << "输入 n 的值：" << endl;
    scanf("%d",&n);
    memset(v,0,sizeof(v));
    for(int i=2;i<=n;i++)
    {
        if(v[i]==0)//i是素数 
        {
            v[i]=i;
            primes[++m]=i;
        }
        for(int j=1;j<=m;j++)
        {
            if(primes[j]>v[i]||primes[j]>n/i)break;//i有比primes[j]更小的质因子，或者超出范围
            v[i*primes[j]]=primes[j];//primes[j]是合数i*primes[j]的最小质因子 
        }
    }
    for(int i=1;i<=m;i++) cout<<primes[i]<<" ";
    return 0;
} 


int main() {
    prime2();
}