#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int findContentChildren(vector<int> &children, vector<int> &cookies)
{
    sort(children.begin(), children.end());
    sort(cookies.begin(), cookies.end());
    int child = 0, cookie = 0;
    while (child < children.size() && cookie < cookies.size())
    {
        if (children[child] <= cookies[cookie])
            ++child;
        ++cookie;
    }
    return child;
}

int main()
{
    vector<int> children = {1, 2, 3};
    vector<int> cookies = {2, 3, 4};
    int child = findContentChildren(children, cookies);
    cout << child << endl;
}

// int main()
// {
//     // Create a vector containing integers
//     std::vector<int> v = {7, 5, 16, 8};

//     // Add two more integers to vector
//     v.push_back(25);
//     v.push_back(13);

//     // Print out the vector
//     std::cout << "v = { ";
//     for (int n : v)
//     {
//         std::cout << n << ", ";
//     }
//     std::cout << "}; \n";
// }