#include <iostream>
 
using namespace std;
const int MAX = 4;

void arr_strings(){
    const char *names[MAX] = {
                   "Zara Ali",
                   "Hina Ali",
                   "Nuha Ali",
                   "Sara Ali",
   };
 
   for (int i = 0; i < MAX; i++)
   {
      cout << "Value of names[" << i << "] = ";
      cout << names[i] << endl;
   }
}

void mytry() {
    int a[] = {12,1,2,1};
    int *p = a;
    cout << p[0] << p[1] <<endl;
}
 
int main ()
{
    mytry();
    return 0;    
}