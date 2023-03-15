""" 2. Risk Limits

Working at Optiver, you quickly get used to the idea of having millions of dollarsworth of orders "in the market" at any given time. But that doesn't mean we aren'taware of the risks! A misbehaving trading process could lose a lot of money withina few minutes. That is why every order gets checked against a set of risk limitsbefore being sent to the market

Your task is to write a simple version of such a limit-checking system. The systemprocesses orders, consisting of an instrument identifier, a timestamp (given inmilliseconds since midnight), an order volume (always a positive integer) and anorder price (always a positive double). You can assume that orders arrive inincreasing timestamp order.
The system also processes risk limits. For every instrument, the following limits aredefined:

If the value (volume * price) of the order is above a given threshold, your programshould output MAX VAL LIMIT followed by the instrument name, e.g. MAX VAL LIMIT ABC.
If the total volume of all orders in a ten-second period exceeds a certain threshold.your program should output MAX VOL 10S LIMIT and the instrument name.
If the total value of all orders in a one-second period would exceed a certainthreshold, your program should outout MAX VAL 1S LIMIT, again followed the byinstrument name.

For every order, your program should print only the first limit breach it encountersIf multiple limit breaches are present in a single order, they should be checked inthe order given above.

We can't place orders without having limits defined for them; if this happens, your program should output NO LIMITS and the instrument name. Also note that limits may change throughout the day, and the latest version received should be used fochecking any orders received afterwards.

## Function Description
Your task is to implement a class which provides the methods AddLimit andProcessOrder.

## Input Format For Custom Testing
The first line contains an integer, n, denoting the number of elements in ARRAY_NAME.
Each line i of the n subsequent lines (where 0<=i< n) contains a(n) DATA_TYPE describing ARRAY_NAME_i
 """
from collections import defaultdict, deque

class RiskLimitProcessor:
    def __init__(self):
        self.limits = {}
        self.instru2orders = defaultdict(list)
        # val10, val1, p10, p1 = 0, 0, 0, 0
        self.instru2vals = defaultdict(lambda : (0,0,0,0))
        self.instru2limit = defaultdict(lambda: False)
    
    def AddLimit(self, instrument, maxValue, maxVolume10Seconds, maxValue1Second):
        self.limits[instrument] = (maxValue, maxVolume10Seconds, maxValue1Second)

    def ProcessOrder(self, instrument, timestamp, volume, price):
        if self.instru2limit[instrument]:
            return
        timestamp /= 1000

        val10, val1, p10, p1 = self.instru2vals[instrument]
        orders = self.instru2orders[instrument]
        if instrument in self.limits:
            maxValue, maxVolume10Seconds, maxValue1Second = self.limits[instrument]
            if volume*price > maxValue:
                print(f"MAX_VAL_LIMIT {instrument}")
                self.instru2limit[instrument] = True
                return
            # p10, p1 = self.instru2pointer10[instrument], self.instru2pointer1[instrument]

            while p10<len(orders) and orders[p10][0] < timestamp-10:
                val10 -= orders[p10][1]*orders[p10][2]
                p10 += 1
            if val10 + volume*price > maxVolume10Seconds:
                print(f"MAX_VAL_10S_LIMIT {instrument}")
                self.instru2limit[instrument] = True
                return
            while p1<len(orders) and orders[p1][0] < timestamp-1:
                val1 -= orders[p1][1]*orders[p1][2]
                p1 += 1
            if val1 + volume*price > maxValue1Second:
                print(f"MAX_VAL_1S_LIMIT {instrument}")
                self.instru2limit[instrument] = True
                return
        orders.append((timestamp, volume, price))
        val10 += volume*price
        val1 += volume*price
        self.instru2vals[instrument] = (val10, val1, p10, p1)

        # print(f"NO_LIMITS {instrument}")



def main():
    riskLimitProcessor = RiskLimitProcessor()
    while True:
        try:
            inp = input()
        except EOFError:
            break
        if not inp: break
        action, instrument,a,b,c = inp.split()
        if action == "LIMIT":
            riskLimitProcessor.AddLimit(instrument, float(a), int(b), float(c))
        elif action == "ORDER":
            riskLimitProcessor.ProcessOrder(instrument, int(a), int(b), float(c))
        else:
            print("Malformed input!")
            return(-1)
    return 0


if __name__=="__main__":
    main()