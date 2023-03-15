#include <cassert>
#include <map>
#include <set>
#include <list>
#include <cmath>
#include <ctime>
#include <deque>
#include <queue>
#include <stack>
#include <string>
#include <bitset>
#include <cstdio>
#include <limits>
#include <vector>
#include <climits>
#include <cstring>
#include <cstdlib>
#include <fstream>
#include <numeric>
#include <sstream>
#include <iostream>
#include <algorithm>
#include <unordered_map>
#include <iomanip>
#include <array>


// This is the class you need to implement! Feel free to add members, private methods etc, but don't change the public
// method signatures.
// class RiskLimitProcessor
// {
//     public:
//         void AddLimit(const std::string& instrument, double maxValue, int maxVolume10Seconds, double maxValue1Second)
//         {
//         }

//         void ProcessOrder(const std::string& instrument, uint64_t timestamp, int volume, double price)
//         {
//             std::cout << "NO_LIMITS XXX" << std::endl;
//         }
// };

using namespace std;

class RiskLimitProcessor {
private:
    unordered_map<string, tuple<double, int, double>> limits;
    unordered_map<string, vector<tuple<int, int, double>>> instru2orders;
    unordered_map<string, tuple<int, int, double>> instru2vals;
public:
    void AddLimit(string instrument, double maxValue, int maxVolume10Seconds, double maxValue1Second) {
        limits[instrument] = make_tuple(maxValue, maxVolume10Seconds, maxValue1Second);
    }

    void ProcessOrder(string instrument, int timestamp, int volume, double price) {
        timestamp /= 1000;
        auto [maxValue, maxVolume10Seconds, maxValue1Second] = limits[instrument];
        if (volume * price > maxValue) {
            cout << "MAX_VAL_1S_LIMIT " << instrument << endl;
            return;
        }
        auto [val10, val1, p10, p1] = instru2vals[instrument];
        auto& orders = instru2orders[instrument];
        while (p10 < orders.size() && get<0>(orders[p10]) < timestamp - 10) {
            val10 -= get<1>(orders[p10]) * get<2>(orders[p10]);
            p10 += 1;
        }
        if (val10 + volume * price > maxVolume10Seconds) {
            cout << "MAX_VAL_10S_LIMIT " << instrument << endl;
            return;
        }
        while (p1 < orders.size() && get<0>(orders[p1]) < timestamp - 1) {
            val1 -= get<1>(orders[p1]) * get<2>(orders[p1]);
            p1 += 1;
        }
        if (val1 + volume * price > maxValue1Second) {
            cout << "MAX_VAL_LIMIT " << instrument << endl;
            return;
        }
        orders.emplace_back(timestamp, volume, price);
        val10 += volume * price;
        val1 += volume * price;
        instru2vals[instrument] = make_tuple(val10, val1, p10, p1);
    }
};



int main()
{
    RiskLimitProcessor riskLimitProcessor;
    while(!std::cin.eof())
    {
        std::string action, instrument;
        std::cin >> action >> instrument;
        if (action.empty())
            break; // handle whitespace at end of input
        if (action == "LIMIT")
        {
            double maxValue;
            int maxVolume10Seconds;
            double maxValue1Second;
            std::cin >> maxValue >> maxVolume10Seconds >> maxValue1Second;
            riskLimitProcessor.AddLimit(instrument, maxValue, maxVolume10Seconds, maxValue1Second);
        }
        else if (action == "ORDER")
        {
            uint64_t timestamp;
            int volume;
            double price;
            std::cin >> timestamp >> volume >> price;
            riskLimitProcessor.ProcessOrder(instrument, timestamp, volume, price);
        }
        else
        {
            std::cerr << "Malformed input!\n";
            return -1;
        }
    }
    return 0;
}