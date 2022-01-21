#include <iostream>
#include <vector>

using namespace std;


int findContentChildren(vector<int>& children, vector<int>& cookies) {
    sort(children.begin(), children.end());
    sort(cookies.begin(), cookies.end());
    int child=0, cookie=0;
    while (child<children.size() && cookie<cookies.size()) {
        if (children[child] <= cookies[cookie]) ++child;
        ++cookie;
    }
    return child;
}

int main() {
    int c[] = {1,2,3};
    // for (int i=0; i<3; i++){

    // }
    vector<int> children(*c);
    vector<int> cookies(*c);
    int r = findContentChildren(children, cookies);
    cout << children.data() <<r << endl;

}