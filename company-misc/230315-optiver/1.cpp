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

enum class BuySell
{
    BUY,
    SELL
};

class PnLCalculator
{
private:
    std::unordered_map<std::string, std::vector<std::vector<int>>> n2t;
    std::unordered_map<std::string, int> n2p;

public:
    void ProcessTrade(int64_t tradeId, const std::string& instrumentId, BuySell buySell, int64_t price, int64_t volume)
    {
        std::vector<int> tmp;
        tmp.push_back(tradeId);
        if (buySell == BuySell::BUY) tmp.push_back(0);
        else tmp.push_back(1);
        tmp.push_back(price);
        tmp.push_back(volume);
        n2t[instrumentId].push_back(tmp);
    }

    void ProcessPriceUpdate(const std::string& instrumentId, int64_t price)
    {
        n2p[instrumentId] = price;
    }

    // returns the output string to be printed
    std::string OutputWorstTrade(const std::string& instrumentId)
    {
        auto tmp = n2t[instrumentId];
        int n = tmp.size();
        std::vector<int> loss;
        int ans = 0, max_l = 0;
        for (int i = 0; i < n; i ++ ) {
            int l = 0;
            int type = tmp[i][1];
            if (type == 0) {
                if (n2p[instrumentId] < tmp[i][2])
                    l += (tmp[i][2] - n2p[instrumentId])*tmp[i][3];
            } else {
                if (n2p[instrumentId] > tmp[i][2])
                    l += (n2p[instrumentId]- tmp[i][2])*tmp[i][3];
            }
            loss.push_back(l);
            if (l >= max_l) max_l = l, ans = tmp[i][0];
        }
        if (max_l == 0) return "NO BAD TRADES";
        return std::to_string(ans);
    }
};

int main()
{
    uint64_t N;
    std::cin >> N;

    PnLCalculator calculator;
    for (size_t i = 0; i < N; ++i)
    {
        std::string queryType;
        std::cin >> queryType;
        if (queryType == "TRADE")
        {
            std::string instrumentId, buySell;
            uint64_t tradeId, price, volume;
            std::cin >> tradeId >> instrumentId >> buySell >> price >> volume;
            if (buySell == "BUY")
            {
                calculator.ProcessTrade(tradeId, instrumentId, BuySell::BUY, price, volume);
            }
            else if (buySell == "SELL")
            {
                calculator.ProcessTrade(tradeId, instrumentId, BuySell::SELL, price, volume);
            }
            else
            {
                std::cerr << "Malformed input!\n";
                return -1;
            }
        }
        else if (queryType == "PRICE")
        {
            std::string instrumentId;
            uint64_t price;
            std::cin >> instrumentId >> price;
            calculator.ProcessPriceUpdate(instrumentId, price);
        }
        else if (queryType == "WORST_TRADE")
        {
            std::string instrumentId;
            std::cin >> instrumentId;
            std::string output = calculator.OutputWorstTrade(instrumentId);
            std::cout << output << std::endl;
        }
        else
        {
            std::cerr << "Malformed input!\n";
            return -1;
        }
    }

    return 0;
}