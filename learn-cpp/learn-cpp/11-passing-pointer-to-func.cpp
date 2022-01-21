#include <iostream>
#include <ctime>
 
using namespace std;
 
void getSeconds(int *par)
{
   // 获取当前的秒数
   *par = time( NULL );
   return;
}

int main ()
{
   int sec;
 
 
   getSeconds( &sec );

   long a = sec;
   short b = sec;
 
   // 输出实际值
   cout << "Number of seconds :" << sec << "\t" << b << endl;
 
   return 0;
}
 
