#include <iostream>
 
using namespace std;

const int MAX = 3;
int main (){
   int var[MAX] = {10, 100, 200};
   int * ptr;

   cout << var[MAX-1]<< endl;

   ptr = &var[MAX-1];
   printf("ptr: %p value: %i\n", ptr, *ptr);
   ptr = var;
   printf("ptr: %p value: %i\n", ptr, *ptr);

}