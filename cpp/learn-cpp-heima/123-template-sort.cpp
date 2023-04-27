#include<iostream>

using namespace std;

template<typename T>
void mySwap(T &a, T &b){
    T temp  = a;
    a = b;
    b = temp;
}

template<class T>
void mySort(T arr[], int len){
    for (int i=0; i<len; i++){
        int max = i;
        for(int j=i+1; j<len; j++){
            if(arr[max] < arr[j]){
                max = j;
            }
        }
        if (max != i){
            mySwap(arr[i], arr[max]);
        }
    }
}

template <typename T>
void printArr(T arr[], int len){
    for(int i=0; i<len; i++){
        cout << arr[i] << " ";
    }
    cout << endl;
}

int main () {
    char charArr[] = "afjaidfald";
    int num = sizeof(charArr) / sizeof(char);
    mySort(charArr, num);
    printArr(charArr, num);

    int intArr[] = {1,2,3,4,434,4,2,2,2,1};
    num = sizeof(intArr) / sizeof(int);
    mySort(intArr, num);
    printArr(intArr, num);
}



