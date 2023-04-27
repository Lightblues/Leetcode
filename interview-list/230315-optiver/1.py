""" 
1. Worst Trade Reporter
You are tasked with building a tool to analyze the profitability of trades (also knownas "profit and loss" or PnL). For the purpose of this problem, every trade has thefollowing attributes:

Trade/D - unique identifier for the trade.
Instrument/D identifier of the instrument that has been traded.
Buy/Sell- flag to indicate whether you bought or sold the instrument
Price - the price at which the instrument has been traded,
Volume - the quantity of the instrument that has been traded.

Consider a trade with the following attributes:
TradelD = 5.
Instrument/D= Google
Buy/Sel/= BUY.
Price = 500.
Volume = 20.

It means that you bought 20 lots of Google stock for 500 dollars and the identifierfor the trade is 5.
Note that trades have a TradelD because there can be multiple trades with thesame Instrument/D, Buy/Sell Price and Volume attributes.

## Problem Statement

In this task, you receive a stream of Ninstructions. Each instruction can be anupdate or a query.

An update can be of 2 kinds:

Trade - indicates that a trade has happened.
Attributes: TradelD, InstrumentID, BUY/SELL Price and Volume
Price - indicates that the true value of an instrument has been updated.
Attributes: InstrumentiD and Price.
There is only 1 kind of query:
WorstTrade- output the TradelD of the worst trade for an instrumentAttributes: Instrument/D.
The WorstTrade is the trade with the highest loss made per-lot of the trade. Tocalculate PnL of a trade the latest price update for an instrument is used as thetrue value of the instrument.

lf you sell 2 Google stocks for 500 each, and had the latest price updatesaying Google is worth 400, the PnL for the trade is (500 - 400)* 2 = 200
lf you later get a price update saying Google is worth 600, the PnL for the same tradeis (500 -600)* 2=-200

In the example above, initially we make a profit-per-lot of 200 / 2 = 100, and afterthe price update it is a loss-per-lot of 200 / 2 = 100.
In case of ties for the worst trade, output the latest one.
In case there are no trades that result in a loss for the instrument, output NO BADTRADES.

## Function Description
Your task is to implement a class that provides
methods ProcessTrade, ProcessPriceUpdate, OutputWorstTrade. Thesemethod calls correspond to the instructions described above with the methodarguments corresponding to the update or query attributes.

Constraints
1 <= N, Tradeld, Price, Volume <= 106
It is guaranteed that price update for an instrument is available before first trade onthat instrument.

## Input Format For Custom Testing

Input to the program is specified using a simple text format. The format anddetails of parsing are not relevant to answering the question but custom inputcan be used to help with development and debugging.
The first line of input contains an integer N that denotes the number of instructions. Each of the N subsequent lines contains either an update ora query in the format below:

Updates:
TRADE <TradelD><InstrumentID><BUY/SELL><Price> <Volume>
PRICE <InstrumentlD>Price>
Query:
WORST_TRADE <InstrumentID>

Some example inputs and their expected outputs are described below

思路1: 注意, 交易记录中, 只有buy的最高价和sell的最低价是可能有用的!!
 """

from enum import Enum
from collections import defaultdict
from math import inf

class BuySell(Enum):
    BUY = 0
    SELL = 1

class PnLCalculator:
    def __init__(self) -> None:
        self.price = {}
        self.time = 0
        # instrumentId: (p, tradeId, time)
        self.buymax = defaultdict(lambda : (-inf,0))
        self.sellmin = defaultdict(lambda : (inf,0))

    def ProcessTrade(self, tradeId: int, instrumentId: str, buySell: BuySell, price: int, volume: int) -> None:
        if buySell==BuySell.BUY:
            # if price > self.buymax[instrumentId][0] or \
            #     price==self.buymax[instrumentId][0] and tradeId>self.buymax[instrumentId][1]:
            if price >= self.buymax[instrumentId][0]:
                self.buymax[instrumentId] = (price, tradeId, self.time)
        elif buySell==BuySell.SELL:
            # if price < self.sellmin[instrumentId][0] or \
            #     price == self.sellmin[instrumentId][0] and tradeId>self.sellmin[instrumentId][1]:
            if price <= self.sellmin[instrumentId][0]:
                self.sellmin[instrumentId] = (price, tradeId, self.time)
        self.time += 1

    def ProcessPriceUpdate(self, instrumentId: str, price: int) -> None:
        self.price[instrumentId] = price

    def OutputWorstTrade(self, instrumentId: str) -> str:
        tmp = []
        price = self.price[instrumentId]
        if self.buymax[instrumentId][0] > price:
            p, tradeId, t = self.buymax[instrumentId]
            tmp.append((p-price, tradeId, t))
        if self.sellmin[instrumentId][0] < price:
            p, tradeId, t = self.sellmin[instrumentId]
            tmp.append((price-p, tradeId, t))
        if len(tmp)==0:
            return "NO BAD TRADES"
        tmp.sort(key=lambda x: (-x[0], -x[2]))
        return str(tmp[0][1])
    
if __name__=="__main__":
    N = int(input())
    calculator = PnLCalculator()
    for i in range(N):
        try:
            imp = input().strip()
        except EOFError:
            break
        queryType, imp = imp.split(maxsplit=1)
        if queryType == "TRADE":
            tradeId, instrumentId, buySell, price, volume = imp.split()
            buySell = BuySell.BUY if buySell == "BUY" else BuySell.SELL
            calculator.ProcessTrade(int(tradeId), instrumentId, buySell, int(price), int(volume))
        elif queryType == "PRICE":
            instrumentId, price = imp.split()
            calculator.ProcessPriceUpdate(instrumentId, int(price))
        elif queryType == "WORST_TRADE":
            instrumentId = imp.strip()
            output = calculator.OutputWorstTrade(instrumentId)
            print(output)
        else:
            print("Malformed input!")
            exit(-1)


