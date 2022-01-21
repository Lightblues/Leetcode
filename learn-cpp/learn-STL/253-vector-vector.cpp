#include<iostream>
#include<vector>

using namespace std;


int main(){
    vector< vector<int> > v;
    vector<int> v1;
    vector<int> v2, v3, v4;
    for(int i=0; i<4; i++){
        v1.push_back(i+1);
        v2.push_back(i+2);
        // 长度不等也行
    }
    v.push_back(v1);
    v.push_back(v2);
    v.push_back(v3);
    v.push_back(v4);

    for(vector<vector<int> >::iterator it=v.begin(); it!=v.end(); it++){
        for(vector<int>::iterator itt=(*it).begin(); itt!=(*it).end(); itt++){
            cout << *itt << "\t";
        }
        cout << endl;
    }

}

